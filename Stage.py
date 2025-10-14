import sys

class Stage:
    """
    Class for the Stage.

    Attributes:
        grid (2D list of str) - the stage that the Player is playing
        pl (Player) - Player object, containing details about the Player's position and inventory
        outcome (int) - 0 if currently playing; 1 if win; 2 if lose
        mushrooms (int) - count of mushrooms collected
        win_condition (int) - count of total mushrooms in the grid
        curr_tile (str) - the tile that the Player is currently on
        last_tile (str) - the previous tile that the Player was on
        rock_title (str) - TODO fill up
        emojis (dict) - TODO fill up
    """
    emojis = {'.': '　', 'L': '👩', 'T': '🌲', '+': '🍄', 'R': '🪨', '~': '🟦', '-': '⚪', 'x': '🪓', '*': '🔥'}
    VALID_MOVES = set(("U", "D", "L", "R", "P", "!"))
    def __init__(self, grid, pl):
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.pl = pl
        self.grid[self.pl.y][self.pl.x] = "L"
        self.outcome = 0
        self.mushrooms = 0
        self.win_condition = sum(sum(b == "+" for b in a) for a in self.grid)
        self.curr_tile = "."
        self.last_tile = "."
        self.rock_tile = "."
    
    def make_move(direction, y, x, can_move_there):
        ...

    def move(self, move_sequence, y, x):
        '''
        print("STAGE:")
        for row in self.grid:
            print(''.join(row))
        print(f"CURRENTLY AT {self.pl.y}, {self.pl.x}. MOVE SEQ IS {move_sequence.upper()}")
        '''
        if any(move not in Stage.VALID_MOVES for move in move_sequence):
            # invalid input
            return
        for move in move_sequence:
            #print(f"{move} -- currently at {self.pl.y}, {self.pl.x}")
            if move.upper() in ("U", "D", "L", "R") and not self.outcome:
                self.pl.x += 1 if (move.upper() == "R" and self.pl.x < len(self.grid[0]) - 1 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else -1 if (move.upper() == "L" and self.pl.x > 0 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else 0
                self.pl.y += 1 if (move.upper() == "D" and self.pl.y < len(self.grid) - 1 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else -1 if (move.upper() == "U" and self.pl.y > 0 and self.can_move_here(move.upper(), self.pl.x, self.pl.y)) else 0
                self.curr_tile = self.grid[self.pl.y][self.pl.x] if self.grid[self.pl.y][self.pl.x] != "L" else self.curr_tile
            elif move.upper() == "P":
                if self.curr_tile not in (".", "-") and not self.pl.inv:
                    self.pl.inv = Stage.emojis[self.curr_tile]
                    self.grid[self.pl.y][self.pl.x] = "."
                    self.curr_tile = "."
                    self.last_tile = "."
            '''
            print(f"At the end, {self.pl.y}, {self.pl.x}")
            for row in self.grid:
                print(''.join(row))
            '''
        else:
            if self.mushrooms == self.win_condition: self.outcome = 1
            self.grid[y][x] = self.last_tile
            self.last_tile = self.grid[self.pl.y][self.pl.x]
            self.grid[self.pl.y][self.pl.x] = "L"
        
    def clear_modify(self, new_grid, first):
        if not first:
            for _ in range(len(self.grid) + 15):
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear line from cursor to end
        nice = [[Stage.emojis[a] for a in b] for b in new_grid]
        for line in nice:
            sys.stdout.write("".join(line) + "\n")
        sys.stdout.flush()
        
    def scorch(self, y, x):
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
        x += 1 if direction == "R" and self.pl.x < len(self.grid[0]) - 1 else -1 if direction == "L" and self.pl.x > 0 else 0
        y += 1 if direction == "D" and self.pl.y < len(self.grid) - 1 else -1 if direction == "U" and self.pl.y > 0 else 0
        x_chk = x + 1 if direction == "R" else x - 1 if direction == "L" else x
        y_chk = y + 1 if direction == "D" else y - 1 if direction == "U" else y
        #print(f"Seeing if player can move to {y}, {x}. Inv is {self.pl.inv}")
        
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
                self.outcome = 2
                return True       
            case 'R':
                # check if the tile the rock will be moved to is empty, paved, or water
                if self.grid[y_chk][x_chk] in ('.', '-', 'L'):
                    self.grid[y][x] = self.rock_tile if self.curr_tile == self.rock_tile else '.'
                    self.rock_tile = self.grid[y_chk][x_chk]
                    self.grid[y_chk][x_chk] = 'R'
                    return True
                elif self.grid[y_chk][x_chk] == '~':
                    self.grid[y][x] = self.rock_tile
                    self.grid[y_chk][x_chk] = '-'
                    return True
                else:
                    return False
            case '+':
                # pick up the mushroom
                self.mushrooms += 1
                if self.mushrooms == self.win_condition:
                    self.outcome = 1
                self.grid[y][x] = '.'
                return True
            case _: # default case; ideally, the code shouldn't reach this
                print("Something went wrong!")