from typing import List
from pydantic import BaseModel
from datetime import datetime

from profiler.domain.model_report import FeaturesOverall


class AggregationBatch(BaseModel):
    model_name: str
    model_version: int
    rows_count: int
    batch_name: str
    file_timestamp: datetime
    feature_overall: FeaturesOverall


class Aggregation(BaseModel):
    model_name: str
    model_version: int
    features: List[str] = []
    batches: List[AggregationBatch]
