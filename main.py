from bucket import Buckets
from bucket import bills


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


#activity

mainbucket = Buckets("main_expenses", "type")
mainbucket.expenses = bills
# print(f"balance_contrib: {mainbucket.balance_contrib}")
# print(f"balance_post_contrib: {mainbucket.balance_post_contrib}")
# print(f"balance: {mainbucket.balance}")
# print(f"bal_to_pay: {mainbucket.bal_to_pay}")
# print(f"balance_contrib: {mainbucket.balance_contrib}")
#
# print(f"From the getFloatingBalance(): {mainbucket.getFloatingBalance()}")
# print(f"amount after contributions main.py {mainbucket.expenses[0].amount_after_contributions}")
# print(f"{mainbucket.expenses[0].installment['contributions_list']}")
# print(f"{mainbucket.expenses[0].installment['payperiods']}")
# # for exp in mainbucket:
# #     print((exp))


print(mainbucket.current_floating_balance)



#What is the matter with everyone and there bad news i can't believe that

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
