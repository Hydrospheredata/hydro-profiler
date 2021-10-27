import json
from profiler.ports.reports_repository import ReportsRepository
from typing import Any, List, Dict
from profiler.domain.production_batch import ProductionBatch
from profiler.domain.model import Model

import sqlite3


class SqliteReportsRepository(ReportsRepository):
    con = sqlite3.connect("profiler/resources/db/sqlite/profiler.db", check_same_thread=False)
    cur = con.cursor()

    def get_report(self, model_name: str, model_version:int, batch_name: str) -> Any:
        self.cur.execute(
            "SELECT report FROM reports WHERE model_name=? AND model_version=? AND batch_name=?", (model_name, model_version, batch_name, )
        )
        x = self.cur.fetchone()[0]
        res = json.loads(x)

        return res

    def save(self, model_name: str, model_version: int, batch_name: str, report: list):
        data = json.dumps(report)
        self.cur.execute(
            "INSERT INTO reports VALUES (?, ?, ?, ?)", (model_name, model_version, batch_name, data, )
        )
        self.con.commit()
