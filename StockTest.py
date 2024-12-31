import unittest
import yfinance as yf
import numpy as np
import datetime
import pandas as pd

from FetchData import FetchData
from IFetchData import IFetchData

class StockTest(unittest.TestCase):
    def test_stuff(self):
        self.assertEqual(1, 1)

    def test_fetch_data(self):
        fetch_data: IFetchData = FetchData()
        symbol = 'tsla'
        download = fetch_data.fetch(symbol)
        cached = fetch_data.fetch(symbol)
        self.assertEqual(download.info(), cached.info())

    def test_check_dates(self):
        fetch_data: IFetchData = FetchData()
        symbol = 'tsla'
        dates = fetch_data.dates_available(symbol)
        print(dates)

if __name__ == "__main__":
    unittest.main()
    # t = StockTest()
    # t.test_check_dates()