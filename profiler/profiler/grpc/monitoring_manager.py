import logging
import queue
import threading

import pandas
import s3fs
from google.protobuf.json_format import MessageToDict
from profiler.config.config import config
from profiler.domain.model import Model
from profiler.domain.model_signature import ModelSignature
from profiler.protobuf.monitoring_manager_pb2 import (
    AnalyzedAck,
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

s3 = s3fs.S3FileSystem(client_kwargs={"endpoint_url": config.minio_endpoint})


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

                for data_obj in response.inference_data_objs:
                    # TODO(bulat): need to use data_obj timestamp somewhere
                    inference_data = pandas.read_csv(
                        s3.open(
                            data_obj.key,
                            mode="rb",
                        )
                    )

                    report = self._reports_use_case.generate_report(
                        model=model, batch_name=data_obj.key, df=inference_data
                    )
                    # store report
                    self._reports_use_case.save_report(
                        model.name, model.version, data_obj.key, report
                    )

                    self._overall_reports_use_case.generate_overall_report(
                        model_name=model.name,
                        model_version=model.version,
                        batch_name=data_obj.key,
                        report=report,
                    )

                    batch_stats = self._overall_reports_use_case.calculate_batch_stats(
                        model_name=model.name,
                        model_version=model.version,
                        batch_name=data_obj.key,
                    )

                    resp = GetInferenceDataUpdatesRequest(
                        plugin_id=self.plugin_name,
                        ack=AnalyzedAck(
                            model_name=model.name,
                            model_version=model.version,
                            batch_stats=batch_stats,
                        ),
                    )

                    ack_queue.put(resp)
            except Exception:
                logging.exception("Error while handling inference data event")

    def watch_models(self):
        req = GetModelUpdatesRequest(plugin_id="profiler_plugin")
        for response in self.model_stub.GetModelUpdates(req):
            print("Got model")
            training_data_url = response.training_data_objs[0].key
            res = MessageToDict(response, including_default_value_fields=True)

            contract = ModelSignature.parse_obj(res["signature"])
            print(contract)

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

            # generate and store report for training data for Overall report
            report = self._reports_use_case.generate_report(
                model, "training", training_df
            )
            self._reports_use_case.save_report(
                model.name, model.version, "training", report
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
