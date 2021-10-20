from hydrosdk.modelversion import ModelVersion
from pydantic import BaseModel


class Report(BaseModel):
    _id: str


def report() -> Report:
    return Report()
