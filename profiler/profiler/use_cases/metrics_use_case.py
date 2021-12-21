from pandas import DataFrame
import traceback
from profiler.domain.feature_metric import (
    CategoryMetrics,
    NumericalMetrics,
)
from profiler.domain.model_metrcis import MetricsByFeature, ModelMetrics
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
            metrics: MetricsByFeature = {}
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
                            feature: NumericalMetrics(
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
                    metrics.update({feature: CategoryMetrics(categories)})

            model_metrics = ModelMetrics(
                model_name=model.name,
                model_version=model.version,
                metrics_by_feature=MetricsByFeature(__root__=metrics),
            )

            self._metrics_repo.save(model_metrics)
            print(f"Metrics were stored for model {model.name}:{model.version}")
        except Exception as err:
            print(err)
            print(traceback.format_exc())


def second_precision(f: float) -> float:
    return float(format(f, ".2f"))
