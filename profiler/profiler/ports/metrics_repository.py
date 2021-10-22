from profiler.domain.feature_metric import BaseMetric
from profiler.domain.model import Model

from typing import List, Dict
from abc import ABC, abstractmethod


class MetricsRepository(ABC):
    @abstractmethod
    def all(self) -> Dict[str, Dict[str, List[BaseMetric]]]:
        pass

    @abstractmethod
    def by_name(self, name: str, version: int) -> Dict[str, List[BaseMetric]]:
        pass

    @abstractmethod
    def save(self, model: Model, metrics: Dict[str, List[BaseMetric]]):
        pass
