import json
from profiler.domain.feature_metric import (
    parse_metric,
)
from typing import List, Dict, Any
from profiler.ports.metrics_repository import MetricsRepository
from profiler.domain.model import Model

from profiler.db.sqlite_context_manager import SqliteContextManager


class SqliteMetricsRepository(MetricsRepository):
    def all(self):
        with SqliteContextManager() as cur:
            return cur.execute("SELECT * FROM metrics")

    def by_name(self, name: str, version: int):
        with SqliteContextManager() as cur:
            cur.execute(
                "SELECT metrics FROM metrics WHERE model_name=? AND model_version=?",
                (
                    name,
                    version,
                ),
            )
            res = cur.fetchone()[0]
            parsed = json.loads(res)

            return {
                feature: list(map(parse_metric, metrics))
                for feature, metrics in parsed.items()
            }

    def save(self, model: Model, metrics: Dict[str, List[Any]]):
        with SqliteContextManager() as cur:
            cur.execute(
                "INSERT INTO metrics VALUES (?, ?, ?)",
                (model.name, model.version, json.dumps(metrics)),
            )
