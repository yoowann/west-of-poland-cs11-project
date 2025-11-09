import sys
from copy import deepcopy
try:
    from main.Status import Status
except ModuleNotFoundError as m:
    from Status import Status

def clamp(value, min_value, max_value):
    '''Returns value if min_value <= value <= max_value; min_value if value < min_value; and max_value if value > max_value.'''
    return max(min_value, min(value, max_value))

class Stage:
    '''
    Class for the Stage, the object of the Shroom Raider game.

    Attributes:
        - original_grid (2D list of str) - the original state of the stage
        - grid (2D list of str) - the stage that the Player is currently playing
        - original_pl (Player) - the original Player object containing details about the Player's initial position and inventory
        - pl (Player) - Player object, containing details about the Player's position and inventory
        - outcome (Status) - describes whether the game is still ongoing or has been won or lost
        - mushrooms (int) - count of mushrooms collected
        - win_condition (int) - count of total mushrooms in the grid
        - curr_tile (str) - the tile that the Player is currently on
        - last_tile (str) - the previous tile that the Player was on
        - rock_tile (dict) - the tiles under all rocks in the map
        - EMOJIS (dict) - UI representation of the ASCII symbols used in the grid
        - VALID_MOVES (set of str) - set of valid characters in the user's input for movement 
    '''
    EMOJIS = {'.': '　', 'L': '👩', 'T': '🌲', '+': '🍄', 'R': '🪨', '~': '🟦', '-': '⬜', 'x': '🪓', '*': '🔥'}
    VALID_MOVES = set(("W", "S", "A", "D", "P", "!"))
    def __init__(self, grid, pl):
        self.original_grid = grid
        self.original_pl = pl
        self.initialize_state(self.original_grid, self.original_pl)
    
    def initialize_state(self, grid, pl):
        '''Initializes the game state.'''
        self.grid = deepcopy(grid)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.pl = deepcopy(pl)
        self.grid[self.pl.y][self.pl.x] = "L"
        self.outcome = Status.ONGOING
        self.mushrooms = 0
        self.curr_tile = self.last_tile = "."
        self.rock_tile = {(y, x) : "." for y in range(self.rows) for x in range(self.cols) if self.grid[y][x] == "R"}
        self.win_condition = sum(sum(tile == "+" for tile in row) for row in self.grid)

    def move(self, move_sequence, y, x):
        '''
        Moves the character in the grid of Stage according to the input in move_sequence.
        
        It iterates over each input and checks whether each movement/action is valid. If it is invalid, it halts. Otherwise, the iteration completes
        and leads to a change in Stage outcome.
        '''
        last_move = ""
        for move in move_sequence:
            if move.upper() not in Stage.VALID_MOVES:
                # invalid move; stop iterating any further
                break
            if self.outcome != Status.ONGOING:
                # player has either won or lost; stop iterating any further
                break
            last_move = move
            if move.upper() in ("W", "S", "A", "D"):
                if self.can_move_here(move.upper(), self.pl.x, self.pl.y):
                    match move.upper():
                        case 'W':
                            self.pl.y = clamp(self.pl.y - 1, 0, self.rows - 1)
                        case 'A':
                            self.pl.x = clamp(self.pl.x - 1, 0, self.cols - 1)
                        case 'S':
                            self.pl.y = clamp(self.pl.y + 1, 0, self.rows - 1)
                        case 'D':
                            self.pl.x = clamp(self.pl.x + 1, 0, self.cols - 1)
                        case _:
                            pass
                self.curr_tile = self.grid[self.pl.y][self.pl.x] if self.grid[self.pl.y][self.pl.x] != "L" else self.curr_tile
            elif move.upper() == "P":
                if self.curr_tile not in (".", "-") and not self.pl.inv:
                    self.pl.inv = Stage.EMOJIS[self.curr_tile]
                    self.grid[self.pl.y][self.pl.x] = "."
                    self.curr_tile = "."
                    self.last_tile = "."
            elif move == "!":
                self.initialize_state(self.original_grid, self.original_pl)
                y, x = self.original_pl.y, self.original_pl.x
        if last_move != "!":
            # update the state of the grid
            if self.mushrooms == self.win_condition:
                self.outcome = Status.WIN # player has collected all mushrooms in the stage
            self.grid[y][x] = self.last_tile if self.grid[y][x] != "R" else "R"
            self.last_tile = self.grid[self.pl.y][self.pl.x]
            self.grid[self.pl.y][self.pl.x] = "L"
        
    def clear_modify(self, new_grid, first):
        '''Formats the terminal to display the state of the new grid by clearing lines.'''
        if not first:
            for _ in range(len(self.grid) + 16):
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear line from cursor to end
        nice = [[Stage.EMOJIS[a] for a in b] for b in new_grid]
        for line in nice:
            sys.stdout.write("".join(line) + "\n")
        sys.stdout.flush()
        
    def scorch(self, y, x):
        '''
        Activates when Player runs into a tree with a flamethrower in inventory.
        
        It scans for all trees connected to the initial tree using iterative depth-first search and converts them to empty tiles.
        '''
        stack = [(y, x)]
        visited = {(y, x)}
        possible_moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        while len(stack) > 0:
            starting_y, starting_x = stack.pop()
            self.grid[starting_y][starting_x] = '.'
            for dy, dx in possible_moves:
                current_y, current_x = starting_y + dy, starting_x + dx
                if 0 <= current_y < self.rows and 0 <= current_x < self.cols and self.grid[current_y][current_x] == 'T' and (current_y, current_x) not in visited:
                    visited.add((current_y, current_x))
                    stack.append((current_y, current_x))

    def can_move_here(self, direction, x, y):
        '''Analyzes the move to be committed by Player and checks its validity according to tile value and context.'''
        x_chk, y_chk = x, y
        match direction:
            case 'D':
                x = clamp(x + 1, 0, self.cols - 1)
                x_chk = clamp(x + 1, 0, self.cols - 1)
            case 'A':
                x = clamp(x - 1, 0, self.cols - 1)
                x_chk = clamp(x - 1, 0, self.cols - 1)
            case 'S':
                y = clamp(y + 1, 0, self.rows - 1)
                y_chk = clamp(y + 1, 0, self.rows - 1)
            case 'W':
                y = clamp(y - 1, 0, self.rows - 1)
                y_chk = clamp(y - 1, 0, self.rows - 1)
            case _:
                pass
        match self.grid[y][x]:
            case '.' | '-' | 'x' | '*' | 'L':
                return True
            case 'T':
                # can move to Tree tile if Player has an axe 
                if self.pl.inv in ("x", "🪓"):
                    self.grid[y][x] = '.'
                    self.pl.inv = ''
                    return True
                # can move to Tree tile if Player has a flamethrower; if so, burn the trees connected to the tile the Player is moving to 
                if self.pl.inv in ("*", "🔥"):
                    self.scorch(y, x)
                    self.pl.inv = ''
                    return True
                return False
            case '~':
                # Player loses
                self.outcome = Status.LOSE
                return True       
            case 'R':
                # check if the tile the rock will be moved to is empty, paved, or water
                if self.grid[y_chk][x_chk] in ('.', '-', 'L'):
                    self.grid[y][x] = self.rock_tile[(y, x)]
                    self.rock_tile.pop((y, x))
                    self.rock_tile[(y_chk, x_chk)] = self.grid[y_chk][x_chk]
                    self.grid[y_chk][x_chk] = 'R'
                    return True
                elif self.grid[y_chk][x_chk] == '~':
                    self.grid[y][x] = self.rock_tile[(y, x)]
                    self.rock_tile.pop((y, x))
                    self.grid[y_chk][x_chk] = '-'
                    return True
                else:
                    return False
            case '+':
                # pick up the mushroom
                self.mushrooms += 1
                if self.mushrooms == self.win_condition:
                    self.outcome = Status.WIN
                self.grid[y][x] = '.'
                return True
            case _: # default case; should never be reached
                sys.exit()