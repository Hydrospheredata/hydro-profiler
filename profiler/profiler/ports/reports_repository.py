from abc import ABC, abstractmethod
from profiler.domain.model_report import ModelReport


class ReportsRepository(ABC):
    @abstractmethod
    def get_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> ModelReport:
        pass

    @abstractmethod
    def save(self, model_report: ModelReport):
        pass
