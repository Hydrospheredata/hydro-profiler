from pydantic import BaseModel
from typing import Any


class Check(BaseModel):
    check: bool
    description: str
    value: Any
    threshold: Any
