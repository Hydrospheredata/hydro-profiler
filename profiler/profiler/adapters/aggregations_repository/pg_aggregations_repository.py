from sqlalchemy import text
from profiler.domain.aggregation import Aggregation, AggregationBatch
from profiler.domain.model_report import FeaturesOverall
from profiler.ports.aggregations_repository import AggregationsRepository
from profiler.db.pg_engine import engine


class PgAggregationsRepository(AggregationsRepository):
    def get_aggregation(self, model_name: str, model_version: int) -> Aggregation:
        with engine.connect() as conn:
            print("get aggregation")
            query = text(
                """SELECT model_name, batch_name, file_timestamp, aggregation, batch_rows_count 
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
                    batch_rows_count,
                ) = row

                batch = AggregationBatch(
                    model_name=model_name,
                    model_version=model_version,
                    rows_count=batch_rows_count,
                    batch_name=batch_name,
                    file_timestamp=file_timestamp,
                    feature_overall=FeaturesOverall.parse_raw(raw_aggregation),
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
        aggregation_batch: AggregationBatch,
    ):
        with engine.connect() as conn:
            try:
                conn.execute(
                    text(
                        "INSERT INTO aggregations VALUES (:model_name, :model_version, :batch_name, :file_timestamp, :data, :batch_rows_count)"
                    ).bindparams(
                        model_name=aggregation_batch.model_name,
                        model_version=aggregation_batch.model_version,
                        batch_name=aggregation_batch.batch_name,
                        file_timestamp=aggregation_batch.file_timestamp,
                        data=aggregation_batch.feature_overall.json(),
                        batch_rows_count=aggregation_batch.rows_count,
                    ),
                )
            except Exception as e:
                print("sql error")
                print(e)
