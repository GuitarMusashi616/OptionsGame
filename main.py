import datetime
import pandas as pd
import yfinance
import numpy as np
from console import Game
from options import option_price


def get_stock_data(symbol, window=252):
    data = yfinance.download(symbol)

    returns = np.log(data['Adj Close'] / data['Adj Close'].shift(1))

    data['Volatility'] = returns.rolling(window=window).std() * np.sqrt(252)

    return data


def test():
    tsla = get_stock_data('TSLA')

    # calculation date today
    calculation_date = datetime.date.today()
    # maturity date weekly
    maturity_date = datetime.date(2023,12,8)

    today = pd.Timestamp(calculation_date.year, calculation_date.month, calculation_date.day)
    ts = tsla.loc[today]

    dic = {i:option_price(calculation_date, maturity_date, ts['Adj Close'], i, ts['Volatility'], 0, True, 0.0434) for i in range(200, 255, 5)}
    
    print(dic)


def main():
    game = Game()
    game.process("info")
    game.play()

if __name__ == "__main__":
    main()