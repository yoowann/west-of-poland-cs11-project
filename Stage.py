import sys
from copy import deepcopy

class Stage:
    """
    Class for the Stage, the object of the Shroom Raider game.

    Attributes:
        - grid (2D list of str) - the stage that the Player is playing
        - pl (Player) - Player object, containing details about the Player's position and inventory
        - outcome (int) - 0 if currently playing; 1 if win; 2 if lose
        - mushrooms (int) - count of mushrooms collected
        - win_condition (int) - count of total mushrooms in the grid
        - curr_tile (str) - the tile that the Player is currently on
        - last_tile (str) - the previous tile that the Player was on
        - rock_tile (dict) - the tiles under all rocks in the map
        - emojis (dict) - UI representation of the ASCII symbols used in the grid
    """
    emojis = {'.': '　', 'L': '👩', 'T': '🌲', '+': '🍄', 'R': '🪨', '~': '🟦', '-': '⚪', 'x': '🪓', '*': '🔥'}
    VALID_MOVES = set(("W", "S", "A", "D", "P", "!"))
    def __init__(self, grid, pl):
        self.original_grid = [row for row in grid]
        self.original_pl = pl
        self.initialize_state(self.original_grid, self.original_pl)
    
    def initialize_state(self, grid, pl):
        '''Initializes the game state'''
        self.grid = deepcopy(grid)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.pl = deepcopy(pl)
        self.grid[self.pl.y][self.pl.x] = "L"
        self.outcome = 0
        self.mushrooms = 0
        self.curr_tile = self.last_tile = "."
        self.rock_tile = {(y, x) : "." for y in range(self.rows) for x in range(self.cols) if self.grid[y][x] == "R"}
        self.win_condition = sum(sum(tile == "+" for tile in row) for row in self.grid)

    def move(self, move_sequence, y, x):
        '''
        Moves the character in the grid of Stage according to the input in move_sequence.
        
        Initially scans for invalid characters in move_sequence; the function is halted if any is detected.
        
        After the initial scan, it iterates over each input and checks whether each movement/action is valid
        and leads to a change in Stage outcome.
        '''
        if any(move.upper() not in Stage.VALID_MOVES for move in move_sequence):
            # invalid input; don't do anything
            return
        last_move = ""
        for move in move_sequence:
            last_move = move
            if move.upper() in ("W", "S", "A", "D") and not self.outcome:
                self.pl.x += 1 if (move.upper() == "D" and self.pl.x < len(self.grid[0]) - 1 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else -1 if (move.upper() == "A" and self.pl.x > 0 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else 0
                self.pl.y += 1 if (move.upper() == "S" and self.pl.y < len(self.grid) - 1 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else -1 if (move.upper() == "W" and self.pl.y > 0 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else 0
                self.curr_tile = self.grid[self.pl.y][self.pl.x] if self.grid[self.pl.y][self.pl.x] != "L" else self.curr_tile
            elif move.upper() == "P" and not self.outcome:
                if self.curr_tile not in (".", "-") and not self.pl.inv:
                    self.pl.inv = Stage.emojis[self.curr_tile]
                    self.grid[self.pl.y][self.pl.x] = "."
                    self.curr_tile = "."
                    self.last_tile = "."
            elif move == "!":
                self.initialize_state(self.original_grid, self.original_pl)
        else:
            if last_move != "!":
                if self.mushrooms == self.win_condition:
                    self.outcome = 1
                self.grid[y][x] = self.last_tile if self.grid[y][x] != "R" else "R"
                self.last_tile = self.grid[self.pl.y][self.pl.x]
                self.grid[self.pl.y][self.pl.x] = "L"
        
    def clear_modify(self, new_grid, first):
        '''Formats the terminal to display the state of the new grid by clearing lines.'''
        if not first:
            for _ in range(len(self.grid) + 16):
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear line from cursor to end
        nice = [[Stage.emojis[a] for a in b] for b in new_grid]
        for line in nice:
            sys.stdout.write("".join(line) + "\n")
        sys.stdout.flush()
        
    def scorch(self, y, x):
        '''
        Activates when Player runs into a tree with a flamethrower in inventory.
        
        It scans for all trees connected to the initial tree and converts them to empty tiles.
        '''

        # find connected component of trees using iterative depth-first search
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
        x += 1 if direction == "D" and self.pl.x < self.cols - 1 else -1 if direction == "A" and self.pl.x > 0 else 0
        y += 1 if direction == "S" and self.pl.y < self.rows - 1 else -1 if direction == "W" and self.pl.y > 0 else 0
        x_chk = x + 1 if direction == "D" else x - 1 if direction == "A" else x
        y_chk = y + 1 if direction == "S" else y - 1 if direction == "W" else y        
        match self.grid[y][x]:
            case '.' | '-' | 'x' | '*' | 'L':
                return True
            case 'T':
                # can move to Tree tile if Player has an axe or flamethrower 
                if self.pl.inv in ("x", "🪓"):
                    self.grid[y][x] = '.'
                    self.pl.inv = ''
                    return True
                if self.pl.inv in ("*", "🔥"):
                    self.scorch(y, x)
                    self.pl.inv = ''
                    return True
                return False
            case '~':
                # player loses
                self.outcome = 2 # TODO make this an enum?
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
                    self.outcome = 1 # player wins
                self.grid[y][x] = '.'
                return True
            case _: # default case; ideally should never be reached
                sys.exit()