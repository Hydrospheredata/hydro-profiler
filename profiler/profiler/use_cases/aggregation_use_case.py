from profiler.domain.aggregation import Aggregation, AggregationBatch
from profiler.domain.model_report import ModelReport
from profiler.ports.aggregations_repository import AggregationsRepository
from profiler.ports.models_repository import ModelsRepository


class AggregationUseCase:
    _repo: AggregationsRepository
    _models_repo: ModelsRepository

    def __init__(
        self,
        repo: AggregationsRepository,
        models_repo: ModelsRepository,
    ) -> None:
        self._repo = repo
        self._models_repo = models_repo

    def get(self, model_name: str, model_version: int) -> Aggregation:
        model = self._models_repo.get_by_name(model_name, model_version)
        agg = self._repo.get_aggregation(model_name, model_version)
        features = [x.name for x in model.contract.merged_features()]
        agg.features = features
        return agg

    def generate_aggregation(
        self,
        report: ModelReport,
    ):
        batch_name = report.batch_name
        file_timestamp = report.file_timestamp

        batch_aggregation = AggregationBatch(
            model_name=report.model_name,
            model_version=report.model_version,
            rows_count=len(report.report.__root__),
            batch_name=batch_name,
            file_timestamp=file_timestamp,
            feature_overall=report.features_overall,
        )

        self._repo.save(batch_aggregation)
