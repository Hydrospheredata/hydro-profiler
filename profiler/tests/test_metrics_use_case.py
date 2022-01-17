from datetime import datetime
from profiler.adapters.overall_reports_repo.local_overall_reports_repository import (
    LocalOverallReportRepository,
)
from profiler.domain.model_signature import ModelSignature
from profiler.domain.model import Model
from profiler.adapters.models_repository.local_model_reporsitory import (
    LocalModelsRepository,
)

from profiler.adapters.reports_repository.local_reports_repository import (
    LocalReportsRepository,
)

from profiler.use_cases.aggregation_use_case import AggregationUseCase
from profiler.use_cases.metrics_use_case import MetricsUseCase
from profiler.adapters.metrics_repository.local_metrics_repository import (
    LocalMetricsRepository,
)
from profiler.adapters.aggregations_repository.local_aggregation_repository import (
    LocalAggregationsRepository,
)

import os
import pandas as pd
from profiler.use_cases.overall_reports_use_case import OverallReportsUseCase

from profiler.use_cases.report_use_case import ReportUseCase


class TestMetricsUseCase:
    def test_x(self):
        test_path = os.path.realpath(os.path.dirname(__file__))
        adult_folder = os.path.join(test_path, "resources/adult")
        metric_repo = LocalMetricsRepository()
        models_repo = LocalModelsRepository()
        reports_repo = LocalReportsRepository()
        agg_repo = LocalAggregationsRepository()
        overall_reports_repo = LocalOverallReportRepository()

        agg_uc: AggregationUseCase = AggregationUseCase(agg_repo, models_repo)
        metrics_uc: MetricsUseCase = MetricsUseCase(metric_repo)
        reports_uc: ReportUseCase = ReportUseCase(
            models_repo, reports_repo, metrics_uc, agg_uc
        )

        overall_uc: OverallReportsUseCase = OverallReportsUseCase(overall_reports_repo)

        contract = ModelSignature.parse_file(
            os.path.join(adult_folder, "contract.json")
        )
        model = Model(name="adult", version=1, contract=contract)
        models_repo.save(model)
        train_file = pd.read_csv(os.path.join(adult_folder, "train.csv"))
        batch_file = pd.read_csv(os.path.join(adult_folder, "batch_3.csv"))

        metrics_uc.generate_metrics(model, train_file)
        metrics = metrics_uc.get_by_model(model)

        training_report = reports_uc.generate_report(
            model, "training", datetime.now(), train_file
        )
        reports_uc.save_report(training_report)

        report = reports_uc.generate_report(
            model, "batch_2", datetime.now(), batch_file
        )
        reports_uc.save_report(report)

        agg_uc.generate_aggregation(report)
        agg = agg_uc.get(model.name, model.version)

        overall_uc.generate_overall_report(training_report)
        overall_uc.generate_overall_report(report)
        overall_report = overall_uc.get_report(model.name, model.version, "batch_2")

        stat = overall_uc.calculate_batch_stats(model.name, model.version, "batch_2")

        assert overall_report
        assert metrics
        assert report
        assert agg
        assert stat
