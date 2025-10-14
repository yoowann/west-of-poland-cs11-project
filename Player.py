class Player():
    """
    Class for the Player

    Attributes:
        x (int) - horizontal position of the Player
        y (int) - vertical position of the Player
        inv (string) - the Player's currently held item
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inv = ""