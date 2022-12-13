import os
from random import randint
from time import sleep

from requests import Session

ACCOUNT_NUMBER_LIMIT: int = int(os.environ.get("ACCOUNT_NUMBER_LIMIT"))
ACCOUNT_CREATION_CHANCE: int = int(os.environ.get("ACCOUNT_CREATION_CHANCE"))

account_list = ["account1", "account2"]


def divide_split(accounts: list[str]) -> list[int]:
    """
    If number of accounts is smaller than 50 minimum split value is 1%.
    If it is greater than 50, some accounts may have 0% split.
    """
    accounts_num = len(accounts)
    splits = [1] * accounts_num if accounts_num < 50 else [0] * accounts_num
    percentage_left = 100 - sum(splits)
    # Randomly select an iterator from a list of accounts.
    account_iter = randint(1, accounts_num) - 1

    while percentage_left > 0:
        # Assign random split values to subsequent accounts
        # until percentage sum is equal to 100.
        account_iter = account_iter + 1 if account_iter < accounts_num - 1 else 0
        splits[account_iter] += randint(1, percentage_left)
        percentage_left = 100 - sum(splits)

    return splits


session = Session()

while True:
    sleep(30)
    # Randomly create new account.
    if (
        len(account_list) < ACCOUNT_NUMBER_LIMIT
        and randint(1, 100) <= ACCOUNT_CREATION_CHANCE
    ):
        account_list.append(f"account{len(account_list) + 1}")
    splits = divide_split(account_list)
    output = {}
    for account, split in zip(account_list, splits):
        output[account] = split
    session.post(url="http://controller:8000/account_splits", json=output)
    print(output)
