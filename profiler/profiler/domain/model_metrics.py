class ModelMetrics:
    def __init__(self, model_name, model_version, metric_by_feature):
        self.model_name = model_name
        self.model_version = model_version
        self.metrics_by_feature = metric_by_feature
