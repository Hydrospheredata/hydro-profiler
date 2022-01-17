import json
from profiler.domain.batch_report import BatchReport
from profiler.ports.reports_repository import ReportsRepository

from sqlalchemy import text
from profiler.db.pg_engine import engine
from profiler.utils.json_dumper import dumper


class PgReportsRepository(ReportsRepository):
    def get_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> BatchReport:
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

            decded_report = json.loads(report)

            batch_report = BatchReport(
                model_name=model_name,
                model_version=model_version,
                batch_name=batch_name,
                file_timestamp=file_timestamp,
                rows_count=decded_report["rows_count"],
            )

            batch_report.failed_rows = decded_report["failed_rows"]
            batch_report.suspicious_rows = decded_report["suspicious_rows"]
            batch_report.features_statistics = decded_report["features_statistics"]

            return batch_report

    def save(self, report: BatchReport):
        with engine.connect() as conn:

            data = {
                "failed_rows": report.failed_rows,
                "suspicious_rows": report.suspicious_rows,
                "features_statistics": report.features_statistics,
                "rows_count": report.rows_count,
            }

            query = text(
                "INSERT INTO reports VALUES (:model_name, :model_version, :batch_name, :file_timestamp, :data)"
            ).bindparams(
                model_name=report.model_name,
                model_version=report.model_version,
                batch_name=report.batch_name,
                file_timestamp=report.file_timestamp,
                data=json.dumps(data, default=dumper),
            )
            conn.execute(query)
