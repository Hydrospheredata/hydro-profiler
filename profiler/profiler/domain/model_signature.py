from typing import List, Optional
from enum import IntEnum, Enum
from pydantic import BaseModel


class DataType(str, Enum):
    DT_INVALID = 'DT_INVALID'
    DT_FLOAT = 'DT_FLOAT'
    DT_DOUBLE = 'DT_DOUBLE'
    DT_INT32 = 'DT_INT32'
    DT_UINT8 = 'DT_UINT8'
    DT_INT16 = 'DT_INT16'
    DT_INT8 = 'DT_INT8'
    DT_STRING = 'DT_STRING'
    DT_INT64 = 'DT_INT64'
    DT_BOOL = 'DT_BOOL'
    DT_UINT16 = 'DT_UINT16'
    DT_HALF = 'DT_HALF'
    DT_UINT32 = 'DT_UINT32'
    DT_UINT64 = 'DT_UINT64'
    DT_ANY = 'DT_ANY'


class DataProfileType(str, Enum):
    NONE = 'NONE'
    CATEGORICAL = 'CATEGORICAL'
    NOMINAL = 'NOMINAL'
    ORDINAL = 'ORDINAL'
    NUMERICAL = 'NUMERICAL'
    CONTINUOUS = 'CONTINUOUS'
    INTERVAL = 'INTERVAL'
    RATIO = 'RATIO'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    AUDIO = 'AUDIO'
    TEXT = 'TEXT'


class TensorShape(BaseModel):
    dims: Optional[List[int]]


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
