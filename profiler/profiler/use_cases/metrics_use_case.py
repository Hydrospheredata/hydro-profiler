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
                    perc_25 = desc["25%"]
                    perc_75 = desc["75%"]
                    perc_01 = t_df[feature].quantile(0.01)
                    perc_99 = t_df[feature].quantile(0.99)

                    metrics.update(
                        {
                            feature: [
                                {
                                    "type": MetricType.MIN_MAX.value,
                                    "config": MinMaxMetric(min=min, max=max).dict(),
                                },
                                {
                                    "type": MetricType.PERCENTILE.value,
                                    "config": PercentileMetric(
                                        perc_01=perc_01, perc_99=perc_99
                                    ).dict(),
                                },
                                {
                                    "type": MetricType.IQR.value,
                                    "config": IQRMetric(
                                        perc_25=perc_25, perc_75=perc_75
                                    ).dict(),
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
                                    "config": IncludeMetric(
                                        categories=categories
                                    ).dict(),
                                }
                            ]
                        }
                    )
            self._metrics_repo.save(model, metrics)
            print(f"Metrics were stored for model {model.name}:{model.version}")
        except FileExistsError as err:
            print(err)
