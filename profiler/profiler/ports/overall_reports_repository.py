from abc import ABC, abstractmethod

from profiler.domain.overall_report import OverallReport


class OverallReportsRepository(ABC):
    @abstractmethod
    def get_overall_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        pass

    @abstractmethod
    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        suspicious_percent: float,
        failed_ratio: float,
    ) -> None:
        pass
