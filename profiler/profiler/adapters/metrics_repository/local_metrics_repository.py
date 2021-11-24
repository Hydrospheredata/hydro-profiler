from profiler.domain.feature_metric import (
    BaseMetric,
    recognize_metric,
)
from typing import List, Dict, Any
from profiler.ports.metrics_repository import MetricsRepository
from profiler.domain.model import Model


class LocalMetricsRepository(MetricsRepository):
    __metrics: Dict[str, Dict[str, List[BaseMetric]]] = {}

    def all(self):
        return self.__metrics

    def by_name(self, model_name: str) -> Dict[str, List[BaseMetric]]:
        r = {}

        for feature, metrics in self.__metrics[model_name].items():
            r.update({feature: list(map(recognize_metric, metrics))})

        return r

    def save(self, model: Model, metrics: Dict[str, List[Any]]):
        self.__metrics.update({model.name: metrics})
