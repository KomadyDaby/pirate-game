from typing import Dict
from action import Action, Active, Passive, LuckyDip
import string
import random
import pandas as pd
import numpy as np


class Grid():
    def __init__(self, x: int, y: int, actions: Dict[Action, int]) -> None:
        self.x, self.y = x, y
        self.grid = pd.DataFrame(np.empty([y, x]), columns=list(string.ascii_uppercase)[:x])

        if sum(n for a, n in actions.items()) > x*y:
            raise Exception(f'Grid of dimensions {x} x {y} is too small for all actions {actions}')

        self.populate_grid(actions)

    def __str__(self) -> None:
        pass


    def get(self, x: str, y: int) -> Action:
        return self.grid.loc[self.grid.index[y], x]

    def populate_grid(self, actions: Dict[Action, int]) -> None:
        coords = [(x, y) for x in range(self.x) for y in range(self.y)]
        random.shuffle(coords)

        count = 0

        for action, n in actions.items():
            for _ in range(n):
                x, y = coords[count]
                count += 1
                self.grid.iloc[y, x] = action


actions = {
    Active('Kill a Player'): 1,
    Active('Kill a Group'): 1,
    Active('Rob a Player'): 1,
    Active('Swap Cash'): 1,
    Active('Choose next square'): 1,
    Action('Shield'): 1,
    Action('Mirror'): 1,
    Action('Bank'): 1,
    Passive('Bomb', '*', 0): 1,
    Passive('Double', '*', 2): 1,
    Passive('Money', '+', 5000): 1,
    Passive('Money', '+', 3000): 2,
    Passive('Money', '+', 1000): 10,
    Passive('Money', '+', 200): 25,
    LuckyDip('Lucky Dip', [
        Active('Kill a Player'),
        Active('Kill a Group'),
        Active('Rob a Player'),
        Active('Swap Cash'),
        Active('Choose next square'),
        Action('Shield'),
        Action('Mirror'),
        Action('Bank'),
        Passive('Bomb', '*', 0),
        Passive('Double', '*', 2)]): 1,
}