from abc import ABC, abstractmethod
from profiler.domain.aggregation import Aggregation, AggregationBatch


class AggregationsRepository(ABC):
    @abstractmethod
    def get_aggregation(self, model_name: str, model_version: int) -> Aggregation:
        pass

    @abstractmethod
    def save(self, aggregation_batch: AggregationBatch):
        pass
