from typing import List
from profiler.domain.overall_report import OverallReport
from profiler.ports.overall_reports_repository import OverallReportsRepository


class LocalOverallReportRepository(OverallReportsRepository):
    reports: List[OverallReport] = []

    def get_overall_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        return [
            x
            for x in self.reports
            if x.batch_name == batch_name
            and x.model_name == model_name
            and x.model_version == model_version
        ][0]

    def save(self, overall_report: OverallReport) -> None:
        self.reports.append(overall_report)
