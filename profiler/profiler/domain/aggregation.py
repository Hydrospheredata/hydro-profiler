class AggregationBatch:
    def __init__(
        self, model_name, model_version, batch_name, file_timestamp, feature_statistics
    ):
        self.model_name = model_name
        self.model_version = model_version
        self.batch_name = batch_name
        self.file_timestamp = file_timestamp
        self.feature_statistics = feature_statistics


class Aggregation:
    def __init__(self, model_name, model_version, features, batches):
        self.model_name = model_name
        self.model_version = model_version
        self.features = features
        self.batches = batches
