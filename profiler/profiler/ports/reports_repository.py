from abc import ABC, abstractmethod
from profiler.domain.batch_report import BatchReport


class ReportsRepository(ABC):
    @abstractmethod
    def get_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> BatchReport:
        pass

    @abstractmethod
    def save(self, model_report: BatchReport):
        pass
