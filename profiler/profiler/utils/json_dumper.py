import datetime


def is_numpy(value):
    return hasattr(value, "dtype")


def dumper(obj):
    print(obj)
    try:
        if is_numpy(obj):
            return obj.item()

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return obj.toJSON()
    except:
        return obj.__dict__
