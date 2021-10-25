import pandas
import threading
import grpc_tools

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


class MonitoringDataSubscriber:
    _metrics_use_case: MetricsUseCase
    _reports_use_case: ReportUseCase

    def __init__(
        self, metrics_use_case: MetricsUseCase, reports_use_case: ReportUseCase
    ):
        self._metrics_use_case = metrics_use_case
        self._reports_use_case = reports_use_case

    @staticmethod
    def model_stub() -> ModelCatalogServiceStub:
        return ModelCatalogServiceStub("")

    @staticmethod
    def data_stub() -> DataStorageServiceStub:
        return DataStorageServiceStub("")

    def watch_inference_data(self):
        req = GetInferenceDataUpdatesRequest()
        for response in self.data_stub().GetInferenceDataUpdates(req):
            contract = ModelSignature.parse_obj(response.signature)
            model = Model(
                name=response.model, version=response.model, contract=contract
            )
            inference_data = pandas.read_csv(response.inference_data_objs[0])

            # TODO: extract name from inference data file name
            self._reports_use_case.generate_report(
                model=model, batch_name="name", df=inference_data
            )

            # for inference_data_url in response.inference_data_objs:
            #   df = pandas.read_csv(inference_data_url)
            # report use case

    def watch_models(self):
        req = GetModelUpdatesRequest("profile_plugin")
        for response in self.model_stub().GetModelUpdates(req):
            training_data_url = response.training_data_objs[0]

            contract = ModelSignature.parse_obj(response.signature)
            model = Model(
                name=response.model, version=response.model, contract=contract
            )
            training_df = pandas.read_csv(training_data_url)

            self._metrics_use_case.generate_metrics(model, training_df)

    def start_watching(self):
        inference_data_thread = threading.Thread(target=self.watch_inference_data())
        inference_data_thread.daemon = True
        inference_data_thread.start()

        models_thread = threading.Thread(target=self.watch_models())
        models_thread.daemon = True
        models_thread.start()
