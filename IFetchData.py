# pyright: strict
from abc import ABC, abstractmethod
from typing import Set
from datetime import date

class IFetchData(ABC):
    @abstractmethod
    def fetch(self, symbol: str):
        pass

    @abstractmethod
    def dates_available(self, symbol: str) -> Set[date]:
        pass