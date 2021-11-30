from profiler.domain.feature_metric import MinMaxMetric
import json

from profiler.domain.feature_metric import CheckType


def test_min_max():
    metric = MinMaxMetric(min=0.1, max=0.5)

    raw = json.dumps(metric.__dict__)
    parsed = json.loads(raw)

    metric = MinMaxMetric(parsed["min"], parsed["max"])
    assert parsed["min"] == 0.1
    assert metric.check(0.3)["status"] == CheckType.SUCCESS
