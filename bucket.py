import pandas as pd
from functools import reduce
from datetime import datetime, timedelta
from datetime import datetime, date
from helpers import reduce_decorator
from Installment import Installment
from Expense import Expense
from bucket_types import *
from functools import reduce

bills = [

    {
        'expense': 'Apple iCloud Subscription',
        'details': {
            'amount': 12.99,
            'due_date': 1,
            'frequency': 'Monthly'

        }

    },
    {
        'expense': 'Fido Bill',
        'details': {
            'amount': 80.90,
            'due_date': 27,
            'frequency': 'Monthly'

        }

    },
{
            'expense': 'Rent',
            'details': {
                'amount': 3000,
                'due_date': 15,
                'frequency': 'Monthly'

            }

        },

    {
        'expense': "Gilson's Debt",
        'details': {
            'amount': 1500,
            'due_date': 15,
            'frequency': 'Monthly'

        }

    },
    {
        'expense': 'Mortgage',
        'details': {
            'amount': 400,
            'due_date': 30,
            'frequency': 'Monthly'

        }

    },
    {
        'expense': 'Property Taxes',
        'details': {
            'amount': 110,
            'due_date': 14,
            'frequency': 'Monthly'

        }

    },
    {
        'expense': 'Maintenance',
        'details': {
            'amount': 98,
            'due_date': 14,
            'frequency': 'Monthly'

        }

    },

]

"""
Generic Accounts that will have specific behaviours and properties to address
the current problems faced with personal budgeting
"""


class Buckets:
    current_month: int = date.today().month
    bi_weekly: timedelta = timedelta(days=14)

    def __init__(self, name, type):

        self.account_name: str = name

        self.type: str = type
        self.now: datetime
        self._expenses: list[Expense] = []
        self._balance: float = 0.00
        self._bal_to_pay: float | None = 0.00
        self._balance_contrib: float = 0.00  # Amount that has been placed into account
        self._balance_post_contrib: float = 0.00  # Bucket amount after contribution/(placed away
        self._current_floating_balance = 0.00
        self._floating_balance = 0.00

    def __iter__(self):
        yield from self._expenses

    def call_expenses(self):
        self._balance = reduce(lambda x, y: x + y.amount, self._expenses, 0.00)
        for i in self._expenses:
            i()
    """
    Floating Balance: 
        An amount that account can never drop below or has to deposited into the bucket so it can keep everything a float
        
        Process was to iterate thorugh all the expenses and get all the payperiods for the month and compare then to thier respective due dates.
        if due date is before the all contribution then the amount contributed amount that was would be missing gets added to the floating amount. 
        contributed amount is not all calculate by basis of 2 on the account that some months have more than two pay periods so we used the expenses'
        monthly_pay_periods from installment class to cover that use case
        
    Current Floating Balance:
    
        Same as the floating balance except this is based on the contributions already made -  thus the current date. So, if we're on the 15th of the month and 
        the due date is on the 7th for an expense but, the next contribution wont be for the 21st - that means the floating amount will be 1 contribution left because we already made .
    """
    @property
    def current_floating_balance(self) -> float:
        self.call_expenses()
        return_obj: list[dict] = []
        for expense in self._expenses:
            floatingbalance: float = 0.00
            ele_container = {}
            # is the next expense contributions before the the expense's due date?

            # Isolated current month's contributions dates only and, found out which date is next by the contributions already made to date
            index = expense.installment['contributions']
            nextcontribution_day: int = expense.currmonth_contributions[index].day

            if expense.due_date < nextcontribution_day:
                floatingbalance += expense.amount_after_contributions

            obj = {
                expense.expense_name: expense.currmonth_contributions[index],
                'index': index,
                'due_date': expense.due_date,
                'current_floating_balance': floatingbalance
            }
            print(obj)
            return_obj = [*return_obj, obj]

        pending_amounts = [obj['current_floating_balance'] for obj in return_obj]
        self._current_floating_balance = reduce(lambda x, y: x + y, pending_amounts, 0.00)
        return self._current_floating_balance
    @property
    def floating_balance(self):
        return_obj = []
        for expense in self.expenses:
            contributions_list = expense.installment['payperiods']
            pending_dates = [pp for pp in contributions_list if
                             pp.month == date.today().month and expense.due_date < pp.day]
            pending_amount = len(pending_dates) * (expense.amount/ expense.installment['monthly_pay_periods'])

            obj = {
                expense.expense_name: pending_dates,
                'floating_balance': pending_amount
            }
            return_obj = [*return_obj, obj]
            expense.expected_floating_balance = return_obj
        pending_amounts = [x['floating_balance'] for x in return_obj]
        self._floating_balance = reduce(lambda x, y: x + y, pending_amounts, 0.00)
        print(return_obj)
        return self._floating_balance

    @property
    def balance_contrib(self):
        self.call_expenses()
        result = [exp.contributed_amount for exp in self._expenses]
        self._balance_contrib = reduce(lambda x, y: x + y, result, 0.00)

        return self._balance_contrib

    @property
    def balance_post_contrib(self):
        self._balance_post_contrib = self._balance - self._balance_contrib
        return self._balance_post_contrib

    @property
    def balance(self) -> float:
        self._balance = reduce(lambda x, y: x + y.amount, self._expenses, 0.00)
        return self._balance

    @property
    def expenses(self) -> list[Expense]:
        self.call_expenses()

        # [print(" Name: {}\n Amount: {}\n Days left: {}\n Due: {}\n DueDate: {}\n payment_status: {}\n\n".format(
        #     exp.expense_name, exp.amount, exp.days_left, exp.due, exp.due_date, exp.payment_status)) for exp in
        #     self._expenses]
        return self._expenses

    @expenses.setter
    def expenses(self, newExp: list[ExpenseType] | Expense):
        expense_collection = [Expense(exp_Item) for exp_Item in newExp]
        newdict = [*self._expenses, *expense_collection]
        self._expenses = newdict
        # [exp_item.call_all_properties() for exp_item in self._expenses]

    def __getitem__(self, index: int | str) -> Expense | None:
        if isinstance(index, str):
            try:
                return list(filter(lambda exp: index in exp.expense_name, self._expenses))[0]
            except:
                raise KeyError(f"{index} is either not found not implemented")
        elif isinstance(index, int):
            if index < len(self._expenses):

                return self._expenses[index]
            else:
                raise IndexError

    def __setitem__(self, index, value):
        self[index] = value

    def __iter__(self) -> Expense | None:
        return (exp for exp in self._expenses)

    def contains(self, item) -> bool:
        return any(exp.expense_name == item for exp in self._expenses)

    def withdraw(self, money: float):
        self.balance -= money

    def deposit(self, money: float):
        self.balance += money

    def get_unpaid(self, amount=True):
        return [exp.amount if amount else exp for exp in self._expenses if
                (exp.due == True) & (exp.payment_status != "Paid")]

    def get_notdue(self, amount=True):
        return list(
            set([exp.amount if amount else exp for exp in self._expenses]) - set(self.get_unpaid(amount=amount)))

    # Balance of due
    @property
    @reduce_decorator
    def bal_to_pay(self) -> list:
        self.call_expenses()
        self._bal_to_pay = self.get_unpaid()
        return self.get_unpaid()

    # Balance to pay
    @property
    @reduce_decorator
    def bal_upcoming(self) -> list:
        self.call_expenses()
        return self.get_notdue()

    def toDF(self, type):
        report = {
            "due": self.get_unpaid(False),
            "notdue": self.get_unpaid(False),
        }

        return pd.DataFrame([ele.to_dict() for ele in report[type]])
