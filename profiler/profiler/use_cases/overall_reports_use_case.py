from typing import Any, List
from profiler.domain.batch_statistics import BatchStatistics
from profiler.domain.overall_report import OverallReport
from profiler.ports.overall_reports_repository import OverallReportsRepository
from profiler.use_cases.report_use_case import (
    calculate_failed_ratio,
    calculate_suspicious_percent,
)
from profiler.utils.safe_divide import safe_divide


class OverallReportsUseCase:
    _overall_reports_repo: OverallReportsRepository

    def __init__(self, overall_reports_repo: OverallReportsRepository):
        self._overall_reports_repo = overall_reports_repo

    def get_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        return self._overall_reports_repo.get_overall_report(
            model_name=model_name, model_version=model_version, batch_name=batch_name
        )

    def generate_overall_report(
        self, model_name: str, model_version: int, batch_name: str, report: List[Any]
    ):
        self._overall_reports_repo.save(
            model_name=model_name,
            model_version=model_version,
            batch_name=batch_name,
            suspicious_percent=calculate_suspicious_percent(report),
            failed_ratio=calculate_failed_ratio(report),
        )
        print(
            f"Overall report was stored for {model_name}:{model_version}/{batch_name}"
        )

    def calculate_batch_stats(
        self, model_name: str, model_version: int, batch_name: str
    ) -> BatchStatistics:
        production_report = self._overall_reports_repo.get_overall_report(
            model_name=model_name, model_version=model_version, batch_name=batch_name
        )
        train_report = self._overall_reports_repo.get_overall_report(
            model_name=model_name,
            model_version=model_version,
            batch_name="training",
        )

        print("traing overall")
        print(train_report)
        print("==============")
        print("production overall")
        print(production_report)

        sus_ratio = safe_divide(
            production_report.suspicious_percent, train_report.suspicious_percent
        )

        return BatchStatistics(
            sus_ratio=sus_ratio,
            sus_verdict=ratio_to_verdict(ratio=sus_ratio),
            fail_ratio=production_report.failed_ratio,
        )


def ratio_to_verdict(ratio: float):
    if ratio < 1:
        return "excellent"
    elif ratio < 1.5:
        return "good"
    elif ratio < 2:
        return "fair"
    else:
        return "bad"
