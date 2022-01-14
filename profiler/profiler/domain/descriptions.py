class CheckDescription:
    def __init__(self, feature, value, metric, desc):
        self.feature = feature
        self.value = value
        self.metric = metric
        self.desc = desc


def failed_min_max_description(feature, value, min, max):
    return CheckDescription(
        feature, value, "MinMax", f"Value {value} not in [{min},{max}]"
    )


def susp_percentile_description(feature, value, perc_01, perc_99):
    return CheckDescription(
        feature,
        value,
        "Percentile(1,99)",
        f"Value {value} not in percentile [{perc_01},{perc_99}]",
    )


def susp_iqr_description(feature, value, perc_25, perc_75):
    return CheckDescription(
        feature,
        value,
        "IQR",
        f"Value {value} not in IQR [{perc_25},{perc_75}]",
    )


def failed_category_description(feature, value):
    return CheckDescription(
        feature, value, "Include", f"Value {value} not in categories"
    )
