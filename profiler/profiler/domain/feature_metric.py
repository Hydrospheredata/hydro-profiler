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


class BaseMetric(BaseModel, ABC):
    count_score: bool = False

    @abstractmethod
    def check(self, value):
        pass


class MinMaxMetric(BaseMetric):
    count_score: bool = True
    min: int
    max: int

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
    categories: List[str]
    count_score = True

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

    def check(self, value: str):
        if str(value) in self.categories:
            return self.success(value)
        else:
            return self.fail(value)


class PercentileMetric(BaseMetric):
    perc_01: int
    perc_99: int

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
    perc_25: int
    perc_75: int

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
        if lower_bound <= value <= upper_bound:
            return self.success(value, lower_bound, upper_bound)
        else:
            return self.fail(value, lower_bound, upper_bound)


def recognize_metric(x):
    if x["type"] == MetricType.MIN_MAX:
        return MinMaxMetric.parse_obj(x["config"])
    elif x["type"] == MetricType.IN:
        return IncludeMetric.parse_obj(x["config"])
    elif x["type"] == MetricType.IQR:
        return IQRMetric.parse_obj(x["config"])
    elif x["type"] == MetricType.PERCENTILE:
        return PercentileMetric.parse_obj(x["config"])
    else:
        return None
