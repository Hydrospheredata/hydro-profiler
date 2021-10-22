from typing import Dict

from profiler.domain.overall import Overall, merge_overall
from profiler.domain.model import Model
from profiler.domain.model_signature import ModelField
from profiler.ports.aggregations_repository import AggregationsRepository

from functools import reduce



def calculate_score(overall: Overall) -> float:
    return float(overall.succeed / overall.count)

class AggregationUseCase:
    _repo: AggregationsRepository

    def __init__(
        self,
        repo: AggregationsRepository,
    ) -> None:
        self._repo = repo

    def get(self, model_name: str, model_version: int):
        return self._repo.get_list(model_name=model_name, model_version=model_version)

    def generate_aggregation(self, model: Model, batch_name: str, report):
        def o(d: Dict[str, Overall], field: ModelField) -> Dict[str, Overall]:
            d.update({field.name: Overall()})
            return d

        feature_overall = reduce(o, model.contract.merged_features(), {})

        for row in report:
            score_by_feature = row['_feature_overall_score']
            for feature, overall in score_by_feature.items():
                feature_overall.update({feature: merge_overall(feature_overall[feature], Overall.parse_obj(overall))})

        for feat, over in feature_overall.items():
            feature_overall.update({feat: calculate_score(over)})

        agg = {
            'keys': list(map(lambda m: m.name, model.contract.merged_features())),
            'scores': feature_overall
        }

        self._repo.save(model_name=model.name, model_version=model.version, batch_name=batch_name, aggregation=agg)


