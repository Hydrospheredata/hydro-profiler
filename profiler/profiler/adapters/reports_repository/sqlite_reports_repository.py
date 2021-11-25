import json
from profiler.ports.reports_repository import ReportsRepository
from typing import Any

from profiler.db.sqlite_context_manager import SqliteContextManager


class SqliteReportsRepository(ReportsRepository):
    def get_report(self, model_name: str, model_version: int, batch_name: str) -> Any:
        with SqliteContextManager() as cur:
            cur.execute(
                "SELECT report FROM reports WHERE model_name=? AND model_version=? AND batch_name=?",
                (
                    model_name,
                    model_version,
                    batch_name,
                ),
            )

            return json.loads(cur.fetchone()[0])

    def save(self, model_name: str, model_version: int, batch_name: str, report: list):
        with SqliteContextManager() as cur:
            data = json.dumps(report)
            cur.execute(
                "INSERT INTO reports VALUES (?, ?, ?, ?)",
                (
                    model_name,
                    model_version,
                    batch_name,
                    data,
                ),
            )
