from typing import List
from profiler.domain.model_metrcis import ModelMetrics
from profiler.ports.metrics_repository import MetricsRepository


class LocalMetricsRepository(MetricsRepository):
    metrics: List[ModelMetrics] = []

    def all(self) -> List[ModelMetrics]:
        return self.metrics

    def by_name(self, name: str, version: int) -> ModelMetrics:
        result = [
            x
            for x in self.metrics
            if x.model_name == name and x.model_version == version
        ]

        return result[0]

    def save(self, model_metrics: ModelMetrics) -> None:
        return self.metrics.append(model_metrics)
