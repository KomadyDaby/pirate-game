from typing import List
from player import Player

class Group():
    def __init__(self, name: str, players: List[Player]) -> None:
        self.name = name
        self.group = players
