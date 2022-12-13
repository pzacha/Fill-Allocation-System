from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Stock(BaseModel):
    ticker: str
    price: float
    quantity: int


class Account(BaseModel):
    name: Optional[str]
    split: Optional[int]
    stocks_quantity: Optional[dict[str, int]] = {}  # Stores only ticker and quantity

    @property
    def value(self) -> float:
        value = 0
        if self.stocks_quantity:
            for stock in self.stocks_quantity:
                value += (
                    ControllerData.stocks_price[stock] * self.stocks_quantity[stock]
                )
        return value

    def split_deviation(self, market_value: float) -> float:
        """
        Return deviation from AUM split.
        """
        return self.value / market_value * 100 - self.split


class ControllerData:
    accounts: Optional[dict[str, Account]] = {
        "account1": Account(name="account1", split=50),
        "account2": Account(name="account2", split=50),
    }
    stocks_price: Optional[dict[str, int]] = {}  # Stores only ticker and price

    @classmethod
    @property
    def overall_value(cls):
        value = 0
        for account in cls.accounts.values():
            value += account.value
        return value


class ControllerAPI:
    def __init__(self):
        self._host: str = "0.0.0.0"
        self._port: int = 8000
        self.app: FastAPI = self.create_app()

    def create_app(self):
        app = FastAPI()

        @app.get("/")
        async def get_data():
            return ControllerData.accounts

        @app.get("/position")
        async def get_data():
            return {
                "accounts": [
                    (name, account.stocks_quantity)
                    for name, account in ControllerData.accounts.items()
                ]
            }

        @app.post("/account_splits")
        async def get_account_splits(account_splits: dict[str, int]):
            for account in account_splits:
                if ControllerData.accounts.get(account):
                    # Update split of existing account
                    ControllerData.accounts[account].split = account_splits[account]
                else:
                    # or add new account.
                    ControllerData.accounts[account] = Account(
                        name=account, split=account_splits[account]
                    )

        @app.post("/trade_fills")
        async def get_trade_fills(item: Stock):
            ControllerData.stocks_price[item.ticker] = item.price
            market_value = ControllerData.overall_value + item.price * item.quantity
            shares = item.quantity

            # TODO: Brute force method
            while shares > 0:
                # Calculate accounts deviation from AUM split.
                accounts_deviation = {
                    account.name: account.split_deviation(market_value)
                    for account in ControllerData.accounts.values()
                }
                sorted_deviation = {
                    a: s
                    for a, s in sorted(
                        accounts_deviation.items(), key=lambda item: item[1]
                    )
                }
                # Add new stock or add 1 share to existing one.
                ControllerData.accounts[next(iter(sorted_deviation))].stocks_quantity[
                    item.ticker
                ] = (
                    ControllerData.accounts[
                        next(iter(sorted_deviation))
                    ].stocks_quantity.get(item.ticker, 0)
                    + 1
                )
                shares -= 1

        return app

    def start(self):
        kwargs = {
            "host": self._host,
            "port": self._port,
        }
        uvicorn.run(self.app, **kwargs)


if __name__ == "__main__":
    api = ControllerAPI()
    api.start()
