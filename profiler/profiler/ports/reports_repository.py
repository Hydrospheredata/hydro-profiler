from abc import ABC, abstractmethod
from datetime import datetime


class ReportsRepository(ABC):
    @abstractmethod
    def get_report(self, model_name: str, model_version: int, batch_name: str):
        pass

    @abstractmethod
    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        file_timestamp: datetime,
        report: list,
    ):
        pass
