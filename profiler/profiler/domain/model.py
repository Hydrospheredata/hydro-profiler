from typing import List
from pydantic import BaseModel

from profiler.domain.model_signature import ModelSignature
from profiler.domain.table_requirement import TableRequirement


class Model(BaseModel):
    name: str
    version: int
    contract: ModelSignature
