import calendar
import datetime


def dt2ts(dt):
    return calendar.timegm(dt.utctimetuple())
def ts2dt(ts):
    return datetime.datetime.fromtimestamp(ts)