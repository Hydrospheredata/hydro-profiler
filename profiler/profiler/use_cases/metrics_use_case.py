from pandas import DataFrame

from profiler.domain.feature_metric import (
    IQRMetric,
    IncludeMetric,
    MinMaxMetric,
    PercentileMetric,
    MetricType,
)
from profiler.domain.model_signature import DataProfileType
from profiler.ports.metrics_repository import MetricsRepository
from profiler.domain.model import Model


class MetricsUseCase:
    _metrics_repo: MetricsRepository

    def __init__(self, metrics_repo: MetricsRepository):
        self._metrics_repo = metrics_repo

    def generate_metrics(self, model: Model, t_df: DataFrame):
        try:
            metrics = {}
            for field in model.contract.merged_features():
                feature = field.name
                if field.profile == DataProfileType.NUMERICAL:
                    desc = t_df[feature].describe()
                    min = desc["min"]
                    max = desc["max"]
                    perc_25 = float(format(desc["25%"], ".2f"))
                    perc_75 = float(format(desc["75%"], ".2f"))
                    perc_01 = float(format(t_df[feature].quantile(0.01), ".2f"))
                    perc_99 = float(format(t_df[feature].quantile(0.99), ".2f"))

                    metrics.update(
                        {
                            feature: [
                                {
                                    "type": MetricType.MIN_MAX.value,
                                    "config": MinMaxMetric(min, max).__dict__,
                                },
                                {
                                    "type": MetricType.PERCENTILE.value,
                                    "config": PercentileMetric(
                                        perc_01, perc_99
                                    ).__dict__,
                                },
                                {
                                    "type": MetricType.IQR.value,
                                    "config": IQRMetric(perc_25, perc_75).__dict__,
                                },
                            ]
                        }
                    )
                elif field.profile == DataProfileType.CATEGORICAL:
                    categories = t_df[feature].unique().tolist()
                    metrics.update(
                        {
                            feature: [
                                {
                                    "type": MetricType.IN.value,
                                    "config": IncludeMetric(categories).__dict__,
                                }
                            ]
                        }
                    )
            self._metrics_repo.save(model, metrics)
            print(f"Metrics were stored for model {model.name}:{model.version}")
        except FileExistsError as err:
            print(err)
