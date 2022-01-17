from typing import List
from abc import ABC, abstractmethod

from profiler.domain.model_metrics import ModelMetrics


class MetricsRepository(ABC):
    @abstractmethod
    def all(self) -> List[ModelMetrics]:
        pass

    @abstractmethod
    def by_name(self, name: str, version: int) -> ModelMetrics:
        pass

    @abstractmethod
    def save(self, model_metrics: ModelMetrics) -> None:
        pass
