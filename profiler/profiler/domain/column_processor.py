import pandas as pd
from profiler.domain.column_report import ColumnReport
from profiler.domain.metric_config import NumericalMetricConfig, CategoricalMetricConfig
import profiler.domain.descriptions as de

pd.options.mode.use_inf_as_na = True


def process_numerical_column(
    feature_name: str, series: pd.Series, config: NumericalMetricConfig
) -> ColumnReport:
    is_missing_value = series.isna()
    missing_values = series[is_missing_value]
    not_missing_values = series[~is_missing_value]

    is_between_min_max = not_missing_values.between(config.min, config.max)
    failed_min_max = not_missing_values[~is_between_min_max]
    passed_min_max = not_missing_values[is_between_min_max]

    is_in_percentile = passed_min_max.between(config.perc_01, config.perc_99)
    failed_percentile = passed_min_max[~is_in_percentile]

    IQR = config.perc_75 - config.perc_25
    lower_iqr = config.perc_25 - (IQR * 1.5)
    upper_iqr = config.perc_75 + (IQR * 1.5)
    is_in_iqr = passed_min_max.between(lower_iqr, upper_iqr)
    failed_iqr = passed_min_max[~is_in_iqr]

    failed_rows = {}
    susp_rows = {}

    for i in missing_values.index:
        failed_rows[i] = [de.missing_value(feature_name)]

    for i in failed_min_max.index:
        failed_rows[i] = [
            de.failed_min_max_description(
                feature_name, failed_min_max[i].item(), config.min, config.max
            )
        ]

    for i in failed_percentile.index:
        desc = de.susp_percentile_description(
            feature_name, failed_percentile[i].item(), config.perc_01, config.perc_99
        )

        if i not in susp_rows:
            susp_rows[i] = [desc]
        else:
            susp_rows[i].extend(desc)

    for i in failed_iqr.index:
        desc = de.susp_iqr_description(
            feature_name, failed_iqr[i].item(), lower_iqr, upper_iqr
        )
        if i not in susp_rows:
            susp_rows[i] = [desc]
        else:
            susp_rows[i].extend([desc])

    return ColumnReport(feature_name, series.size, failed_rows, susp_rows)


def process_categorical_column(
    feature_name: str, series: pd.Series, config: CategoricalMetricConfig
) -> ColumnReport:
    categories = config.categories

    is_missing_value = series.isna()
    missing_values = series[is_missing_value]
    not_missing_values = series[~is_missing_value]

    is_in_category = not_missing_values.isin(categories)
    failed_category = not_missing_values[~is_in_category]

    failed_rows = {}
    susp_rows = {}

    for i in missing_values.index:
        failed_rows[i] = [de.missing_value(feature_name)]

    for i in failed_category.index:
        desc = de.failed_category_description(feature_name, failed_category[i])
        failed_rows[i] = [desc]

    return ColumnReport(feature_name, series.size, failed_rows, susp_rows)
