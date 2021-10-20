import abc
from enum import Enum
from typing import Any
from pydantic.main import BaseModel
from domain.check import Check


class CmpOp(str, Enum):
    IN = "IN"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"


class MetricSpec(BaseModel, abc.ABC):
    operator: str
    value: Any
    description: str

    def check(self, value):
        operator = self["operator"]
        if operator == CmpOp.GREATER_THAN.value:
            return GreaterThanMetricSpec.check(self, value=value).dict()
        elif operator == CmpOp.LESS_THAN.value:
            return LessThanMetricSpec.check(self, value=value).dict()
        elif operator == CmpOp.IN.value:
            return InMetricSpec.check(self, value=value).dict()


class InMetricSpec(MetricSpec):
    operator = CmpOp.IN.value

    def check(self, value):
        return Check(
            check=value in self["value"],
            description=self["description"],
            value=value,
            threshold=self["value"],
        )


class LessThanMetricSpec(MetricSpec):
    operator = CmpOp.LESS_THAN.value

    def check(self, value):
        threshold = self["value"]
        return Check(
            check=value < threshold,
            description=self["description"],
            value=value,
            threshold=threshold,
        )


class GreaterThanMetricSpec(MetricSpec):
    operator = CmpOp.GREATER_THAN.value

    def check(self, value):
        threshold = self["value"]
        return Check(
            check=value > threshold,
            description=self["description"],
            value=value,
            threshold=threshold,
        )
