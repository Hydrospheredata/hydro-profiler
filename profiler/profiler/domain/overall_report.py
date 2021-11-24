from pydantic import BaseModel


class OverallReport(BaseModel):
    model_name: str
    model_version: int
    batch_name: str
    suspicious_percent: float
    failed_percent: float
