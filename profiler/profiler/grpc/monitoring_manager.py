import pandas
import threading
import grpc
import s3fs
from google.protobuf.json_format import MessageToDict
from urllib.parse import urlparse
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
        init_req = GetInferenceDataUpdatesRequest.InitialRequest(
            plugin_id="profiler_plugin"
        )
        req = GetInferenceDataUpdatesRequest(init=init_req)
        reqs = iter([req])
        for response in self.data_stub.GetInferenceDataUpdates(reqs):
            print("Got inference data")
            res = MessageToDict(response)

            contract = ModelSignature.parse_obj(res["signature"])

            model = Model(
                name=res["model"]["modelName"],
                version=res["model"]["modelVersion"],
                contract=contract,
            )
            inference_data = pandas.read_csv(
                s3.open(
                    response.inference_data_objs[0],
                    mode="rb",
                )
            )

            pars = urlparse(response.inference_data_objs[0])
            name = str(pars.path.split("/")[-1])
            self._reports_use_case.generate_report(
                model=model, batch_name=name, df=inference_data
            )

    def watch_models(self):
        req = GetModelUpdatesRequest(plugin_id="profiler_plugin")
        for response in self.model_stub.GetModelUpdates(req):
            print("Got model")
            training_data_url = response.training_data_objs[0]
            res = MessageToDict(response)

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

    def start_watching(self):
        print("Start watching...")
        inference_data_thread = threading.Thread(target=self.watch_inference_data)
        inference_data_thread.daemon = True
        inference_data_thread.start()

        models_thread = threading.Thread(target=self.watch_models)
        models_thread.daemon = True
        models_thread.start()
