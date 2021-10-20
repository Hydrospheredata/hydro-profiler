from typing import List
from enum import IntEnum
from pydantic import BaseModel


class DataType(IntEnum):
    DT_INVALID = 0
    DT_FLOAT = 1
    DT_DOUBLE = 2
    DT_INT32 = 3
    DT_UINT8 = 4
    DT_INT16 = 5
    DT_INT8 = 6
    DT_STRING = 7
    DT_INT64 = 9
    DT_BOOL = 10
    DT_UINT16 = 17
    DT_HALF = 19
    DT_UINT32 = 22
    DT_UINT64 = 23
    DT_ANY = 24


class DataProfileType(IntEnum):
    NONE = 0
    CATEGORICAL = 1
    NOMINAL = 11
    ORDINAL = 12
    NUMERICAL = 2
    CONTINUOUS = 21
    INTERVAL = 22
    RATIO = 23
    IMAGE = 3
    VIDEO = 4
    AUDIO = 5
    TEXT = 6


class TensorShape(BaseModel):
    dims: List[int]


class ModelField(BaseModel):
    name: str
    shape: TensorShape
    dtype: DataType
    profile: DataProfileType


class ModelSignature(BaseModel):
    inputs: List[ModelField]
    outputs: List[ModelField]

    def merged_features(self) -> List[ModelField]:
        return [*self.inputs, *self.outputs]
