from typing import List
from profiler.domain.aggregation import Aggregation, AggregationBatch
from profiler.ports.aggregations_repository import AggregationsRepository


class LocalAggregationsRepository(AggregationsRepository):
    aggregations: List[AggregationBatch] = []

    def get_aggregation(self, model_name: str, model_version: int) -> Aggregation:

        batches = [
            x
            for x in self.aggregations
            if x.model_name == model_name and model_version == model_version
        ]

        return Aggregation(
            model_name=model_name, model_version=model_version, batches=batches
        )

    def save(self, aggregation: Aggregation):
        self.aggregations.append(aggregation)
