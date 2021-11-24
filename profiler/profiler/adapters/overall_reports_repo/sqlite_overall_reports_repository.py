from profiler.ports.overall_reports_repository import OverallReportsRepository
from profiler.domain.overall_report import OverallReport

import sqlite3


class SqliteOverallReportsRepository(OverallReportsRepository):
    def get_overall_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        con = sqlite3.connect(
            "profiler/resources/db/sqlite/profiler.db", check_same_thread=False
        )
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM overall_reports WHERE model_name=? AND model_version=? AND batch_name=?",
            (
                model_name,
                model_version,
                batch_name,
            ),
        )

        (
            model_name,
            model_version,
            batch_name,
            suspicious_percent,
            failed_percent,
        ) = cur.fetchone()

        con.close()

        return OverallReport(
            model_name=model_name,
            model_version=model_version,
            batch_name=batch_name,
            suspicious_percent=suspicious_percent,
            failed_percent=failed_percent,
        )

    def save(
        self,
        model_name: str,
        model_version: int,
        batch_name: str,
        suspicious_percent: float,
        failed_percent: float,
    ) -> None:
        con = sqlite3.connect(
            "profiler/resources/db/sqlite/profiler.db", check_same_thread=False
        )
        cur = con.cursor()
        cur.execute(
            "INSERT INTO overall_reports VALUES (?, ?, ?, ?, ?)",
            (model_name, model_version, batch_name, suspicious_percent, failed_percent),
        )
        con.commit()
        con.close()
