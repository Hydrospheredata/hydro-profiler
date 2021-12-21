from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional
from pydantic.main import BaseModel


class CheckType(str, Enum):
    SUCCESS = "succeed"
    FAILED = "failed"
    SUSPICIOUS = "suspicious"


class MetricsGroupType(str, Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"


class MetricType(str, Enum):
    MIN_MAX = "MinMax"
    IN = "Include"
    PERCENTILE = "Percentile(1, 99)"
    IQR = "IQR"


class MetricCheckResult(BaseModel):
    metric_type: MetricType
    status: CheckType
    description: Optional[str]


class BaseMetric(ABC):
    count_score: bool = False

    @abstractmethod
    def check(self, value) -> Optional[MetricCheckResult]:
        pass


class MetricsGroup(ABC):
    @abstractmethod
    def toJson(self) -> str:
        pass

    @abstractmethod
    def check(self, value) -> List[MetricCheckResult]:
        pass


class NumericalMetrics(MetricsGroup):
    type = MetricsGroupType.NUMERICAL

    def __init__(
        self,
        min,
        max,
        perc_01,
        perc_25,
        perc_75,
        perc_99,
    ) -> None:
        self.min = min
        self.max = max
        self.perc_01 = perc_01
        self.perc_25 = perc_25
        self.perc_75 = perc_75
        self.perc_99 = perc_99
        self.min_max_metric = MinMaxMetric(self.min, self.max)
        self.perc_metric = PercentileMetric(self.perc_01, self.perc_99)
        self.iqr_metric = IQRMetric(self.perc_25, self.perc_75)

    def toJson(self):
        d = {
            "type": self.type,
            "min": self.min,
            "max": self.max,
            "perc_01": self.perc_01,
            "perc_25": self.perc_25,
            "perc_75": self.perc_75,
            "perc_99": self.perc_99,
        }

        return d

    def check(self, value):
        not_in_min_max = self.min_max_metric.check(value)
        result = []

        if not_in_min_max:
            result.append(not_in_min_max)
        else:
            result.extend([x.check(value) for x in [self.perc_metric, self.iqr_metric]])

        return [x for x in result if x is not None]


class CategoryMetrics(MetricsGroup):
    type = MetricsGroupType.CATEGORICAL

    def __init__(self, categories) -> None:
        self.categories = categories
        self.includeMetric = IncludeMetric(categories)

    def toJson(self) -> str:
        return {"type": self.type, "categories": self.categories}

    def check(self, value):
        return [
            result for result in [self.includeMetric.check(value)] if result is not None
        ]


class MinMaxMetric(BaseMetric):
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max
        self.count_score: bool = True

    def check(self, value: int) -> Optional[Any]:
        if self.min <= value <= self.max:
            return None

        return MetricCheckResult(
            metric_type=MetricType.MIN_MAX,
            status=CheckType.FAILED,
            description=f"value {value} not in  range [{self.min}, {self.max}]",
        )


class IncludeMetric(BaseMetric):
    def __init__(self, categories) -> None:
        self.categories = categories

    def check(self, value) -> Optional[MetricCheckResult]:
        if value in self.categories:
            return None

        return MetricCheckResult(
            metric_type=MetricType.IN,
            status=CheckType.FAILED,
            description=f"Category {value} not in categories",
        )


class PercentileMetric(BaseMetric):
    def __init__(self, perc_01, perc_99) -> None:
        self.perc_01 = perc_01
        self.perc_99 = perc_99
        self.count_score = False

    def check(self, value: int):
        if self.perc_01 <= value <= self.perc_99:
            return None

        return MetricCheckResult(
            metric_type=MetricType.PERCENTILE,
            status=CheckType.SUSPICIOUS,
            description=f"value {value} not in  range [{self.perc_01}, {self.perc_99}]",
        )


class IQRMetric(BaseMetric):
    def __init__(self, perc_25, perc_75) -> None:
        self.perc_25 = perc_25
        self.perc_75 = perc_75

        IQR = self.perc_75 - self.perc_25
        self.lower_bound = self.perc_25 - (IQR * 1.5)
        self.upper_bound = self.perc_75 + (IQR * 1.5)

    def check(self, value):
        lower_f = format(self.lower_bound, ".2f")
        upper_f = format(self.upper_bound, ".2f")

        if self.lower_bound <= value <= self.upper_bound:
            return None

        return MetricCheckResult(
            metric_type=MetricType.IQR,
            status=CheckType.SUSPICIOUS,
            description=f"value {value} not in  range [{lower_f}, {upper_f}]",
        )


def parse_metric(metrics_group):
    if metrics_group["type"] == MetricsGroupType.NUMERICAL:
        min = metrics_group["min"]
        max = metrics_group["max"]
        perc_01 = metrics_group["perc_01"]
        perc_99 = metrics_group["perc_99"]
        perc_25 = metrics_group["perc_25"]
        perc_75 = metrics_group["perc_75"]

        return NumericalMetrics(min, max, perc_01, perc_25, perc_75, perc_99)
    elif metrics_group["type"] == MetricsGroupType.CATEGORICAL:
        return CategoryMetrics(metrics_group["categories"])
    return None
