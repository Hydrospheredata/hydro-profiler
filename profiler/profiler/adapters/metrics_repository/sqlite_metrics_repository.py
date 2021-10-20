import json
from profiler.domain.feature_metric import (
    IQRMetric,
    IncludeMetric,
    MinMaxMetric,
    PercentileMetric, MetricType,
)
from profiler.domain.metric_spec import MetricSpec
from typing import List, Dict
from profiler.ports.metrics_repository import MetricsRepository
from profiler.domain.model import Model

import sqlite3


class SqliteMetricsRepository(MetricsRepository):
    con = sqlite3.connect("profiler/resources/db/sqlite/profiler.db")
    cur = con.cursor()

    def all(self):
        return self.cur.execute("SELECT * FROM metrics")

    def by_name(self, name: str, version: int):
        self.cur.execute("SELECT metrics FROM metrics WHERE model_name=? AND model_version=?", (name, version,))
        res = self.cur.fetchone()[0]
        parsed = json.loads(res)
        r = {}

        def recognizeMetric(x):
            if x["type"] == MetricType.MIN_MAX:
                return MinMaxMetric.parse_obj(x["config"])
            elif x["type"] == MetricType.IN:
                return IncludeMetric.parse_obj(x["config"])
            elif x["type"] == MetricType.IQR:
                return IQRMetric.parse_obj(x["config"])
            elif x["type"] == MetricType.PERCENTILE:
                return PercentileMetric.parse_obj(x["config"])
            else:
                return None

        for feature, metrics in parsed.items():
            r.update({feature: list(map(recognizeMetric, metrics))})

        return r

    def save(self, model: Model, metrics: Dict[str, List[MetricSpec]]):
        data = json.dumps(metrics)
        self.cur.execute("INSERT INTO metrics VALUES (?, ?, ?)", (model.name, model.version, data))
        self.con.commit()
