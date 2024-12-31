import datetime
from typing import List

from matplotlib import pyplot as plt
import numpy as np
from FetchData import FetchData
from IFetchData import IFetchData
from graph import graph_prices
from options import option_price
from player import Player
import yfinance as yf
import pandas as pd
import QuantLib as ql
import os

class Game:
    def __init__(self, start_date: datetime.datetime = datetime.datetime(2023, 2, 10), starting_cash: int=10000):
        self.player = Player(starting_cash)
        self.fetch_data: IFetchData = FetchData()
        self.date = start_date

    def play(self):
        while True:
            command = input("> ")
            pcom = command.lower()
            if pcom == "quit" or pcom == 'exit' or pcom == 'q':
                break
            try:
                self.process(command)
            except:
                print("syntax error try again")

    def get_annual_volatility(self, symbol: str, date: datetime.datetime):
        from_date = date - datetime.timedelta(days=365)
        self.data[symbol].loc[from_date: date]

    # def download(self, symbol: str, window: int=365):
    #     data = yf.download(symbol, auto_adjust=True)
    #     returns = np.log(data['Close'] / data['Close'].shift(1))
    #     data['Volatility'] = returns.rolling(window=window).std() * np.sqrt(252)
    #     return data

    def graph_prices(self, symbol: str, from_date: datetime.datetime, to_date: datetime.datetime):
        # if symbol not in self.data:
        #     self.data[symbol] = self.download(symbol)

        data = self.fetch_data.fetch(symbol)

        graph_prices(data.loc[from_date:to_date]['Close'])

    def get_option_price(self, is_call: bool, symbol: str, strike_price: int, maturity: datetime.datetime, date: datetime.datetime) -> ql.VanillaOption:
        # dic = {i:option_price(calculation_date, maturity_date, ts['Close'], i, ts['Volatility'], 0, True, 0.0434) for i in range(200, 255, 5)}
        # return option_price(date, maturity, )
        ts = self.get_stock_row(symbol, date)

        dividend_rate = 0
        risk_free_rate = 0.0434

        return option_price(date, maturity, ts['Close'], strike_price, ts['Volatility'], dividend_rate, is_call, risk_free_rate)

    def get_stock_row(self, symbol: str, date: datetime.datetime):
        # if symbol not in self.data:
        #     self.data[symbol] = self.download(symbol)

        data = self.fetch_data.fetch(symbol)

        try:
            ts = data.loc[date]
        except KeyError as e:
            print("No stock price data for that day, stock market closed on weekends / holidays")
            raise e

        return ts


    def get_price(self, symbol: str, date: datetime.datetime):
        ts = self.get_stock_row(symbol, date)
        return ts['Close']

    def get_total_price(self, symbol: str, quantity: int, date: datetime.datetime):
        price = self.get_price(symbol, date)
        return price * quantity

    def print_option_stats(self, is_call: bool, symbol: str, strike_price: int, maturity: datetime.datetime, date: datetime.datetime):
        option = self.get_option_price(is_call, symbol, strike_price, maturity, date)
        ts = self.get_stock_row(symbol, date)

        print(f"Price: {option.NPV() * 100}")
        print(f"Implied Volatility: {ts['Volatility']}")
        print(f"Delta: {option.delta()}")
        print(f"Gamma: {option.gamma()}")
        print(f"Theta: {option.theta()}")
        # print(f"Vega: {option.vega()}")
        # print(f"Rho: {option.rho()}")

    def get_option_asset_name(self, is_call: bool, strike_price: int, symbol: str, maturity: datetime.datetime):
        option_type = "call" if is_call else "put"
        return f"{strike_price} {symbol} {option_type} for {maturity.date()}"

    def parse_option_asset_name(self, name: str):
        words = name.split()
        date_words = words[4].split('-')
        date_ints = [int(x) for x in date_words]
        maturity = datetime.datetime(*date_ints)
        dic = {
            "strike_price" : float(words[0]),
            "symbol" : words[1],
            "is_call" : words[2] == "call",
            "maturity" : maturity,
        }
        return dic

    def trade_options(self, is_buy: bool, is_call: bool, symbol: str, quantity: int, strike_price: int, maturity: datetime.datetime, date: datetime.datetime):
        option = self.get_option_price(is_call, symbol, strike_price, maturity, date)
        asset = self.get_option_asset_name(is_call, strike_price, symbol, maturity)
        total_cost = option.NPV() * quantity * 100
        if not is_buy:
            total_cost *= -1
            quantity *= -1
        self.exchange(asset, quantity, total_cost)

    def trade_shares(self, is_buy: bool, symbol: str, quantity: int):
        # assumes self.date is the date you are exchanging the shares
        total_cost = self.get_total_price(symbol, quantity, self.date)
        if not is_buy:
            total_cost *= -1
            quantity *= -1
        self.exchange(symbol, quantity, total_cost)

    def exchange(self, symbol: str, quantity: int, total_cost: int):
        before = str(dict(self.player.assets))
        self.player.assets['cash'] -= total_cost
        self.player.assets[symbol] += quantity
        if self.player.assets[symbol] == 0:
            del self.player.assets[symbol]
        #print(before, " -> ", dict(self.player.assets))
        print(dict(self.player.assets))


    def date_from_last_3(self, commands: List[str]):
        return datetime.datetime(int(commands[-3]), int(commands[-2]), int(commands[-1]))

    def print_date(self):
        print(self.date.strftime("%A %B %d, %Y"))

    def process(self, command: str):
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
            self.print_date()
            print(dict(self.player.assets))
            # dates = pd.date_range(self.date - datetime.timedelta(days=31), self.date)
            # self.tsla.loc[dates].plot()

        if commands[0] == 'graph':
            symbol = commands[1]

            days = 365 if len(commands) < 3 else int(commands[2])
            self.graph_prices(symbol, self.date - datetime.timedelta(days=days), self.date)
            # graph_prices(self.data[symbol])

        if commands[0] == 'check':
            if "call" in commands or "put" in commands:
                # check 250 tsla call 2023 12 5
                assert len(commands) >= 7, "eg. check 250 tsla call 2023 12 5"
                maturity = self.date_from_last_3(commands)
                self.print_option_stats(True if commands[3] == "call" else False, commands[2], int(commands[1]), maturity, self.date)
                return
                    
            symbol = commands[1]
            cost_per_share = self.get_price(symbol, self.date)
            print(f'cost per share: {cost_per_share}')
        
        if commands[0] == 'buy':
            if "call" in commands or "put" in commands:
                # buy 23 250 tsla call 2023 12 5
                assert len(commands) >= 8, "eg. buy 23 250 tsla call 2023 12 5"
                maturity = self.date_from_last_3(commands)
                self.trade_options(True, True if commands[4] == "call" else False, commands[3], int(commands[1]), int(commands[2]), maturity, self.date)
                return

            quantity = int(commands[1])
            symbol = commands[2]
            self.trade_shares(True, symbol, quantity)
            # total_cost = self.get_total_price(symbol, quantity, self.date)
            # self.player.assets['cash'] -= total_cost
            # self.player.assets[symbol] += quantity

            # if commands[1] == 'call':
            #     print(commands[2:])

        if commands[0] == 'sell':
            if "call" in commands or "put" in commands:
                # sell 23 250 tsla call 2023 12 5
                assert len(commands) >= 8, "eg. sell 23 250 tsla call 2023 12 5"
                maturity = self.date_from_last_3(commands)
                self.trade_options(False, True if commands[4] == "call" else False, commands[3], int(commands[1]), int(commands[2]), maturity, self.date)
                return

            quantity = int(commands[1])
            symbol = commands[2]
            self.trade_shares(False, symbol, quantity)
            # total_cost = self.get_total_price(symbol, quantity, self.date)
            # self.player.assets['cash'] += total_cost
            # self.player.assets[symbol] -= quantity
        if commands[0] == 'portval':
            total_val = self.player.assets['cash']
            for asset, quantity in self.player.assets.items():
                if "call" in asset or "put" in asset:
                    option_data = self.parse_option_asset_name(asset)
                    option = self.get_option_price(option_data["is_call"], option_data["symbol"], option_data["strike_price"], option_data["maturity"], self.date)
                    option_val = option.NPV() * 100 * quantity
                    print(f"{quantity}x {asset} = {option_val}")
                    total_val += option_val
                elif asset != "cash":
                    stock_val = self.get_total_price(asset, quantity, self.date)
                    print(f"{quantity}x {asset} = {stock_val}")
                    total_val += stock_val
            print(f"Portfolio Value = {total_val}")


        if commands[0] == 'end' or commands[0] == 'next' or commands[0] == 'n':
            delta = datetime.timedelta(weeks=1)
            if len(commands) > 1:
                delta = datetime.timedelta(days=int(commands[1]))
            self.date += delta
            self.print_date()

if __name__ == "__main__":
    game = Game()
    game.process("info")
    game.play()
