import os
from random import choice, randint, random
from time import sleep

from pydantic import BaseModel, PositiveFloat
from requests import Session

TIME_INTERVAL_LIMIT: int = int(os.environ.get("TIME_INTERVAL_LIMIT"))
PRICE_FLUCTUATION_PERCENTAGE_LIMIT: int = int(
    os.environ.get("PRICE_FLUCTUATION_PERCENTAGE_LIMIT")
)
QUANTITY_LIMIT: int = int(os.environ.get("QUANTITY_LIMIT"))


class Stock(BaseModel):
    ticker: str
    value: PositiveFloat

    def change_stock_value(self, fluctuation: int) -> None:
        """
        Change the stock value in the range [-PRICE_FLUCTUATION_PERCENTAGE_LIMIT, PRICE_FLUCTUATION_PERCENTAGE_LIMIT] percent.
        Stock minimum price is 1.
        """
        self.value += self.value * (random() * 2 - 1) * fluctuation / 100
        if self.value < 1:
            self.value = 1


axa = Stock(ticker="AXA", value=30)
unh = Stock(ticker="UNH", value=540)
alv = Stock(ticker="ALV", value=215)
pru = Stock(ticker="PRU", value=100)
bnp = Stock(ticker="BNP", value=55)
hum = Stock(ticker="HUM", value=530)
cb = Stock(ticker="CB", value=220)
zurn = Stock(ticker="ZURN", value=450)
aon = Stock(ticker="AON", value=305)
aca = Stock(ticker="ACA", value=15)

STOCKS = [axa, unh, alv, pru, bnp, hum, cb, zurn, aon, aca]

session = Session()

while True:
    sleep(random() * TIME_INTERVAL_LIMIT)
    stock = choice(STOCKS)
    stock.change_stock_value(PRICE_FLUCTUATION_PERCENTAGE_LIMIT)
    output = {
        "ticker": stock.ticker,
        "price": round(stock.value, 2),
        "quantity": randint(1, QUANTITY_LIMIT),
    }
    session.post(url="http://controller:8000/trade_fills", json=output)
    print(output)
