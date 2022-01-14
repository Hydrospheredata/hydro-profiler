from profiler.domain.column_report import ColumnReport
from profiler.utils.merge_dict import merge_dict


class BatchReport:
    def __init__(
        self, model_name, model_version, batch_name, file_timestamp, rows_count
    ):
        self.model_name = model_name
        self.model_version = model_version
        self.batch_name = batch_name
        self.file_timestamp = file_timestamp
        self.failed_rows = {}
        self.suspicious_rows = {}
        self.features_statistics = {}
        self.rows_count = rows_count

    def process_column_report(self, cr: ColumnReport):
        self.failed_rows = merge_dict(self.failed_rows, cr.failed_rows)
        self.suspicious_rows = merge_dict(self.suspicious_rows, cr.suspicious_rows)

        self.features_statistics.update({cr.feature_name: cr.statistic})

    def calculate_suspicious_percent(self):
        suspicious_count = len(self.suspicious_rows.keys())

        if self.rows_count == 0 or suspicious_count == 0:
            return 0

        return (suspicious_count / self.rows_count) * 100

    def calculate_failed_ratio(self):
        failed_count = len(self.failed_rows.keys())

        if self.rows_count == 0 or failed_count == 0:
            return 0

        return failed_count / self.rows_count
