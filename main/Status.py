from enum import Enum, auto

class Status(Enum):
    '''Enum describing the current state of the Game.'''
    WIN = auto()
    LOSE = auto()
    ONGOING = auto()