from profiler.domain.feature_metric import (
    BaseMetric,
    IQRMetric,
    IncludeMetric,
    MetricType,
    MinMaxMetric,
    PercentileMetric,
)
from profiler.domain.metric_spec import MetricSpec
from typing import List, Dict
from profiler.ports.metrics_repository import MetricsRepository
from profiler.domain.model import Model


class LocalMetricsRepository(MetricsRepository):
    __metrics: Dict[str, Dict[str, List[BaseMetric]]] = {}

    def all(self):
        return self.__metrics

    def by_name(self, model_name: str) -> Dict[str, List[BaseMetric]]:
        r = {}

        def recognizeMetric(x):
            if x["type"] == MetricType.MIN_MAX:
                return MinMaxMetric.parse_obj(x["config"])
            elif x["type"] == MetricType.IN:
                return IncludeMetric.parse_obj(x["config"])
            elif x["type"] == MetricType.IQR:
                return IQRMetric.parse_obj(x["config"])
            elif x["type"] == MetricType.PERCENTILE:
                return PercentileMetric.parse_obj(x["config"])
            else:
                return None

        for feature, metrics in self.__metrics[model_name].items():
            r.update({feature: list(map(recognizeMetric, metrics))})

        return r

    def save(self, model: Model, metrics: Dict[str, List[MetricSpec]]):
        self.__metrics.update({model.name: metrics})
