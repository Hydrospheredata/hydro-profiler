from abc import ABC


class MetricConfig(ABC):
    pass


class NumericalMetricConfig(MetricConfig):
    def __init__(
        self,
        min,
        max,
        perc_01,
        perc_25,
        perc_75,
        perc_99,
    ) -> None:
        self.config_type = "numerical"
        self.min = min
        self.max = max
        self.perc_01 = perc_01
        self.perc_25 = perc_25
        self.perc_75 = perc_75
        self.perc_99 = perc_99


class CategoricalMetricConfig(MetricConfig):
    def __init__(self, categories):
        self.config_type = "categorical"
        self.categories = categories


def parse_config(config):
    if config["config_type"] == "numerical":
        min = config["min"]
        max = config["max"]
        perc_01 = config["perc_01"]
        perc_99 = config["perc_99"]
        perc_25 = config["perc_25"]
        perc_75 = config["perc_75"]

        return NumericalMetricConfig(min, max, perc_01, perc_25, perc_75, perc_99)
    elif config["config_type"] == "categorical":
        return CategoricalMetricConfig(config["categories"])
    return None
