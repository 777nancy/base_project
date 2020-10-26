from datetime import datetime


def get_microsecond_now():
    dt = datetime.now()

    return int(dt.timestamp() * 1000)
