import logging
from typing import Dict
from pandas import DataFrame, Series

from profiler.domain.errors import GenerateMetricsError
from profiler.domain.metric_config import (
    CategoricalMetricConfig,
    MetricConfig,
    NumericalMetricConfig,
)
from profiler.domain.model_metrics import ModelMetrics
from profiler.domain.model_signature import DataProfileType
from profiler.ports.metrics_repository import MetricsRepository
from profiler.domain.model import Model


class MetricsUseCase:
    _metrics_repo: MetricsRepository

    def __init__(self, metrics_repo: MetricsRepository):
        self._metrics_repo = metrics_repo

    def get_by_model(self, model: Model):
        return self._metrics_repo.by_name(model.name, model.version)

    def process_numerical_column(self, series: Series):
        try:
            desc = series.describe()
            min = desc["min"]
            max = desc["max"]
            perc_25 = second_precision(desc["25%"])
            perc_75 = second_precision(desc["75%"])
            perc_01 = second_precision(series.quantile(0.01))
            perc_99 = second_precision(series.quantile(0.99))

            return NumericalMetricConfig(
                min=min,
                max=max,
                perc_01=perc_01,
                perc_25=perc_25,
                perc_75=perc_75,
                perc_99=perc_99,
            )
        except TypeError:
            raise

    def is_supproted_profile_type(self, profile_type: DataProfileType):
        return profile_type in [DataProfileType.NUMERICAL, DataProfileType.CATEGORICAL]

    def process_cateforical_column(self, series: Series):
        categories = series.unique().tolist()
        return CategoricalMetricConfig(categories)

    def generate_metrics(self, model: Model, t_df: DataFrame):
        try:
            logging.info(f"Generate metrics for {model.name}:{model.version}")
            metrics: Dict[str, MetricConfig] = {}

            for field in model.contract.merged_features():
                feature = field.name
                profile = field.profile
                dtype = field.dtype

                try:
                    series = t_df[feature]
                except Exception:
                    logging.warning(
                        f"Feature {feature} doesn't exist in trainig file. SKIP"
                    )
                    continue

                if not self.is_supproted_profile_type(profile):
                    logging.warning(
                        f"Unsupported profile type ({feature}, {profile}). SKIP"
                    )
                    continue

                try:
                    if profile == DataProfileType.NUMERICAL:
                        metric = self.process_numerical_column(series)
                    elif profile == DataProfileType.CATEGORICAL:
                        metric = self.process_cateforical_column(series)
                except Exception:
                    logging.exception(
                        f"Couldn't create metric for ({feature}, {profile}, {dtype})",
                        exc_info=True,
                    )
                    continue
                else:
                    metrics.update({feature: metric})

            model_metrics = ModelMetrics(
                model.name,
                model.version,
                metrics,
            )

            self._metrics_repo.save(model_metrics)
        except Exception as e:
            logging.exception("Error during creating metrics")
            raise GenerateMetricsError(
                f"Couldn't generate metrics report for {model.name}:{model.version}", e
            )


def second_precision(f: float) -> float:
    return float(format(f, ".2f"))
