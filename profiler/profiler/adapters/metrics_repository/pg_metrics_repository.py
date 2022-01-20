import logging
from typing import Dict, List
from sqlalchemy import text
import json
from profiler.domain import EntityNotFoundError
from profiler.domain.errors import EntityWasNotStoredError

from profiler.domain.metric_config import MetricConfig, parse_config
from profiler.domain.model_metrics import ModelMetrics
from profiler.ports.metrics_repository import MetricsRepository
from profiler.db.pg_engine import engine
from profiler.utils.json_dumper import dumper


class PgMetricsRepository(MetricsRepository):
    def all(self) -> Dict[str, Dict[str, List[MetricConfig]]]:
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

            if result is None:
                raise EntityNotFoundError(f"Metrics for {name}{version} were not found")

            try:
                (name, version, metrics) = result
                parsed = json.loads(metrics)
                res = ModelMetrics(
                    model_name=name,
                    model_version=version,
                    metric_by_feature={
                        feature: parse_config(metrics)
                        for feature, metrics in parsed.items()
                    },
                )
                return res
            except Exception:
                logging.exception("Error during pasing config")

    def save(self, model_metrics: ModelMetrics):
        with engine.connect() as conn:
            try:
                model_name = model_metrics.model_name
                model_version = model_metrics.model_version

                query = text(
                    "INSERT INTO metrics VALUES (:model_name, :model_version, :metrics)"
                ).bindparams(
                    model_name=model_name,
                    model_version=model_version,
                    metrics=json.dumps(
                        model_metrics.metrics_by_feature, default=dumper
                    ),
                )
                conn.execute(query)
                logging.info(
                    f"Metrics were stored for model {model_name}:{model_version}"
                )
            except Exception as e:
                raise EntityWasNotStoredError(
                    f"Metrics for {model_name}{model_version} were not stored", e
                )
