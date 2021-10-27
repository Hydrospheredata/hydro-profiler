import json
import sqlite3
from typing import Any, Dict

from profiler.ports.aggregations_repository import AggregationsRepository

class SqliteAggregationsRepository(AggregationsRepository):
    con = sqlite3.connect("profiler/resources/db/sqlite/profiler.db", check_same_thread=False)
    cur = con.cursor()

    def get_list(self, model_name: str, model_version: int) -> Dict[str, Any]:
        self.cur.execute("SELECT model_name, batch_name, aggregation FROM aggregations WHERE model_name=? AND model_version=?", (model_name, model_version))
        db_rows = self.cur.fetchall()

        if len(db_rows) == 0:
            return {
                "features": [],
                "scores": []
            }
        else:
            features = []
            aggregates = []

            for model_name, batch_name, raw_aggregation  in db_rows:
                agg = json.loads(raw_aggregation)
                features = agg['keys']
                aggregates.append({
                    "batch_name": batch_name,
                    "scores": agg["scores"]
                })

            return {
                "features": features,
                "scores": aggregates
            }

    def save(self, model_name: str, model_version: int, batch_name: str, aggregation: Any):
        data = json.dumps(aggregation)
        self.cur.execute("INSERT INTO aggregations VALUES (?, ?, ?, ?)", (model_name, model_version, batch_name, data))
        self.con.commit()
