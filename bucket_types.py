from typing import TypedDict
from datetime import date


class Details(TypedDict):
    amount: float
    due_date: int | None
    frequency: str
    payment_status: str


class ExpenseType(TypedDict):
    expense: str
    details: Details


class FrequencyType(TypedDict):
    monthly: int
    biweekly: int


class InstallmentType(TypedDict):
    payperiods: list[date]
    monthly_pay_periods: int | None
    total_pay_periods: int | None
    contributions: int | None
    contributions_list: list[date]
