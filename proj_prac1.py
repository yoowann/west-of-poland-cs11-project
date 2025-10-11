import sys

class Player():
    def __init__(self, x, y, inv = []):
        self.x = x - 1
        self.y = y - 1
        self.inv = inv
        
    def add(self, item):
        if self.inv:
            print(f"{self.name} has item already:\n{self.inv}")
        else:
            self.inv.append(item)
 
class Stage_1():
    def __init__(self, grid, pl_i):
        self.grid = grid
        self.pl_i = pl_i
        self.grid[self.pl_i.y][self.pl_i.x] = "L"
        self.outcome = 0
        self.mushrooms = 0
        self.win_condition = sum([sum(1 if b == "+" else 0 for b in a) for a in self.grid])
        self.paved = False
        
    def move(self, move_sequence, y, x):
        for _ in move_sequence:
            if _.upper() in ("U", "D", "L", "R"):
                if self.mushrooms == self.win_condition: self.outcome = 1
                self.pl_i.x += 1 if (_ == "R" and self.pl_i.x < len(self.grid[0]) - 1 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else -1 if (_ == "L" and self.pl_i.x > 0 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else 0
                self.pl_i.y += 1 if (_ == "D" and self.pl_i.y < len(self.grid) - 1 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else -1 if (_ == "U" and self.pl_i.y > 0 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else 0
            else:
                self.pl_i.x = x
                self.pl_i.y = y
                return
        else:
            if self.mushrooms == self.win_condition: self.outcome = 1
            self.grid[y][x] = "." if not self.paved else "-"
            self.paved = True if self.grid[self.pl_i.y][self.pl_i.x] == "-" else False 
            self.grid[self.pl_i.y][self.pl_i.x] = "L"
        
    def clear_modify(self, new_grid, first):
        if not first:
            for _ in range(len(self.grid) + 14):
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear line from cursor to end`
        
        for line in new_grid:
            sys.stdout.write("".join(line) + "\n")
        sys.stdout.flush()
        
    def analyze(self, direction, x, y):
        x += 1 if direction == "R" and self.pl_i.x < len(self.grid[0]) - 1 else -1 if direction == "L" and self.pl_i.x > 0 else 0
        y += 1 if direction == "D" and self.pl_i.y < len(self.grid) - 1 else -1 if direction == "U" and self.pl_i.y > 0 else 0
        x_chk = x + 1 if direction == "R" else x - 2 if direction == "L" else x
        y_chk = y + 1 if direction == "D" else y - 2 if direction == "U" else y
        
        match(self.grid[y][x]):
            case '.': return True
            case '-': return True
            case 'L': return True
            case 'T': return False
            case '~':
                self.outcome = 2
                return False       
            case 'R':
                if self.grid[y_chk][x_chk] == '.':
                    self.grid[y_chk][x_chk] = 'R'
                    self.grid[y][x] = '.'
                    return True
                elif self.grid[y_chk][x_chk] == '~':
                    self.grid[y_chk][x_chk] = '-'
                    self.grid[y][x] = '.'
                    return True
                else:
                    return False
            case '+':
                self.mushrooms += 1
                self.grid[y][x] = '.'
                return True
                           
def main_menu():
    lara = Player(2, 3)
    gs1 = Stage_1([
        ["T", "T", "T", "T", "T", "T", "T"],
        ["T", ".", "R", ".", "R", ".", "T"],
        ["T", ".", "R", ".", "R", ".", "T"],
        ["T", ".", ".", "~", ".", ".", "T"],
        ["T", ".", "+", ".", ".", ".", "T"],
        ["T", ".", ".", "+", ".", ".", "T"],
        ["T", "T", "T", "T", "T", "T", "T"],
        ], lara)
    skipped = False
    first = True
    
    while(not (skipped or gs1.outcome)):
        gs1.clear_modify(gs1.grid, first)
       
        a = input(f"\nWelcome to the Main Menu of \"Shroom Runner!\" \n\n[Controls]\n1. U - Move Up\n2. D - Move Down\n3. L - Move Left\n4. R - Move Right\n5. P - Pick Up Item\n6. ! - Reset Stage\n\n[i] Number of Mushrooms Collected: {gs1.mushrooms}\n\nEnter moves: ")
        skipped = True if a == "E" else False
        
        gs1.move(a, gs1.pl_i.y, gs1.pl_i.x)
        first = False
    else:
        if not skipped:
            gs1.clear_modify(gs1.grid, False)
            
            print("\nYou won!" if gs1.outcome == 1 else "\nYou lost!")
        
def main():
    main_menu()
        
main()

'''
STAGE DOCUMENTATION

    #Water Test
    gs1 = Stage_1([
        ["T", "T", "T", "T", "T", "T", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", "~", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", "T", "T", "T", "T", "T", "T"],
        ], lara)
        
    #Rock Test
    gs1 = Stage_1([
        ["T", "T", "T", "T", "T", "T", "T"],
        ["T", ".", "R", ".", "R", ".", "T"],
        ["T", ".", "R", ".", "R", ".", "T"],
        ["T", ".", ".", "~", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", "T", "T", "T", "T", "T", "T"],
        ], lara)
        
    #Rock and Mushrooms Test
    gs1 = Stage_1([
        ["T", "T", "T", "T", "T", "T", "T"],
        ["T", ".", "R", ".", "R", ".", "T"],
        ["T", ".", "R", ".", "R", ".", "T"],
        ["T", ".", ".", "~", ".", ".", "T"],
        ["T", ".", "+", ".", ".", ".", "T"],
        ["T", ".", ".", "+", ".", ".", "T"],
        ["T", "T", "T", "T", "T", "T", "T"],
        ], lara)
       
    #Maximum Parameter Test 
    gs1 = Stage_1([
        ["T" for i in range(30)],
        *[["T", *["." for j in range(28)], "T"] for k in range(28)],
        ["T" for m in range(30)]
        ], lara)
'''
    