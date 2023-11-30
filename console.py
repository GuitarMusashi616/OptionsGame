import datetime
from player import Player
import yfinance as yf
import pandas as pd


class Game:
    def __init__(self):
        self.player = Player(10_000)
        self.date = datetime.date(2023, 2, 10)
        self.tsla = yf.download('TSLA')

    def play(self):
        while True:
            command = input(">")
            if command.lower() == "quit":
                break
            self.process(command)

    def get_option_price(self, symbol, strike_price, maturity, quanitity, date):
        # dic = {i:option_price(calculation_date, maturity_date, ts['Adj Close'], i, ts['Volatility'], 0, True, 0.0434) for i in range(200, 255, 5)}
        pass

    def get_price(self, symbol, quantity, date):

        today = pd.Timestamp(date.year, date.month, date.day)
        ts = self.tsla.loc[today]

        return ts['Adj Close'] * quantity


    def process(self, command):
        commands = command.lower().split()
        # buy 100 tsla shares
        # buy 1 tsla call

        # buy 100 tsla
        # sell 100 tsla

        # buy tsla call

        # graph day
        # graph week
        # graph month
        # graph year

        if commands[0] == 'info':
            print(self.date)
            print(self.player.assets)
            # dates = pd.date_range(self.date - datetime.timedelta(days=31), self.date)
            # self.tsla.loc[dates].plot()
        
        if commands[0] == 'buy':
            quantity = int(commands[1])
            symbol = commands[2]
            total_cost = self.get_price(symbol, quantity, self.date)
            self.player.assets['cash'] -= total_cost
            self.player.assets[symbol] += quantity

            if commands[1] == 'call':
                print(commands[2:])

        if commands[0] == 'sell':
            quantity = int(commands[1])
            symbol = commands[2]
            total_cost = self.get_price(symbol, quantity, self.date)
            self.player.assets['cash'] += total_cost
            self.player.assets[symbol] -= quantity

        if commands[0] == 'end':
            self.date += datetime.timedelta(weeks=1)


if __name__ == "__main__":
    game = Game()
    game.play()
