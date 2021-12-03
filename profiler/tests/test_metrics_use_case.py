import pytest
from profiler.domain.model import Model
from profiler.domain.model_signature import ModelSignature

from profiler.ports.metrics_repository import MetricsRepository
from profiler.use_cases.metrics_use_case import MetricsUseCase
from profiler.adapters.metrics_repository.local_metrics_repository import (
    LocalMetricsRepository,
)

# TODO!: add tests


class TestMetricsUseCase:
    @pytest.fixture(scope="class", autouse=True)
    def empty_signature(self) -> ModelSignature:
        return ModelSignature(inputs=[], outputs=[])

    @pytest.fixture
    def model_with_empty_signature(self, empty_signature) -> Model:
        return Model("adult", 1, empty_signature)

    @pytest.fixture
    def metrics_repository(self) -> MetricsRepository:
        return LocalMetricsRepository()

    @pytest.fixture
    def metrics_use_case(self, metrics_repository: MetricsRepository):
        return MetricsUseCase(metrics_repository)

    def test_x(model_with_empty_signature):
        assert 1 == 1
