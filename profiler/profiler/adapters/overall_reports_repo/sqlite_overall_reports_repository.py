from profiler.ports.overall_reports_repository import OverallReportsRepository
from profiler.domain.overall_report import OverallReport

from profiler.db.sqlite_context_manager import SqliteContextManager


class SqliteOverallReportsRepository(OverallReportsRepository):
    def get_overall_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        with SqliteContextManager() as cur:
            print(f"Take overall report for {model_name}:{model_version}/{batch_name}")

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
                print("Found overall report")
                (
                    model_name,
                    model_version,
                    batch_name,
                    suspicious_percent,
                    failed_percent,
                ) = result

                return OverallReport(
                    model_name=model_name,
                    model_version=model_version,
                    batch_name=batch_name,
                    suspicious_percent=suspicious_percent,
                    failed_percent=failed_percent,
                )
            else:
                return None

    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        suspicious_percent: float,
        failed_percent: float,
    ) -> None:
        with SqliteContextManager() as cur:
            print(f"Save overall report for {model_name}:{model_version}/{batch_name}")

            cur.execute(
                "INSERT INTO overall_reports VALUES (?, ?, ?, ?, ?)",
                (
                    model_name,
                    model_version,
                    batch_name,
                    suspicious_percent,
                    failed_percent,
                ),
            )
