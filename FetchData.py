# pyright: basic

import yfinance as yf
import numpy as np
import os
import pandas as pd
from datetime import date, datetime
from typing import Set

from IFetchData import IFetchData

class FetchData(IFetchData):
    """Caches historical stock prices and calculations"""
    ROLLING_VOLATILITY_WINDOW = 365

    def __init__(self):
        self.data = {}
        self.folder_for_csvs = 'csv_folder'

    def fetch(self, symbol: str) -> pd.DataFrame:
        """Window is only for calculating the rolling volatility"""
        symbol = symbol.lower()

        if symbol in self.data:
            return self.data[symbol]

        file_path = self.get_symbol_file_path(symbol)

        if not os.path.exists(file_path):
            # data = pd.read_csv(file_path, parse_dates=True, index_col=0, date_format="ISO8601") 
            # data = pd.read_csv(file_path, date_format="ISO8601", index_col=0) 
            data = self.download(symbol)
            self.save_df_to_csv(file_path, symbol, data)

        self.data[symbol] = pd.read_excel(file_path, index_col=0)
        
        return self.data[symbol]

    def dates_available(self, symbol: str) -> Set[datetime]:
        data = self.fetch(symbol)

        return set(data.index)

        

    def make_folder_for_csvs_if_not_exists(self):
        if not os.path.exists(self.folder_for_csvs):
            os.makedirs(self.folder_for_csvs)

    # def check_file_exists(self, filename: str) -> bool:
    #     self.make_folder_for_csvs_if_not_exists()
    #     file_path = os.path.join(self.folder_for_csvs, filename)
    #     return os.path.isfile(file_path)

    def has_symbol(self, symbol: str) -> bool:
        return symbol in self.data

    def get_symbol_file_path(self, symbol: str) -> str:
        csv_file = f'{symbol}.xlsx'
        file_path = os.path.join(self.folder_for_csvs, csv_file)
        return file_path

    def save_df_to_csv(self, file_path: str, symbol: str, df: pd.DataFrame):
        # df.to_csv(file_path, index=True)
        df.to_excel(file_path, index=True)

    def download(self, symbol: str):
        data = yf.download(symbol, auto_adjust=True)
        assert data is not None, f"Could not download data for {symbol}"

        returns = np.log(data['Close'] / data['Close'].shift(1))
        data['Volatility'] = returns.rolling(window=self.ROLLING_VOLATILITY_WINDOW).std() * np.sqrt(252) # type: ignore
        return data
    
