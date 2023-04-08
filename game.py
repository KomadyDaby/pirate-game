from player import Player
from group import Group
from action import Action, Active, Passive, LuckyDip
from grid import Grid
from typing import List
import random
import string

#df.loc[df.index[1], 'A']

class Game():
    previous_moves = []
    next_moves = []

    def __init__(self, n_players: int, n_groups: int, x: int, y: int, actions: List[Action, int]) -> None:
        self.x = list(string.ascii_uppercase)[:x]
        self.y = list(range(y))

        self.actions = actions
        
        self.players = {}
        for p in range(n_players):
            self.players[p] = Player(str(p), x, y, actions)

        players = self.players.values()
        random.shuffle(players)

        self.groups = {}
        group_size = n_players//n_groups
        for g in range(n_groups): 
            self.groups[g] = Group(str(g), players[g*group_size: min(n_players, (g+1)*group_size)])

        self.moves = [f'{x}{y}' for x in self.x for y in self.y]
        random.shuffle(self.moves)

    def play(self) -> None:
        for move in self.moves:
            if move in self.previous_moves:
                continue

            while len(self.next_moves) > 0: 
                self.round(self.next_moves.pop(0))

            self.round(move)

    def get_loc(self, move: str) -> Tuple[str, int]:
        return re.findall('[A-Za-z]+', move)[0].upper(), int(re.findall('[0-9]+', move)[0])


    def passive_actions(self, x: str, y: int) -> None:
        for name, player in self.players.items():
            action = player.get_action(x, y)

            if type(action) == Passive:
                player.update_cash(action.execute(player.get_cash()))
            elif type(action) == Action:
                if action.get_name() == 'Bank':
                    player.bank_cash()
                elif action.get_name() == 'Shield':
                    player.add_shield()
                elif action.get_name() == 'Mirror':
                    player.add_mirror()

    def kill_player(self, name: str, player: Player) -> None:
        choice = action.execute(self.players.keys().remove(name))
        respose = self.players[choice].defend()
        if response == 'None':
            print(f'{name} killed {choice}')
            self.players[choice].reset_cash()
        elif response == 'Shield':
            print(f'{name} tried to kill {choice} but {choice} used their shield.')
        elif reponse == 'Mirror':
            print(f'{name} tried to kill {choice} but {choice} used their mirror.')
            while reponse == 'Mirror':
                response = player.defend()
                if response == 'None':
                    print(f'{choice} killed {name}')
                    self.players[choice].reset_cash()
                elif response == 'Shield':
                    print(f'{choice} tried to mirror {name} but {name} used their shield.')
                elif response == 'Mirror':
                    print(f'{name} tried to mirror {choice} but {choice} used their mirror.')
                    respose = self.players[choice].defend()
                    if response == 'None':
                        print(f'{name} killed {choice}')
                        self.players[choice].reset_cash()
                    elif response == 'Shield':
                        print(f'{name} tried to mirror {choice} but {choice} used their shield.')
                    elif reponse == 'Mirror':
                        print(f'{name} tried to mirror {choice} but {choice} used their mirror.')


    def active_actions(self, x: str, y: int) -> None:
        for name, player in self.players.items():
            action = player.get_action(x, y)

            if type(action) == Active:
                if action.get_name() == 'Kill a Player':
                    self.kill_player(name, player)
                elif action.get_name() == 'Kill a Group':
                    pass
                elif action.get_name() == 'Swap Cash':
                    choice = action.execute(self.players.keys().remove(name))
                    player_cash = player.get_cash()
                    player.update_cash(self.players[choice].get_cash())
                    self.players[choice].update_cash(player_cash)
                elif action.get_name() == 'Rob a Player':
                    choice = action.execute(self.players.keys().remove(name))
                    player.add_cash(self.players[choice].get_cash())
                    self.players[choice].reset_cash()
                elif action.get_name() == 'Choose next square':
                    remaining_moves = set(self.moves).difference(set(self.previous_moves)).difference(set(self.next_moves))
                    self.next_moves.append(action.execute(remaining_moves))

    def round(self, move: str) -> None:
        self.previous_moves.append(move)

        x, y = self.get_loc(move)

        self.passive_actions(x, y)

        self.active_actions(x, y)











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

game = Game(12, 4, 7, 7, actions)