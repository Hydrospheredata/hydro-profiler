from profiler.domain.column_statistic import ColumnStatistic
import json


class ColumnReport:
    def __init__(self, feature_name, rows_count, failed_rows, suspicious_rows):
        self.feature_name = feature_name
        self.failed_rows = failed_rows
        self.suspicious_rows = suspicious_rows
        self.statistic = ColumnStatistic(
            rows_count, len(failed_rows.keys()), len(suspicious_rows.keys())
        )

    def toJson(self):
        res = {
            "feature_name": self.feature_name,
            "failed_rows": self.failed_rows,
            "suspicious_rows": self.suspicious_rows,
            "statistic": self.statistic,
        }

        return json.dumps(res)
