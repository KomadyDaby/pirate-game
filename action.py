from typing import Any, List, Union
import random


class Action():
    def __init__(self, name: str) -> None:
        self.name = name
 
    def get_name(self) -> str:
        return self.name
    
    def execute(self, _) -> None:
        pass



class Passive(Action):
    def __init__(self, name: str, operation: str, value: int) -> None:
        self.name = name
        self.operation = operation
        self.value = value


    def execute(self, cash: int) -> int:
        return eval(f'{cash} {self.operation} {self.value}')
    


class Active(Action):
    def execute(self, choices: List[Any]) -> Any:
        return input(f'Enter your coice from the following: {choices}')
    


class LuckyDip(Action):
    def __init__(self, name, choices: List[Action]):
        self.name = name
        self.choices = choices

    def execute(self, arg: Union[List[Any], int]) -> Any:
        action =  random.choice(self.choices)
        return action.execute(arg)