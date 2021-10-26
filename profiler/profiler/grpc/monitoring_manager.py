import pandas
import threading
import grpc_tools
import grpc
import s3fs

from profiler.config.config import config

from profiler.domain.model import Model
from profiler.domain.model_signature import ModelSignature

from profiler.protobuf.monitoring_manager_pb2_grpc import (
    ModelCatalogServiceStub,
    DataStorageServiceStub,
)

from profiler.protobuf.monitoring_manager_pb2 import (
    GetModelUpdatesRequest,
    GetInferenceDataUpdatesRequest,
)

from profiler.use_cases.metrics_use_case import MetricsUseCase
from profiler.use_cases.report_use_case import ReportUseCase

s3 = s3fs.S3FileSystem(client_kwargs={"endpoint_url": config.minio_endpoint})


class MonitoringDataSubscriber:
    _metrics_use_case: MetricsUseCase
    _reports_use_case: ReportUseCase
    channel: grpc.Channel
    data_stub: DataStorageServiceStub
    model_stub: ModelCatalogServiceStub

    def __init__(
        self,
        channel: grpc.Channel,
        metrics_use_case: MetricsUseCase,
        reports_use_case: ReportUseCase,
    ):
        self.channel = channel
        self._metrics_use_case = metrics_use_case
        self._reports_use_case = reports_use_case
        self.data_stub = DataStorageServiceStub(self.channel)
        self.model_stub = ModelCatalogServiceStub(self.channel)

    def watch_inference_data(self):
        req = GetInferenceDataUpdatesRequest(plugin_id="profiler_plugin")
        for response in self.data_stub.GetInferenceDataUpdates(req):
            print("Prishli dannye")
            print(response)
            contract = ModelSignature.parse_obj(response.signature)
            model = Model(
                name=response.model, version=response.model, contract=contract
            )
            inference_data = pandas.read_csv(
                s3.open(
                    response.inference_data_objs[0],
                    mode="rb",
                )
            )

            # TODO: extract name from inference data file name
            self._reports_use_case.generate_report(
                model=model, batch_name="name", df=inference_data
            )

            # for inference_data_url in response.inference_data_objs:
            #   df = pandas.read_csv(inference_data_url)
            # report use case

    def watch_models(self):
        req = GetModelUpdatesRequest(plugin_id="profiler_plugin")
        for response in self.model_stub.GetModelUpdates(req):
            training_data_url = response.training_data_objs[0]
            print("Prishla model")
            print(training_data_url)
            contract = ModelSignature.parse_obj(response.signature)
            model = Model(
                name=response.model, version=response.model, contract=contract
            )
            training_df = pandas.read_csv(
                s3.open(
                    training_data_url,
                    mode="rb",
                )
            )

            self._metrics_use_case.generate_metrics(model, training_df)

    def start_watching(self):
        inference_data_thread = threading.Thread(target=self.watch_inference_data())
        inference_data_thread.daemon = True
        inference_data_thread.start()

        models_thread = threading.Thread(target=self.watch_models())
        models_thread.daemon = True
        models_thread.start()
