from __future__ import annotations
from typing import Any, Dict,List, Optional
from action import Action, Passive, LuckyDip, Active
from grid import Grid
import re

class Player():
    cash = 0
    bank = 0
    shield = 0
    mirror = 0

    def __init__(self, name: str, x: int, y: int, actions: Dict[Action, int]) -> None:
        self.name = name
        self.grid = Grid(x, y, actions)

    def __str__(self) -> None:
        pass

    def get_action(self, x: str, y: int) -> Action:
        return self.grid.get(x, y)

    def get_cash(self) -> int:
        return self.cash
    
    def reset_cash(self) -> None:
        cash = 0

    def add_cash(self, cash: int) -> None:
        self.cash += cash

    def update_cash(self, cash: int) -> None:
        self.cash = cash

    def bank_cash(self) -> None:
        self.bank += self.cash 
        self.cash = 0

    def add_shield(self) -> None:
        self.shield += 1

    def add_mirror(self) -> None:
        self.mirror += 1

    def can_defend(self) -> bool:
        return self.shield + self.mirror > 0

    def get_defense_options(self) -> List[str]:
        options = ['None']
        if self.shield > 0:
            options.append('Shield')
        elif self.mirror > 0:
            options.append('Mirror')

    def defend(self) -> Optional[str]:
        if not self.can_defend():
            return 'None'

        choice = input(f'Please enter your defense option from the following {self.get_defense_options()}')
        if choice == 'Mirror':
            self.use_mirror()
        elif choice == 'Shield':
            self.use_shield()

        return choice


    def use_shield(self) -> bool:
        if self.shield > 0:
            self.shield =- 1
            return True
        else:
            return False
        
    def use_mirror(self) -> bool:
        if self.mirror > 0:
            self.mirror =- 1
            return True
        else:
            return False


