from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

HELSINKI = ZoneInfo("Europe/Helsinki")


def in_helsinki(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        return moment.replace(tzinfo=HELSINKI)
    return moment.astimezone(HELSINKI)


def local_date(moment: datetime) -> date:
    return in_helsinki(moment).date()


def week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())
