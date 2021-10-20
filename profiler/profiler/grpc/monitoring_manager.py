import pandas

from profiler.protobuf.monitoring_manager_pb2_grpc import ModelCatalogServiceStub, DataStorageServiceStub
from profiler.protobuf.monitoring_manager_pb2 import GetModelUpdatesRequest, GetInferenceDataUpdatesRequest, ModelSignature



class MonitoringDataSubscriber():
    @staticmethod
    def model_stub() -> ModelCatalogServiceStub:
        return ModelCatalogServiceStub("")

    @staticmethod
    def data_stub() -> DataStorageServiceStub:
        return DataStorageServiceStub("")

    def inference_data(self):
        req = GetInferenceDataUpdatesRequest()
        for response in self.data_stub().GetInferenceDataUpdates(req):
            model = response.model
            signature = response.signature
            inference_data_url = response.inference_data_objs[0]

            for inference_data_url in response.inference_data_objs:
                df = pandas.read_csv(inference_data_url)
                # report use case

    def models(self):
        req = GetModelUpdatesRequest("profile_plugin")
        for response in self.model_stub().GetModelUpdates(req):
            model = response.model
            signature: ModelSignature = response.signature
            training_data_url = response.training_data_objs[0]
            df = pandas.read_csv(training_data_url)
            # metrics_use_case

