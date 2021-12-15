import json
from typing import Any, Dict

from sqlalchemy import text
from profiler.ports.aggregations_repository import AggregationsRepository
from profiler.db.pg_engine import engine


class PgAggregationsRepository(AggregationsRepository):
    def get_list(self, model_name: str, model_version: int) -> Dict[str, Any]:
        with engine.connect() as conn:
            query = text(
                "SELECT model_name, batch_name, file_timestamp, aggregation FROM aggregations WHERE model_name=:model_name AND model_version=:model_version"
            ).bindparams(model_name=model_name, model_version=model_version)

            db_rows = conn.execute(query).fetchall()

            if len(db_rows) == 0:
                return {"features": [], "scores": []}
            else:
                features = []
                aggregates = []

                for model_name, batch_name, file_timestamp, raw_aggregation in db_rows:
                    agg = json.loads(raw_aggregation)
                    features = agg["keys"]
                    aggregates.append(
                        {
                            "batch_name": batch_name,
                            "scores": agg["scores"],
                            "file_timestamp": file_timestamp,
                        }
                    )

                return {"features": features, "scores": aggregates}

    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        file_timestamp: str,
        aggregation: Any,
    ):
        with engine.connect() as conn:
            data = json.dumps(aggregation)
            conn.execute(
                text(
                    "INSERT INTO aggregations VALUES (:model_name, :model_version, :batch_name, :file_timestamp, :data)"
                ).bindparams(
                    model_name=model_name,
                    model_version=model_version,
                    batch_name=batch_name,
                    file_timestamp=file_timestamp,
                    data=data,
                ),
            )
