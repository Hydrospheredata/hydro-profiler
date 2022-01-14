from typing import Dict
from pandas import DataFrame
import traceback
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

    def generate_metrics(self, model: Model, t_df: DataFrame):
        print("generate metrics")
        try:
            metrics: Dict[str, MetricConfig] = {}
            for field in model.contract.merged_features():
                feature = field.name
                if field.profile == DataProfileType.NUMERICAL:
                    desc = t_df[feature].describe()
                    min = desc["min"]
                    max = desc["max"]
                    perc_25 = second_precision(desc["25%"])
                    perc_75 = second_precision(desc["75%"])
                    perc_01 = second_precision(t_df[feature].quantile(0.01))
                    perc_99 = second_precision(t_df[feature].quantile(0.99))

                    metrics.update(
                        {
                            feature: NumericalMetricConfig(
                                min=min,
                                max=max,
                                perc_01=perc_01,
                                perc_25=perc_25,
                                perc_75=perc_75,
                                perc_99=perc_99,
                            )
                        }
                    )
                elif field.profile == DataProfileType.CATEGORICAL:
                    categories = t_df[feature].unique().tolist()
                    metrics.update({feature: CategoricalMetricConfig(categories)})
                else:
                    print(f"Unsupported profile type {field.profile}")
            model_metrics = ModelMetrics(
                model.name,
                model.version,
                metrics,
            )

            self._metrics_repo.save(model_metrics)
            print(f"Metrics were stored for model {model.name}:{model.version}")
        except Exception as err:
            print(err)
            print(traceback.format_exc())


def second_precision(f: float) -> float:
    return float(format(f, ".2f"))
