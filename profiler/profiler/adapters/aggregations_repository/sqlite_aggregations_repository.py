import json
import sqlite3
from typing import Any, Dict

from profiler.ports.aggregations_repository import AggregationsRepository
from profiler.db.sqlite_context_manager import SqliteContextManager


class SqliteAggregationsRepository(AggregationsRepository):
    def get_list(self, model_name: str, model_version: int) -> Dict[str, Any]:
        with SqliteContextManager() as cur:
            cur.execute(
                "SELECT model_name, batch_name, aggregation FROM aggregations WHERE model_name=? AND model_version=?",
                (model_name, model_version),
            )
            db_rows = cur.fetchall()

            if len(db_rows) == 0:
                return {"features": [], "scores": []}
            else:
                features = []
                aggregates = []

                for model_name, batch_name, raw_aggregation in db_rows:
                    agg = json.loads(raw_aggregation)
                    features = agg["keys"]
                    aggregates.append(
                        {"batch_name": batch_name, "scores": agg["scores"]}
                    )

                return {"features": features, "scores": aggregates}

    def save(
        self, model_name: str, model_version: int, batch_name: str, aggregation: Any
    ):
        with SqliteContextManager() as cur:
            data = json.dumps(aggregation)
            cur.execute(
                "INSERT INTO aggregations VALUES (?, ?, ?, ?)",
                (model_name, model_version, batch_name, data),
            )
