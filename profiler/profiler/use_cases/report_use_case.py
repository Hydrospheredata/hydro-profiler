from datetime import datetime
from typing import List

from pandas.core.frame import DataFrame
from profiler.domain.feature_metric import CheckType
from profiler.domain.model import Model
from profiler.domain.model_report import (
    DataRowReport,
    DataRowStatus,
    FeatureUnsucceedCalculator,
    FeaturesOverall,
    ModelReport,
    Report,
)
from profiler.domain.model_signature import DataProfileType
from profiler.ports.metrics_repository import MetricsRepository
from profiler.ports.models_repository import ModelsRepository
from profiler.ports.reports_repository import ReportsRepository

from profiler.use_cases.aggregation_use_case import AggregationUseCase


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
        agg_use_case: AggregationUseCase,
    ) -> None:
        self._models_repo = models_repo
        self._metrics_repo = metrics_repo
        self._reports_repo = reports_repo
        self._aggregation_use_case = agg_use_case

    def get_report(self, model_name: str, model_version: int, batch_name: str):
        return self._reports_repo.get_report(
            model_name=model_name, model_version=model_version, batch_name=batch_name
        )

    def save_report(self, model_report: ModelReport):
        self._reports_repo.save(model_report)
        self._aggregation_use_case.generate_aggregation(model_report)

    def generate_report(
        self, model: Model, batch_name: str, file_timestamp: datetime, df: DataFrame
    ) -> ModelReport:
        print(f"Generate report for {model.name}:{model.version}")
        metrics = self._metrics_repo.by_name(name=model.name, version=model.version)
        print("metrics")

        metrics_by_feature = metrics.metrics_by_feature.__root__
        reports: List[DataRowReport] = []

        features = []
        for feature, metrics in metrics_by_feature.items():
            features.append(feature)
        print(features)
        features_unsucceed_calculator = FeatureUnsucceedCalculator(features)

        for index, row in df.iterrows():
            status = DataRowStatus.HEALTHY
            features_checks_results = {}

            for feature, metrics in metrics_by_feature.items():
                check_results = metrics.check(row[feature])
                features_checks_results[feature] = check_results

                some_failed = [x for x in check_results if x.status == CheckType.FAILED]

                some_susp = [
                    x for x in check_results if x.status == CheckType.SUSPICIOUS
                ]

                if some_failed:
                    features_unsucceed_calculator.add_failed(feature)
                    status = DataRowStatus.HAS_FAILED

                if some_susp and not some_failed:
                    features_unsucceed_calculator.add_suspicious(feature)

                if some_susp and status == DataRowStatus.HEALTHY:
                    status = DataRowStatus.HAS_SUSPICIOUS

            reports.append(
                DataRowReport(
                    id=index, features_checks=features_checks_results, status=status
                )
            )

        print("report generated")

        return ModelReport(
            model_name=model.name,
            model_version=model.version,
            batch_name=batch_name,
            file_timestamp=file_timestamp,
            report=Report(__root__=reports),
            features_overall=FeaturesOverall(
                __root__=features_unsucceed_calculator.get_result()
            ),
        )


def calculate_suspicious_percent(report: ModelReport):
    rows = report.report.__root__
    rows_count = len(rows)
    suspicious_rows = [x for x in rows if x.status == DataRowStatus.HAS_SUSPICIOUS]
    suspicious_count = len(suspicious_rows)

    if rows_count == 0 or suspicious_count == 0:
        return 0

    return (suspicious_count / rows_count) * 100


def calculate_failed_ratio(report):
    rows = report.report.__root__
    rows_count = len(rows)
    failed_rows = [x for x in rows if x.status == DataRowStatus.HAS_FAILED]
    failed_count = len(failed_rows)

    if rows_count == 0 or failed_count == 0:
        return 0

    return failed_count / rows_count
