from collections import defaultdict


class Player:
    def __init__(self, starting_cash):
        self.assets = defaultdict(int)
        self.assets['cash'] += starting_cash
        # self.assets = {
        #     'cash': starting_cash
        # }