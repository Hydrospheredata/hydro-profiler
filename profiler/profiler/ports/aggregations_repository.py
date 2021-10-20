from abc import ABC, abstractmethod
from typing import Dict, List, Any

from profiler.domain.model import Model
from profiler.domain.production_batch import ProductionBatch


class AggregationsRepository(ABC):
    @abstractmethod
    def get_list(self, model_name: str, model_version: int) -> List[Any]:
        pass

    @abstractmethod
    def save(self, model_name: str, model_version: int, batch_name: str, aggregation: str):
        pass
