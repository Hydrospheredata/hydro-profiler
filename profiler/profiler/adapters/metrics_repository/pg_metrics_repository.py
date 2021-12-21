from typing import Dict, List
from profiler.domain.model_metrcis import MetricsByFeature, ModelMetrics

from profiler.domain.feature_metric import BaseMetric, parse_metric
from profiler.ports.metrics_repository import MetricsRepository
from profiler.db.pg_engine import engine
from sqlalchemy import text
import json


class PgMetricsRepository(MetricsRepository):
    def all(self) -> Dict[str, Dict[str, List[BaseMetric]]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM metrics"))
            return result.all()

    def by_name(self, name: str, version: int) -> ModelMetrics:
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM metrics WHERE model_name=:name AND model_version=:version"
                ).bindparams(name=name, version=version),
            ).fetchone()

            (name, version, metrics) = result
            parsed = json.loads(metrics)

            res = ModelMetrics(
                model_name=name,
                model_version=version,
                metrics_by_feature=MetricsByFeature(
                    __root__={
                        feature: parse_metric(metrics)
                        for feature, metrics in parsed.items()
                    }
                ),
            )
            return res

    def save(self, model_metrics: ModelMetrics):
        with engine.connect() as conn:
            query = text(
                "INSERT INTO metrics VALUES (:model_name, :model_version, :metrics)"
            ).bindparams(
                model_name=model_metrics.model_name,
                model_version=model_metrics.model_version,
                metrics=model_metrics.metrics_by_feature.json(),
            )
            conn.execute(query)
