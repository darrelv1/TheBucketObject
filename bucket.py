import pandas as pd
from functools import reduce
from datetime import datetime, timedelta
from datetime import datetime, date
from helpers import reduce_decorator


bills = [
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
            'amount': 1500,
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

    def getFloatingBalance(self) -> float:
        floatingbalance: float = 0.00
        expensesList: list[dict] = []
        for ele in self._expenses:
            ele_container = {}
            # is the next expense contributions before the the expense's due date?

            # Isolated current month's contributions dates only and, found out which date is next by the contributions already made to date
            index = ele.installment['contributions'] - 1
            nextcontribution_day: int = ele.currmonth_contributions[index].day

            if ele.due_date > nextcontribution_day:
                floatingbalance += ele.amount_after_contributions
                ele_container = {
                    'expense': ele.expense_name,
                    'amount': ele.amount,
                    'due_date': ele.due_date,
                    'next_contribution': nextcontribution_day,
                    'floating balance' : floatingbalance,
                    'amount after contribution': ele.amount_after_contributions,
                    'contributions_amount': ele.contributed_amount,
                    'monthly_pay_periods' : ele.installment['monthly_pay_periods']
                }
                expensesList.append(ele_container)

        return expensesList

    def call_expenses(self):
        self._balance = reduce(lambda x, y: x + y.amount, self._expenses, 0.00)
        for i in self._expenses:
            i()

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
        [print(" Name: {}\n Amount: {}\n Days left: {}\n Due: {}\n DueDate: {}\n payment_status: {}\n\n".format(
            exp.expense_name, exp.amount, exp.days_left, exp.due, exp.due_date, exp.payment_status)) for exp in
            self._expenses]
        return self._expenses

    @expenses.setter
    def expenses(self, newExp: list[ExpenseType] | Expense):
        expense_collection = [Expense(exp_Item) for exp_Item in newExp]
        newdict = [*self._expenses, *expense_collection]
        self._expenses = newdict

    def __getitem__(self, index: int | str) -> Expense | None:
        if isinstance(index, str):
            try:
                return list(filter(lambda exp: index in exp.expense_name, self._expenses))[0]
            except:
                raise KeyError(f"{index} is either not found not implemented")
        elif isinstance(index, int):
            if index < len(self._expenses):
                print(f"testing __getitem__ {len(self._expenses)}")
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
        print(f"Withdraw Occur, new balance ${self.balance}")

    def deposit(self, money: float):
        self.balance += money
        print(f"Withdraw Occur, new balance ${self.balance}")

    def get_unpaid(self, amount=True):
        return [exp.amount if amount else exp for exp in self if (exp.due == True) & (exp.payment_status != "Paid")]

    def get_notdue(self, amount=True):
        return list(
            set([exp.amount if amount else exp for exp in self._expenses]) - set(self.get_unpaid(amount=amount)))

    # Balance of due
    @property
    @reduce_decorator
    def bal_to_pay(self) -> list:
        self.call_expenses()
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


