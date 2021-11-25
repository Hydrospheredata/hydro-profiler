import logging
import queue
import threading

import pandas
import s3fs
from google.protobuf.json_format import MessageToDict
from profiler.config.config import config
from profiler.domain.batch_statistics import BatchStatistics
from profiler.domain.model import Model
from profiler.domain.model_signature import ModelSignature
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

import grpc

from profiler.utils.inference_url_parser import extract_file_name

s3 = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": config.minio_endpoint}, use_listings_cache=False
)


class MonitoringDataSubscriber:
    _metrics_use_case: MetricsUseCase
    _reports_use_case: ReportUseCase
    _overall_reports_use_case: OverallReportsUseCase
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
    ):
        self.channel = channel
        self._metrics_use_case = metrics_use_case
        self._reports_use_case = reports_use_case
        self._overall_reports_use_case = overall_reports_use_case
        self.data_stub = DataStorageServiceStub(self.channel)
        self.model_stub = ModelCatalogServiceStub(self.channel)

    def watch_inference_data(self):
        ack_queue = queue.Queue(100)
        init_req = GetInferenceDataUpdatesRequest(plugin_id=self.plugin_name)
        ack_queue.put(init_req)

        def qgetter():
            item = ack_queue.get()
            print("Sending message to the manager")
            return item

        reqs = iter(qgetter, None)
        for response in self.data_stub.GetInferenceDataUpdates(reqs):
            try:
                print("Got inference data")

                res = MessageToDict(response, including_default_value_fields=True)

                contract = ModelSignature.parse_obj(res["signature"])

                model = Model(
                    name=res["model"]["modelName"],
                    version=res["model"]["modelVersion"],
                    contract=contract,
                )

                print("Try to find overall report for training data")
                training_overall_report = self._overall_reports_use_case.get_report(
                    model.name, model.version, "training"
                )
                print(f"Train rep: {training_overall_report}")

                if training_overall_report:
                    for data_obj in response.inference_data_objs:
                        # TODO(bulat): need to use data_obj timestamp somewhere
                        inference_data = pandas.read_csv(
                            s3.open(
                                data_obj.key,
                                mode="rb",
                            )
                        )

                        batch_name = extract_file_name(data_obj.key)

                        report = self._reports_use_case.generate_report(
                            model, batch_name, inference_data
                        )
                        self._reports_use_case.save_report(model, batch_name, report)

                        self._overall_reports_use_case.generate_overall_report(
                            model.name, model.version, batch_name, report
                        )

                        batch_stats: BatchStatistics = (
                            self._overall_reports_use_case.calculate_batch_stats(
                                model.name,
                                model.version,
                                batch_name,
                            )
                        )

                        print("Batch statistic")
                        print(batch_stats)

                        resp = GetInferenceDataUpdatesRequest(
                            plugin_id=self.plugin_name,
                            ack=AnalyzedAck(
                                model_name=model.name,
                                model_version=model.version,
                                inference_data_obj=data_obj,
                                batch_stats=GBatchStatistics(
                                    sus_ratio=batch_stats.sus_ratio,
                                    sus_verdict=batch_stats.sus_verdict,
                                    fail_ratio=batch_stats.fail_ratio,
                                ),
                            ),
                        )

                        ack_queue.put(resp)
                else:
                    print("Could not find overall report for training data")
            except Exception:
                logging.exception("Error while handling inference data event")

    def watch_models(self):
        req = GetModelUpdatesRequest(plugin_id="profiler_plugin")
        for response in self.model_stub.GetModelUpdates(req):
            print("Got model request")
            training_data_url = response.training_data_objs[0].key
            print(f"Training data url: training_data_url")

            res = MessageToDict(response, including_default_value_fields=True)

            contract = ModelSignature.parse_obj(res["signature"])

            model = Model(
                name=res["model"]["modelName"],
                version=res["model"]["modelVersion"],
                contract=contract,
            )
            training_df = pandas.read_csv(
                s3.open(
                    training_data_url,
                    mode="rb",
                )
            )

            self._metrics_use_case.generate_metrics(model, training_df)

            # generate report for training data
            report = self._reports_use_case.generate_report(
                model, "training", training_df
            )

            self._overall_reports_use_case.generate_overall_report(
                model_name=model.name,
                model_version=model.version,
                batch_name="training",
                report=report,
            )

    def start_watching(self):
        print("Start watching...")
        inference_data_thread = threading.Thread(target=self.watch_inference_data)
        inference_data_thread.daemon = True
        inference_data_thread.start()

        models_thread = threading.Thread(target=self.watch_models)
        models_thread.daemon = True
        models_thread.start()
