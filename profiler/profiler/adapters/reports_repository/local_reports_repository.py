from typing import List
from profiler.domain.model_report import ModelReport
from profiler.ports.reports_repository import ReportsRepository


class LocalReportsRepository(ReportsRepository):
    reports: List[ModelReport] = []

    def get_report(self, model_name: str, model_version: int, batch_name: str):
        return [
            x
            for x in self.reports
            if x.model_name == model_name
            and x.model_version == model_version
            and x.batch_name == batch_name
        ][0]

    def save(self, report: ModelReport):
        self.reports.append(report)
