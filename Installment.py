from datetime import date, datetime, timedelta
from types import *
import calendar as cal
from base import BucketComponent


class Installment(BucketComponent):

    def __init__(self):

        self.contributions: int = 0
        self.contributions_list: list[date] = []
        self.start_date: datetime | None = None
        self.payperiods: list[date] = []
        self.reserveAmount: float = 0
        self.monthly_pay_periods: int | None = 0
        self.total_pay_periods: int | None = 0

    def getPeriods(self):

        active = Installment.active_date
        intial = self.start_date

        bi_weekly: timedelta = timedelta(days=14)
        months_last_day: date = date(active.year, active.month, cal.monthrange(active.year, active.month)[1])

        temp_date: date = intial

        while temp_date < months_last_day:

            if temp_date.month == active.month:
                self.monthly_pay_periods += 1
                if temp_date.day < active.day:
                    self.contributions += 1
                    self.contributions_list = [*self.contributions_list, temp_date]

            self.total_pay_periods += 1
            self.payperiods = [*self.payperiods, temp_date]
            temp_date += bi_weekly

    def get_result(self, startdate: datetime):
        self.start_date = startdate
        self.getPeriods()
        return {
            'contributions': self.contributions,
            'contributions_list': self.contributions_list,
            'total_pay_periods': self.total_pay_periods,
            'monthly_pay_periods': self.monthly_pay_periods,
            'payperiods': self.payperiods
        }
