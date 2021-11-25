from pydantic import BaseModel


class BatchStatistics(BaseModel):
    sus_ratio: float
    sus_verdict: str
    fail_ratio: float
