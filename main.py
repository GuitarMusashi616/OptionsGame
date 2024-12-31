import datetime
import pandas as pd
import yfinance
import numpy as np
from Game import Game
from random import randint

def get_random_starting_date(lower_bound = 180, upper_bound = 365) -> datetime.datetime:
    starting_date = datetime.datetime.today() - datetime.timedelta(days=randint(lower_bound, upper_bound))
    return starting_date.replace(hour=0, minute=0, second=0, microsecond=0)

def main():
    starting_cash = 10_000
    starting_date = get_random_starting_date()

    game = Game(starting_date, starting_cash)
    # game = Game()
    game.process("info")
    game.play()

if __name__ == "__main__":
    main()