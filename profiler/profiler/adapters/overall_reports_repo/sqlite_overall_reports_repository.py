from profiler.ports.overall_reports_repository import OverallReportsRepository
from profiler.domain.overall_report import OverallReport

from profiler.db.sqlite_context_manager import SqliteContextManager


class SqliteOverallReportsRepository(OverallReportsRepository):
    def get_overall_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        with SqliteContextManager() as cur:
            cur.execute(
                "SELECT * FROM overall_reports WHERE model_name=? AND model_version=? AND batch_name=?",
                (
                    model_name,
                    model_version,
                    batch_name,
                ),
            )

            result = cur.fetchone()

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

    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        suspicious_percent: float,
        failed_ratio: float,
    ) -> None:
        with SqliteContextManager() as cur:
            cur.execute(
                "INSERT INTO overall_reports VALUES (?, ?, ?, ?, ?)",
                (
                    model_name,
                    model_version,
                    batch_name,
                    suspicious_percent,
                    failed_ratio,
                ),
            )
