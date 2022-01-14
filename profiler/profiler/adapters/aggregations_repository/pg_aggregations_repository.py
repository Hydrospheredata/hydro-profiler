import json
from sqlalchemy import text
from profiler.domain.aggregation import Aggregation, AggregationBatch
from profiler.ports.aggregations_repository import AggregationsRepository
from profiler.db.pg_engine import engine
from profiler.utils.json_dumper import dumper


class PgAggregationsRepository(AggregationsRepository):
    def get_aggregation(self, model_name: str, model_version: int) -> Aggregation:
        with engine.connect() as conn:
            print("get aggregation")
            query = text(
                """SELECT model_name, batch_name, file_timestamp, aggregation
                   FROM aggregations
                   WHERE model_name=:model_name AND model_version=:model_version"""
            ).bindparams(model_name=model_name, model_version=model_version)

            db_rows = conn.execute(query).fetchall()

            if len(db_rows) == 0:
                return Aggregation(
                    model_name=model_name,
                    model_version=model_version,
                    features=[],
                    batches=[],
                )

            batches = []
            for row in db_rows:
                (
                    model_name,
                    batch_name,
                    file_timestamp,
                    raw_aggregation,
                ) = row

                batch = AggregationBatch(
                    model_name=model_name,
                    model_version=model_version,
                    batch_name=batch_name,
                    file_timestamp=file_timestamp,
                    feature_statistics=json.loads(raw_aggregation),
                )

                batches.append(batch)

            return Aggregation(
                model_name=model_name,
                model_version=model_version,
                features=[],
                batches=batches,
            )

    def save(
        self,
        batch: AggregationBatch,
    ):
        with engine.connect() as conn:
            try:
                conn.execute(
                    text(
                        "INSERT INTO aggregations VALUES (:model_name, :model_version, :batch_name, :file_timestamp, :data, :batch_rows_count)"
                    ).bindparams(
                        model_name=batch.model_name,
                        model_version=batch.model_version,
                        batch_name=batch.batch_name,
                        file_timestamp=batch.file_timestamp,
                        data=json.dumps(batch.feature_statistics, default=dumper),
                        batch_rows_count=0,
                    ),
                )
            except Exception as e:
                print("sql error")
                print(e)
