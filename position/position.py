from time import sleep
from pydantic import BaseModel

from requests import Session

session = Session()


class PositionData(BaseModel):
    accounts: list[tuple]

    def __str__(self):
        output = ""
        for account in self.accounts:
            output += f"{account[0]}: "
            for ticker, quantity in account[1].items():
                output += f"{quantity} {ticker}, "
            output += "\n"
        return output[:-2]


while True:
    sleep(10)
    response = session.get(url="http://controller:8000/position")
    data = PositionData(**response.json())
    print(data)
