from datetime import datetime
import logging
import pandas as pd

from profiler.use_cases.aggregation_use_case import AggregationUseCase
from profiler.use_cases.metrics_use_case import MetricsUseCase
from profiler.use_cases.overall_reports_use_case import OverallReportsUseCase
from profiler.use_cases.report_use_case import ReportUseCase


class TestMetricsUseCase:
    def test_x(
        self,
        caplog,
        models_repo,
        metrics_use_case,
        aggregations_use_case,
        reports_use_case,
        overall_reports_use_case,
        adult_model_wrapper,
    ):
        caplog.set_level(logging.INFO)
        agg_uc: AggregationUseCase = aggregations_use_case
        metrics_uc: MetricsUseCase = metrics_use_case
        reports_uc: ReportUseCase = reports_use_case
        overall_uc: OverallReportsUseCase = overall_reports_use_case

        model = adult_model_wrapper.model
        train_file = pd.read_csv(adult_model_wrapper.get_batch("train.csv"))
        batch_file = pd.read_csv(adult_model_wrapper.get_batch("batch_3.csv"))

        models_repo.save(model)

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
