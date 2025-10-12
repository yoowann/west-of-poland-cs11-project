import sys
import argparse

class Player():
    def __init__(self, x, y):
        self.x = x - 1
        self.y = y - 1
        self.inv = ""
 
class Stage_1():
    def __init__(self, grid, pl_i):
        self.grid = grid
        self.pl_i = pl_i
        self.grid[self.pl_i.y][self.pl_i.x] = "L"
        self.outcome = 0
        self.mushrooms = 0
        self.win_condition = sum([sum(1 if b == "+" else 0 for b in a) for a in self.grid])
        self.curr_tile = "."
        self.last_tile = "."
        self.rock_tile = "."
        self.emojis = {'.': '　', 'L': '👩', 'T': '🌲', '+': '🍄', 'R': '🪨', '~': '🟦', '-': '⚪', 'x': '🪓', '*': '🔥'}
    
    def move(self, move_sequence, y, x):
        for _ in move_sequence:
            if _.upper() in ("U", "D", "L", "R") and not self.outcome:
                self.pl_i.x += 1 if (_.upper() == "R" and self.pl_i.x < len(self.grid[0]) - 1 and self.analyze(_.upper(), self.pl_i.x, self.pl_i.y)) else -1 if (_.upper() == "L" and self.pl_i.x > 0 and self.analyze(_.upper(), self.pl_i.x, self.pl_i.y)) else 0
                self.pl_i.y += 1 if (_.upper() == "D" and self.pl_i.y < len(self.grid) - 1 and self.analyze(_.upper(), self.pl_i.x, self.pl_i.y)) else -1 if (_.upper() == "U" and self.pl_i.y > 0 and self.analyze(_.upper(), self.pl_i.x, self.pl_i.y)) else 0
                self.curr_tile = self.grid[self.pl_i.y][self.pl_i.x] if self.grid[self.pl_i.y][self.pl_i.x] != "L" else self.curr_tile
            elif _.upper() == "P":
                if self.curr_tile not in (".", "-") and not self.pl_i.inv:
                    self.pl_i.inv = self.emojis[self.curr_tile]
                    self.grid[self.pl_i.y][self.pl_i.x] = "."
                    self.curr_tile = "."
                    self.last_tile = "."
            elif _.upper() not in ("U", "D", "L", "R", "P", "!"):
                self.pl_i.x = x
                self.pl_i.y = y
                return
        else:
            if self.mushrooms == self.win_condition: self.outcome = 1
            self.grid[y][x] = self.last_tile
            self.last_tile = self.grid[self.pl_i.y][self.pl_i.x]
            self.grid[self.pl_i.y][self.pl_i.x] = "L"
        
    def clear_modify(self, new_grid, first):
        if not first:
            for _ in range(len(self.grid) + 15):
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear line from cursor to end`

        nice = [[self.emojis[a] for a in b] for b in new_grid]
        
        for line in nice:
            sys.stdout.write("".join(line) + "\n")
        sys.stdout.flush()
        
    def scorch(self, y, x, data = []):
        if self.grid[y][x] == 'T' and (y, x) not in data: 
            self.grid[y][x] = '.'
            data.append((y, x))
        else:
            return ()
        
        if y == 0 and x == 0:
            return self.scorch(y, x + 1, data) + self.scorch(y + 1, x, data)
        if y == len(self.grid) - 1 and x == 0:
            return self.scorch(y, x + 1, data) + self.scorch(y - 1, x, data)
        if y == 0 and x == len(self.grid[0]) - 1:
            return self.scorch(y, x - 1, data) + self.scorch(y + 1, x, data)
        if y == len(self.grid) - 1 and x == len(self.grid[0]) - 1:
            return self.scorch(y, x - 1, data) + self.scorch(y - 1, x, data)
        if y in (0, len(self.grid) - 1):
            return self.scorch(y, x + 1, data) + self.scorch(y, x - 1, data) + self.scorch(y + 1 if y == 0 else y - 1, x, data)
        if x in (0, len(self.grid[0]) - 1):
            return self.scorch(y + 1, x, data) + self.scorch(y - 1, x, data) + self.scorch(y, x + 1 if x == 0 else x - 1, data)
        return self.scorch(y + 1, x, data) + self.scorch(y - 1, x, data) + self.scorch(y, x + 1, data) + self.scorch(y, x - 1, data)
        
    def analyze(self, direction, x, y):
        x += 1 if direction == "R" and self.pl_i.x < len(self.grid[0]) - 1 else -1 if direction == "L" and self.pl_i.x > 0 else 0
        y += 1 if direction == "D" and self.pl_i.y < len(self.grid) - 1 else -1 if direction == "U" and self.pl_i.y > 0 else 0
        x_chk = x + 1 if direction == "R" else x - 1 if direction == "L" else x
        y_chk = y + 1 if direction == "D" else y - 1 if direction == "U" else y
        
        match(self.grid[y][x]):
            case '.' | '-' | 'x' | '*' | 'L': return True
            case 'T': 
                if self.pl_i.inv in ("x", "🪓"):
                    self.grid[y][x] = '.'
                    self.pl_i.inv = ''
                    return True
                elif self.pl_i.inv in ("*", "🔥"):
                    self.scorch(y, x)
                    self.pl_i.inv = ''
                    return True
                return False
            case '~':
                self.outcome = 2
                return True       
            case 'R':
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
                self.mushrooms += 1
                if self.mushrooms == self.win_condition:
                    self.outcome = 1
                self.grid[y][x] = '.'
                return True

def read_stage_file(stage_file): # Returns player location as well as array-fied stage file
    f = open(stage_file)
    r, c = (int(i) for i in f.readline().split())
    
    player_found = False
    player_x, player_y = 0, 0

    stage = [list(row) for row in f.read().split('\n')]

    for row in stage:
        for unit in row:
            if unit == 'L':
                player_found = True
                break
            elif not player_found:
                player_x += 1

        if not player_found:
            player_x = 0
            player_y += 1
        else:
            break

    return (player_x+1, player_y+1), stage

def main_menu(stage_file, moves, output_file):
    if not stage_file:
        stage_file = "stage-files/stage-file-default.txt"

    player_location, stage = read_stage_file(stage_file)

    lara = Player(*player_location)
    gs1 = Stage_1(stage, lara)
    
    skipped = False
    first = True
    
    if moves:
        for move in moves:
            a = move
            skipped = True if a.upper() == "E" else False
            
            gs1.move(a, gs1.pl_i.y, gs1.pl_i.x)
            first = False
    else:
        while(not (skipped or gs1.outcome)):
            gs1.clear_modify(gs1.grid, first)
        
            a = input(f"\nWelcome to the Main Menu of \"Shroom Runner!\" \n\n[Controls]\n1. U - Move Up\n2. D - Move Down\n3. L - Move Left\n4. R - Move Right\n5. P - Pick Up Item\n6. ! - Reset Stage\n\n[i] Number of Mushrooms Collected: {gs1.mushrooms}\n[i] Currently Holding: {"".join(gs1.pl_i.inv)}\n\nEnter moves: ")
            skipped = True if a.upper() == "E" else False
            
            gs1.move(a, gs1.pl_i.y, gs1.pl_i.x)
            first = False
        else:
            if not skipped:
                gs1.clear_modify(gs1.grid, False)
                
                print("\nYou won!" if gs1.outcome == 1 else "\nYou lost!")
                print(f"Number of Mushrooms Collected: {gs1.mushrooms}")

    if output_file:
        with open(output_file, "w") as file:
            if gs1.outcome == 1:
                file.write("CLEAR \n")
            else:
                file.write("NOT CLEAR \n")

            file.write("\n".join(("".join(i) for i in gs1.grid)))
            
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="Returns the results of the game in a text file")
    parser.add_argument("-m", "--move", help="String of player moves")
    parser.add_argument("-f", "--stage", help="Use a stage file")

    args = parser.parse_args()

    main_menu(args.stage, args.move, args.output)
        
main()