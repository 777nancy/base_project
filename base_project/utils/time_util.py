from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_microsecond_now():
    dt = datetime.now()

    return int(dt.timestamp() * 1000)


def get_timestamp_now():
    """YYYY/MM/DD HH:MM:SS形式のタイムスタンプを返却する

    Returns:
        YYYY/MM/DD HH:MM:SSのタイムスタンプ
    """
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')


def get_today_stamp():
    """YYYY/MM/DD形式のタイムスタンプを返却する

    Returns:
        YYYY/MM/DDのタイムスタンプ
    """

    return datetime.now().strftime('%Y/%m/%d')


def get_date_stamp(year, month, day):
    """YYYY/MM/DD形式のタイムスタンプを返却する

    Returns:
        YYYY/MM/DDのタイムスタンプ
    """

    return datetime(year, month, day).strftime('%Y/%m/%d')


def get_past_date_stamp(date=None, years=0, months=0, days=0):
    if date is None:
        someday = datetime.now()
    else:
        someday = date
    one_day = someday - relativedelta(years=years, months=months, days=days)

    return one_day.strftime('%Y/%m/%d')
