from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any


class AggregationsRepository(ABC):
    @abstractmethod
    def get_list(self, model_name: str, model_version: int) -> List[Any]:
        pass

    @abstractmethod
    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        file_timestamp: datetime,
        aggregation: str,
    ):
        pass
