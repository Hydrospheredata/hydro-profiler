import json
from profiler.ports.reports_repository import ReportsRepository
from typing import Any

from sqlalchemy import text
from profiler.db.pg_engine import engine


class PgReportsRepository(ReportsRepository):
    def get_report(self, model_name: str, model_version: int, batch_name: str) -> Any:
        with engine.connect() as conn:
            query = text(
                "SELECT report FROM reports WHERE model_name=:model_name AND model_version=:model_version AND batch_name=:batch_name"
            ).bindparams(
                model_name=model_name,
                model_version=model_version,
                batch_name=batch_name,
            )
            raw = conn.execute(query).fetchone()[0]

            return json.loads(raw)

    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        file_timestamp: str,
        report: list,
    ):
        with engine.connect() as conn:
            data = json.dumps(report)
            query = text(
                "INSERT INTO reports VALUES (:model_name, :model_version, :batch_name, :file_timestamp, :data)"
            ).bindparams(
                model_name=model_name,
                model_version=model_version,
                batch_name=batch_name,
                file_timestamp=file_timestamp,
                data=data,
            )
            conn.execute(query)
