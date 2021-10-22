from profiler.domain.overall import Overall, merge_overall
from profiler.ports.reports_repository import ReportsRepository
from profiler.domain.model import Model
from profiler.ports.metrics_repository import MetricsRepository
from profiler.ports.models_repository import ModelsRepository
from profiler.use_cases.aggregation_use_case import AggregationUseCase

from pandas.core.frame import DataFrame
from functools import reduce


class ReportUseCase:
    _models_repo: ModelsRepository
    _metrics_repo: MetricsRepository
    _reports_repo: ReportsRepository
    _aggregation_use_case: AggregationUseCase

    def __init__(
        self,
        models_repo: ModelsRepository,
        metrics_repo: MetricsRepository,
        reports_repo: ReportsRepository,
        agg_use_case: AggregationUseCase
    ) -> None:
        self._models_repo = models_repo
        self._metrics_repo = metrics_repo
        self._reports_repo = reports_repo
        self._aggregation_use_case = agg_use_case

    def get_report(self, model_name: str, model_version: int, batch_name: str):
        return self._reports_repo.get_report(model_name=model_name, model_version=model_version, batch_name=batch_name)

    def generate_report(self, model: Model, batch_name: str, df: DataFrame):
        metrics_dict = self._metrics_repo.by_name(name=model.name, version=model.version)

        report = []

        for index, row in df.iterrows():
            result = {
                "_id": index,
                "_raw_checks": {},
                "_feature_overall": {},
            }
            raw_metrics = {}
            feature_overall = {}
            feature_overall_score = {}
            row_overall = Overall()

            for feature, metrics in metrics_dict.items():
                checks = list(
                    map(
                        lambda metric: metric.check(row[feature]),
                        metrics,
                    )
                )

                _feature_overall = reduce(calculate_overall, checks, Overall())
                _feature_overall_score = reduce(calculate_feature_score, checks, Overall())

                row_overall = merge_overall(row_overall, _feature_overall)

                raw_metrics.update({feature: checks})
                feature_overall.update({feature: _feature_overall.dict()})
                feature_overall_score.update({feature: _feature_overall_score.dict()})

            result.update(
                {
                    "_raw_checks": raw_metrics,
                    "_feature_overall": feature_overall,
                    "_row_overall": row_overall.dict(),
                    "_feature_overall_score": feature_overall_score
                }
            )
            report.append(result)

        self._reports_repo.save(model_name=model.name, model_version=model.version, batch_name=batch_name, report=report)
        self._aggregation_use_case.generate_aggregation(model=model, batch_name=batch_name, report=report)
        print("report was generated and stored")

def calculate_overall(over: Overall, check):
    status = check["status"]
    if status == "failed":
        over.add_fail()
    elif status == "suspicious":
        over.add_suspicious()
    else:
        over.add_succeed()
    return over


def calculate_feature_score(over: Overall, check) -> Overall:
    status = check["status"]
    count_score = check["count_score"]

    if count_score:
        if status == "failed":
            over.add_fail()
        else:
            over.add_succeed()
    return over
