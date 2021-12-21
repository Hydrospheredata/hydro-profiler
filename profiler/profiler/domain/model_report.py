from datetime import datetime
from typing import Any, List, Dict, Optional
from pydantic import BaseModel
from enum import Enum


class FeatureUnsucceedCalculator:
    def __init__(self, features: List[str]) -> None:
        self.features: Dict[str, FeatureUnsucceedCount] = {
            feature: FeatureUnsucceedCount() for feature in features
        }

    def add_failed(self, feature: str):
        self.features[feature] = self.features[feature].add_failed()

    def add_suspicious(self, feature: str):
        self.features[feature] = self.features[feature].add_susp()

    def get_result(self):
        return self.features


class FeatureUnsucceedCount(BaseModel):
    failed: int = 0
    suspicious: int = 0

    def add_failed(self):
        return FeatureUnsucceedCount(failed=self.failed + 1, suspicious=self.suspicious)

    def add_susp(self):
        return FeatureUnsucceedCount(failed=self.failed, suspicious=self.suspicious + 1)


class FeaturesOverall(BaseModel):
    __root__: Dict[str, FeatureUnsucceedCount]


class DataRowStatus(str, Enum):
    HAS_FAILED = "has_failed"
    HAS_SUSPICIOUS = "has_suspicious"
    HEALTHY = "healthy"


class DataRowReport(BaseModel):
    id: int
    features_checks: Dict[str, List[Any]]
    status: DataRowStatus


class Report(BaseModel):
    __root__: List[DataRowReport]


class ModelReport(BaseModel):
    model_name: str
    model_version: int
    batch_name: str
    file_timestamp: datetime
    report: Report
    features_overall: Optional[FeaturesOverall]
