import logging
import queue
import threading

import pandas
import s3fs
import grpc
from google.protobuf.json_format import MessageToDict

from profiler.config.config import config
from profiler.domain.batch_statistics import BatchStatistics
from profiler.domain.model import Model
from profiler.domain.model_signature import ModelSignature
from profiler.ports.models_repository import ModelsRepository
from profiler.protobuf.monitoring_manager_pb2 import (
    AnalyzedAck,
    BatchStatistics as GBatchStatistics,
    GetInferenceDataUpdatesRequest,
    GetModelUpdatesRequest,
)
from profiler.protobuf.monitoring_manager_pb2_grpc import (
    DataStorageServiceStub,
    ModelCatalogServiceStub,
)
from profiler.use_cases.metrics_use_case import MetricsUseCase
from profiler.use_cases.overall_reports_use_case import OverallReportsUseCase
from profiler.use_cases.report_use_case import (
    ReportUseCase,
)

s3 = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": config.minio_endpoint}, use_listings_cache=False
)


class MonitoringDataSubscriber:
    _metrics_use_case: MetricsUseCase
    _reports_use_case: ReportUseCase
    _overall_reports_use_case: OverallReportsUseCase
    _models_repo: ModelsRepository
    channel: grpc.Channel
    data_stub: DataStorageServiceStub
    model_stub: ModelCatalogServiceStub
    plugin_name: str = "profiler_plugin"

    def __init__(
        self,
        channel: grpc.Channel,
        metrics_use_case: MetricsUseCase,
        reports_use_case: ReportUseCase,
        overall_reports_use_case: OverallReportsUseCase,
        models_repo: ModelsRepository,
    ):
        self.channel = channel
        self._metrics_use_case = metrics_use_case
        self._reports_use_case = reports_use_case
        self._overall_reports_use_case = overall_reports_use_case
        self._model_repo = models_repo
        self.data_stub = DataStorageServiceStub(self.channel)
        self.model_stub = ModelCatalogServiceStub(self.channel)

    def watch_inference_data(self):
        ack_queue = queue.Queue(100)
        init_req = GetInferenceDataUpdatesRequest(plugin_id=self.plugin_name)
        ack_queue.put(init_req)

        def qgetter():
            item = ack_queue.get()
            logging.info("Sending message to the manager")
            return item

        reqs = iter(qgetter, None)
        for response in self.data_stub.GetInferenceDataUpdates(reqs):
            try:
                logging.info("Got inference data")
                model = self.model_from_proto(response)

                if self.training_overall_report_exists(model):
                    for data_obj in response.inference_data_objs:
                        file_url = data_obj.key
                        data_frame = self.fetch_data_frame(file_url)

                        self.process_inference_data_frame(
                            file_url,
                            data_frame,
                            data_obj.lastModifiedAt.ToDatetime(),
                            model,
                        )

                        resp = GetInferenceDataUpdatesRequest(
                            plugin_id=self.plugin_name,
                            ack=AnalyzedAck(
                                model_name=model.name,
                                model_version=model.version,
                                inference_data_obj=data_obj,
                                batch_stats=self.batch_statistics_to_proto(
                                    self.get_batch_statistics(file_url, model)
                                ),
                            ),
                        )

                        ack_queue.put(resp)
                else:
                    logging.warning("Could not find overall report for training data")
                    logging.warning("Waiting for the next message...")
            except Exception as e:
                logging.exception("Error while handling inference data event", e)

    def watch_models(self):
        req = GetModelUpdatesRequest(plugin_id="profiler_plugin")
        for response in self.model_stub.GetModelUpdates(req):
            try:
                logging.info("Got model request")

                model = self.model_from_proto(response)
                self._model_repo.save(model)

                batch_name = "training"
                data_obj = response.training_data_objs[0]

                file_url = data_obj.key
                file_timestamp = data_obj.lastModifiedAt.ToDatetime()
                data_frame = self.fetch_data_frame(file_url)

                self.process_training_data_frame(
                    batch_name=batch_name,
                    file_timestamp=file_timestamp,
                    data_frame=data_frame,
                    model=model,
                )

            except Exception:
                logging.exception("Couldn't process model")

    def start_watching(self):
        logging.info("Start watching...")

        inference_data_thread = threading.Thread(target=self.watch_inference_data)
        inference_data_thread.daemon = True
        inference_data_thread.start()

        models_thread = threading.Thread(target=self.watch_models)
        models_thread.daemon = True
        models_thread.start()

    def process_training_data_frame(
        self, batch_name, file_timestamp, data_frame, model
    ):
        self._metrics_use_case.generate_metrics(model, data_frame)
        report = self._reports_use_case.generate_report(
            model, batch_name, file_timestamp, data_frame
        )

        self._overall_reports_use_case.generate_overall_report(report)

    def process_inference_data_frame(
        self, batch_name, data_frame, file_timestmp, model
    ):
        report = self._reports_use_case.generate_report(
            model, batch_name, file_timestmp, data_frame
        )
        self._reports_use_case.save_report(report)
        self._overall_reports_use_case.generate_overall_report(report)

    def fetch_data_frame(self, file_url: str):
        return pandas.read_csv(
            s3.open(
                file_url,
                mode="rb",
            )
        )

    def get_batch_statistics(self, batch_name, model):
        return self._overall_reports_use_case.calculate_batch_stats(
            model.name,
            model.version,
            batch_name,
        )

    def batch_statistics_to_proto(self, batch_stat: BatchStatistics):
        return GBatchStatistics(
            sus_ratio=batch_stat.sus_ratio,
            sus_verdict=batch_stat.sus_verdict,
            fail_ratio=batch_stat.fail_ratio,
        )

    def training_overall_report_exists(self, model: Model):
        return (
            self._overall_reports_use_case.get_report(
                model.name, model.version, "training"
            )
            is not None
        )

    def model_from_proto(self, message):
        res = MessageToDict(message, including_default_value_fields=True)
        contract = ModelSignature.parse_obj(res["signature"])
        model = Model(
            name=res["model"]["modelName"],
            version=res["model"]["modelVersion"],
            contract=contract,
        )
        return model
