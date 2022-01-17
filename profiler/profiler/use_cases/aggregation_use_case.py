from profiler.domain.aggregation import Aggregation, AggregationBatch
from profiler.domain.batch_report import BatchReport
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
        report: BatchReport,
    ):
        batch_name = report.batch_name
        file_timestamp = report.file_timestamp

        batch_aggregation = AggregationBatch(
            report.model_name,
            report.model_version,
            batch_name,
            file_timestamp,
            report.features_statistics,
        )

        self._repo.save(batch_aggregation)
