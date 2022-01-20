from profiler.domain.errors import EntityNotFoundError, EntityWasNotStoredError
from profiler.ports.overall_reports_repository import OverallReportsRepository
from profiler.domain.overall_report import OverallReport

from sqlalchemy import text
from profiler.db.pg_engine import engine


class PgOverallReportsRepository(OverallReportsRepository):
    def get_overall_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        with engine.connect() as conn:
            query = text(
                "SELECT * FROM overall_reports WHERE model_name=:model_name AND model_version=:model_version AND batch_name=:batch_name"
            ).bindparams(
                model_name=model_name,
                model_version=model_version,
                batch_name=batch_name,
            )

            result = conn.execute(query).fetchone()

            if result is None:
                raise EntityNotFoundError(
                    f"Overall report for {model_name}:{model_version} was not found"
                )

            if result:
                (
                    model_name,
                    model_version,
                    batch_name,
                    suspicious_percent,
                    failed_ratio,
                ) = result

                return OverallReport(
                    model_name=model_name,
                    model_version=model_version,
                    batch_name=batch_name,
                    suspicious_percent=suspicious_percent,
                    failed_ratio=failed_ratio,
                )
            else:
                return None

    def save(self, overall_report: OverallReport) -> None:
        with engine.connect() as conn:
            try:
                query = text(
                    "INSERT INTO overall_reports VALUES (:model_name, :model_version, :batch_name, :suspicious_percent, :failed_ratio)"
                ).bindparams(
                    model_name=overall_report.model_name,
                    model_version=overall_report.model_version,
                    batch_name=overall_report.batch_name,
                    suspicious_percent=overall_report.suspicious_percent,
                    failed_ratio=overall_report.failed_ratio,
                )

                conn.execute(query)
            except Exception as e:
                raise EntityWasNotStoredError(
                    f"Overall report for {overall_report.model_name}:{overall_report.model_version}/{overall_report.batch_name} was not stored",
                    e,
                )
