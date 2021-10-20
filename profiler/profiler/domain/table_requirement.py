from pydantic import BaseModel


class TableRequirement(BaseModel):
    column: str
    datatype: str
