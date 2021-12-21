from typing import Dict
from pydantic import BaseModel
from profiler.domain.feature_metric import MetricsGroup


class MetricsByFeature(BaseModel):
    __root__: Dict[str, MetricsGroup]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {MetricsGroup: lambda mg: mg.toJson()}


class ModelMetrics(BaseModel):
    model_name: str
    model_version: int
    metrics_by_feature: MetricsByFeature

    class Config:
        arbitrary_types_allowed = True
