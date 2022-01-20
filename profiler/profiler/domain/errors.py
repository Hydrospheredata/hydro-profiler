class Error(Exception):
    pass


class EntityWasNotStoredError(Error):
    pass


class EntityNotFoundError(Error):
    pass


class ParsingMetricConfigError(Error):
    pass


class GenerateMetricsError(Error):
    pass


class GenerateReportError(Error):
    pass


class CreatingBatchStatsError(Error):
    pass


class ParseMetricConfigError(Error):
    pass
