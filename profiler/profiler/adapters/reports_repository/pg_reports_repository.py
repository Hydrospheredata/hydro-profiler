from profiler.domain.model_report import ModelReport, Report
from profiler.ports.reports_repository import ReportsRepository

from sqlalchemy import text
from profiler.db.pg_engine import engine


class PgReportsRepository(ReportsRepository):
    def get_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> ModelReport:
        with engine.connect() as conn:
            query = text(
                "SELECT * FROM reports WHERE model_name=:model_name AND model_version=:model_version AND batch_name=:batch_name"
            ).bindparams(
                model_name=model_name,
                model_version=model_version,
                batch_name=batch_name,
            )

            res = conn.execute(query).fetchone()

            (model_name, model_version, batch_name, file_timestamp, report) = res

            return ModelReport(
                model_name=model_name,
                model_version=model_version,
                batch_name=batch_name,
                file_timestamp=file_timestamp,
                report=Report.parse_raw(report),
            )

    def save(self, model_report: ModelReport):
        with engine.connect() as conn:
            query = text(
                "INSERT INTO reports VALUES (:model_name, :model_version, :batch_name, :file_timestamp, :data)"
            ).bindparams(
                model_name=model_report.model_name,
                model_version=model_report.model_version,
                batch_name=model_report.batch_name,
                file_timestamp=model_report.file_timestamp,
                data=model_report.report.json(),
            )
            conn.execute(query)
