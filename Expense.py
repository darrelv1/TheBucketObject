from bucket_types import *
from datetime import date, datetime
import calendar as cal
from Installment import Installment
from base import BucketComponent


class Expense(BucketComponent):
    hora: datetime = datetime.today()

    def __init__(self, data: ExpenseType):

        self.data: ExpenseType = data
        self.expense_name: str = data['expense']
        self.amount: float = data['details']['amount']
        self.due_date: int = data['details']['due_date']
        self._frequency: str = data['details']['frequency']
        self._contributed_amount: float = 0.00
        self._amount_after_contributions: float = 0.00
        self.payment_status: str = "Not Paid"
        self._currmonth_contributions: list[date] = []

        # Internal Variable
        self.due = False
        self.days_left = self.due_date - Expense.hora.day if Expense.hora.day < self.due_date else None
        self._installment: InstallmentType = {}

    def __str__(self):
        return self.expense_name

    # Working in Progress
    @property
    def currmonth_contributions(self):
        payperiods: list[date] = self._installment['payperiods']
        self._currmonth_contributions: list = [period for period in payperiods if period.month == self.active_month]
        return self._currmonth_contributions

    @property
    def contributed_amount(self):
        payment_details = self._installment

        if len(payment_details.items()) == 0:
            self._contributed_amount = self.amount
            return self._contributed_amount
        else:
            self._contributed_amount = payment_details['contributions'] * (
                        self.amount / payment_details['monthly_pay_periods'])
            return self._contributed_amount

    @property
    def amount_after_contributions(self):
        self._amount_after_contributions = self.amount - self._contributed_amount
        return self.amount - self._contributed_amount

    @property
    def installment(self):
        install_insta = Installment()
        new = install_insta.get_result(date(2023, 7, 27))
        self._installment = {**self._installment, **new}
        return self._installment

    @property
    def frequency(self) -> int:
        table = {
            'Monthly': '1',
            'biweekly': '2'
        }

        return table[self._frequency]

    @frequency.setter
    def frequency(self, new_freq):
        self._frequency = new_freq

    def __reCalculate__(self):
        self.days_left = self.due_date - Expense.hora.day if Expense.hora.day < self.due_date else 0
        self.due = False if Expense.hora.day < self.due_date else True
        self.payment_status = "Overdue" if (self.payment_status == "Not Paid") and (
                Expense.hora.day >= self.due_date) else self.payment_status

    def __call__(self, amount=0.00, add=False) -> float | None:
        self.amount += amount if add else (amount * -1)
        self.__reCalculate__()
        return self.amount

    def __gt__(self, other):
        if not isinstance(other, Expense):
            return NotImplemented
        return self.days_left > other.days_left

    def __lt__(self, other):
        if not isinstance(other, Expense):
            return NotImplemented
        return self.days_left < other.days_left

    def __repr__(self):
        return (f"Expense({{'expense': '{self.expense_name}', "
                f"'details': {{'amount': {self.amount}, "
                f"'due_date': {self.due_date}, 'frequency': {self.frequency})")

    def to_dict(self):
        return {

            'expense_name': self.expense_name,
            'amount': self.amount,
            'due_date': self.due_date,
            'frequency': self.frequency,
            'status': self.payment_status,
            'due': self.due,
            'days_left': self.days_left
        }
