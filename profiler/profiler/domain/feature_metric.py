from abc import ABC, abstractmethod
from typing import List
from enum import Enum
from pydantic.main import BaseModel


class CheckType(str, Enum):
    SUCCESS = "succeed"
    FAILED = "failed"
    SUSPICIOUS = "suspicious"


class MetricType(str, Enum):
    MIN_MAX = "MinMax"
    IN = "Include"
    PERCENTILE = "Percentile(1, 99)"
    IQR = "IQR"


class BaseMetric(ABC):
    count_score: bool = False

    @abstractmethod
    def check(self, value):
        pass


class MinMaxMetric(BaseMetric):
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max
        self.count_score: bool = True

    def fail(self, value: int):
        return {
            "metric_type": MetricType.MIN_MAX,
            "status": CheckType.FAILED,
            "description": f"value {value} not in  range [{self.min}, {self.max}]",
            "count_score": self.count_score,
        }

    def success(self, value: int):
        return {
            "metric_type": MetricType.MIN_MAX,
            "status": CheckType.SUCCESS,
            "description": f"value {value} in range [{self.min}, {self.max}]",
            "count_score": self.count_score,
        }

    def check(self, value: int):
        if self.min <= value <= self.max:
            return self.success(value)
        else:
            return self.fail(value)


class IncludeMetric(BaseMetric):
    def __init__(self, categories) -> None:
        self.categories = categories
        self.count_score = True

    def fail(self, category: str):
        return {
            "metric_type": MetricType.IN,
            "status": CheckType.FAILED,
            "description": f"Category {category} not in categories",
            "count_score": self.count_score,
        }

    def success(self, category: str):
        return {
            "metric_type": MetricType.IN,
            "status": CheckType.SUCCESS,
            "description": f"Training categories includes {category}",
            "count_score": self.count_score,
        }

    def check(self, value):
        if value in self.categories:
            return self.success(value)
        else:
            return self.fail(value)


class PercentileMetric(BaseMetric):
    def __init__(self, perc_01, perc_99) -> None:
        self.perc_01 = perc_01
        self.perc_99 = perc_99
        self.count_score = False

    def fail(self, value: int):
        return {
            "metric_type": MetricType.PERCENTILE,
            "status": CheckType.SUSPICIOUS,
            "description": f"value {value} not in  range [{self.perc_01}, {self.perc_99}]",
            "count_score": self.count_score,
        }

    def success(self, value: int):
        return {
            "metric_type": MetricType.PERCENTILE,
            "status": CheckType.SUCCESS,
            "description": f"value {value} in range [{self.perc_01}, {self.perc_99}]",
            "count_score": self.count_score,
        }

    def check(self, value: int):
        if self.perc_01 <= value <= self.perc_99:
            return self.success(value)
        else:
            return self.fail(value)


class IQRMetric(BaseMetric):
    def __init__(self, perc_25, perc_75) -> None:
        self.perc_25 = perc_25
        self.perc_75 = perc_75
        self.count_score = False

    def fail(self, value: int, lower, upper):
        return {
            "metric_type": MetricType.IQR,
            "status": CheckType.SUSPICIOUS,
            "description": f"value {value} not in  range [{lower}, {upper}]",
            "count_score": self.count_score,
        }

    def success(self, value: int, lower, upper):
        return {
            "metric_type": MetricType.IQR,
            "status": CheckType.SUCCESS,
            "description": f"value {value} in range [{lower}, {upper}]",
            "count_score": self.count_score,
        }

    def check(self, value):
        IQR = self.perc_75 - self.perc_25
        lower_bound = self.perc_25 - (IQR * 1.5)
        upper_bound = self.perc_75 + (IQR * 1.5)

        lower_f = format(lower_bound, ".2f")
        upper_f = format(upper_bound, ".2f")

        if lower_bound <= value <= upper_bound:
            return self.success(value, lower_f, upper_f)
        else:
            return self.fail(value, lower_f, upper_f)


def recognize_metric(x):
    config = x["config"]

    if x["type"] == MetricType.MIN_MAX:
        return MinMaxMetric(config["min"], config["max"])
    elif x["type"] == MetricType.IN:
        return IncludeMetric(config["categories"])
    elif x["type"] == MetricType.IQR:
        return IQRMetric(config["perc_25"], config["perc_75"])
    elif x["type"] == MetricType.PERCENTILE:
        return PercentileMetric(config["perc_01"], config["perc_99"])
    else:
        return None
