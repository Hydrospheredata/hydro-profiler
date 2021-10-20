from pydantic import BaseModel


class ProductionBatch(BaseModel):
    name: str
    path: str
