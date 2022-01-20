from datetime import datetime
import logging

from pandas.core.frame import DataFrame
from profiler.domain.batch_report import BatchReport
from profiler.domain.column_processor import (
    process_categorical_column,
    process_numerical_column,
)
from profiler.domain.errors import GenerateReportError
from profiler.domain.model import Model

from profiler.domain.model_signature import DataProfileType
from profiler.ports.models_repository import ModelsRepository
from profiler.ports.reports_repository import ReportsRepository

from profiler.use_cases.aggregation_use_case import AggregationUseCase
from profiler.use_cases.metrics_use_case import MetricsUseCase


class ReportUseCase:
    _models_repo: ModelsRepository
    _reports_repo: ReportsRepository
    _metrics_use_case: MetricsUseCase
    _aggregation_use_case: AggregationUseCase

    def __init__(
        self,
        models_repo: ModelsRepository,
        reports_repo: ReportsRepository,
        metrics_use_case: MetricsUseCase,
        agg_use_case: AggregationUseCase,
    ) -> None:
        self._models_repo = models_repo
        self._metrics_use_case = metrics_use_case
        self._reports_repo = reports_repo
        self._aggregation_use_case = agg_use_case

    def get_report(self, model_name: str, model_version: int, batch_name: str):
        return self._reports_repo.get_report(model_name, model_version, batch_name)

    def save_report(self, report: BatchReport):
        self._reports_repo.save(report)
        self._aggregation_use_case.generate_aggregation(report)

    def generate_report(
        self, model: Model, batch_name: str, file_timestamp: datetime, df: DataFrame
    ) -> BatchReport:
        try:
            metrics_by_feature = self._metrics_use_case.get_by_model(
                model
            ).metrics_by_feature
            model_fields = model.contract.merged_features()

            batch_report = BatchReport(
                model.name, model.version, batch_name, file_timestamp, df.shape[0]
            )

            for model_field in model_fields:
                feature_name = model_field.name
                profile = model_field.profile

                if profile not in [
                    DataProfileType.NUMERICAL,
                    DataProfileType.CATEGORICAL,
                ]:
                    logging.warning(f"Could not find feature {feature_name} in batch")
                    continue

                try:
                    metric_config = metrics_by_feature[feature_name]
                    if model_field.profile == DataProfileType.NUMERICAL:
                        result = process_numerical_column(
                            feature_name, df[feature_name], metric_config
                        )
                    elif model_field.profile == DataProfileType.CATEGORICAL:
                        result = process_categorical_column(
                            feature_name, df[feature_name], metric_config
                        )
                except KeyError:
                    logging.warning(
                        f"Didn't find metrics for field {feature_name.capitalize()}. SKIP"
                    )
                except Exception:
                    logging.warning(
                        f"Could'n calculate checks for {model.name}:{model.version}/{batch_name}/{feature_name}",
                        exc_info=True,
                    )
                    continue
                else:
                    batch_report.process_column_report(result)

            return batch_report
        except Exception as e:
            raise GenerateReportError(
                f"Report for {model.name}:{model.version}/{batch_name} was not generated",
                e,
            )
