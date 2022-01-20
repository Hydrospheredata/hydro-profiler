import pytest
import os
from profiler.adapters.aggregations_repository.local_aggregation_repository import (
    LocalAggregationsRepository,
)
from profiler.adapters.metrics_repository.local_metrics_repository import (
    LocalMetricsRepository,
)

from profiler.adapters.models_repository.local_model_reporsitory import (
    LocalModelsRepository,
)
from profiler.adapters.overall_reports_repo.local_overall_reports_repository import (
    LocalOverallReportRepository,
)
from profiler.adapters.reports_repository.local_reports_repository import (
    LocalReportsRepository,
)
from profiler.domain.model import Model
from profiler.domain.model_signature import ModelSignature
from profiler.ports.metrics_repository import MetricsRepository
from profiler.use_cases.aggregation_use_case import AggregationUseCase
from profiler.use_cases.metrics_use_case import MetricsUseCase
from profiler.use_cases.overall_reports_use_case import OverallReportsUseCase
from profiler.use_cases.report_use_case import ReportUseCase


class TestModelWrapper:
    def __init__(self, name, version, test_path) -> None:
        self.folder = os.path.join(test_path, f"resources/{name}")

        contract = ModelSignature.parse_file(os.path.join(self.folder, "contract.json"))

        self.model = Model(name=name, version=version, contract=contract)

    def get_batch(self, file_name):
        return os.path.join(self.folder, file_name)


@pytest.fixture(scope="package")
def models_repo():
    return LocalModelsRepository()


@pytest.fixture(scope="package")
def metrics_repo():
    return LocalMetricsRepository()


@pytest.fixture(scope="package")
def reports_repo():
    return LocalReportsRepository()


@pytest.fixture(scope="package")
def aggregations_repo():
    return LocalAggregationsRepository()


@pytest.fixture(scope="package")
def overall_reports_repo():
    return LocalOverallReportRepository()


@pytest.fixture(scope="package")
def metrics_use_case(metrics_repo: MetricsRepository):
    return MetricsUseCase(metrics_repo)


@pytest.fixture(scope="package")
def aggregations_use_case(models_repo, aggregations_repo):
    return AggregationUseCase(aggregations_repo, models_repo)


@pytest.fixture(scope="package")
def reports_use_case(
    models_repo, reports_repo, metrics_use_case, aggregations_use_case
):
    return ReportUseCase(
        models_repo, reports_repo, metrics_use_case, aggregations_use_case
    )


@pytest.fixture(scope="package")
def overall_reports_use_case(overall_reports_repo):
    return OverallReportsUseCase(overall_reports_repo)


@pytest.fixture(scope="package")
def test_path():
    return os.path.realpath(os.path.dirname(__file__))


@pytest.fixture(scope="package")
def adult_model_wrapper(test_path):
    return TestModelWrapper("adult", "1", test_path)
