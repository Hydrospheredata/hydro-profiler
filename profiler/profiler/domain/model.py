from pydantic import BaseModel

from profiler.domain.model_signature import ModelSignature


class Model(BaseModel):
    name: str
    version: int
    contract: ModelSignature


