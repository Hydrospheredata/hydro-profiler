from abc import ABC, abstractmethod
from typing import Dict


class ReportsRepository(ABC):
    @abstractmethod
    def get_report(self, model_name: str, model_version: int, batch_name: str):
        pass

    @abstractmethod
    def save(self, model_name: str, model_version: int, batch_name: str, report: Dict[str, any]):
        pass
