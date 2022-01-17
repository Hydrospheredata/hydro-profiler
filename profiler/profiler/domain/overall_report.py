class OverallReport:
    def __init__(
        self, model_name, model_version, batch_name, suspicious_percent, failed_ratio
    ):
        self.model_name = model_name
        self.model_version = model_version
        self.batch_name = batch_name
        self.suspicious_percent = suspicious_percent
        self.failed_ratio = failed_ratio
