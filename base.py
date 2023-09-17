from abc import ABC
from datetime import datetime, timedelta, date


class BucketComponent(ABC):
    active_date: date = date.today()
    active_month: int = active_date.month
    active_day: int = active_date.day
    bi_weekly: timedelta = timedelta(days=14)
