from profiler.domain.batch_statistics import BatchStatistics
from profiler.domain.model_report import ModelReport
from profiler.domain.overall_report import OverallReport
from profiler.ports.overall_reports_repository import OverallReportsRepository
from profiler.use_cases.report_use_case import (
    calculate_failed_ratio,
    calculate_suspicious_percent,
)
from profiler.utils.safe_divide import safe_divide


class OverallReportsUseCase:
    repo: OverallReportsRepository

    def __init__(self, repo: OverallReportsRepository):
        self.repo = repo

    def get_report(
        self, model_name: str, model_version: int, batch_name: str
    ) -> OverallReport:
        return self.repo.get_overall_report(model_name, model_version, batch_name)

    def generate_overall_report(self, model_report: ModelReport):

        overall_report = OverallReport(
            model_name=model_report.model_name,
            model_version=model_report.model_version,
            batch_name=model_report.batch_name,
            suspicious_percent=calculate_suspicious_percent(model_report),
            failed_ratio=calculate_failed_ratio(model_report),
        )

        self.repo.save(overall_report)

    def calculate_batch_stats(
        self, model_name: str, model_version: int, batch_name: str
    ) -> BatchStatistics:
        production_report = self.repo.get_overall_report(
            model_name=model_name, model_version=model_version, batch_name=batch_name
        )
        train_report = self.repo.get_overall_report(
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
