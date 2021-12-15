from typing import Dict, List

from profiler.domain.model import Model
from profiler.domain.feature_metric import BaseMetric, recognize_metric
from profiler.ports.metrics_repository import MetricsRepository
from profiler.db.pg_engine import engine
from sqlalchemy import text
import json


class PgMetricsRepository(MetricsRepository):
    def all(self) -> Dict[str, Dict[str, List[BaseMetric]]]:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM metrics"))
            return result.all()

    def by_name(self, name: str, version: int) -> Dict[str, List[BaseMetric]]:
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT metrics FROM metrics WHERE model_name=:name AND model_version=:version"
                ).bindparams(name=name, version=version),
            ).fetchone()

            parsed = json.loads(result[0])
            r = {}

            for feature, metrics in parsed.items():
                r.update({feature: list(map(recognize_metric, metrics))})

            return r

    def save(self, model: Model, metrics: Dict[str, List[BaseMetric]]):
        with engine.connect() as conn:
            query = text(
                "INSERT INTO metrics VALUES (:model_name, :model_version, :metrics)"
            ).bindparams(
                model_name=model.name,
                model_version=model.version,
                metrics=json.dumps(metrics),
            )
            conn.execute(query)
