from datetime import datetime


def get_microsecond_now():
    dt = datetime.now()

    return int(dt.timestamp() * 1000)


def get_timestamp():
    """YYYY/MM/DD HH:MM:SS形式のタイムスリップを返却する

    Returns:
        YYYY/MM/DD HH:MM:SSのタイムスタンプ
    """
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
