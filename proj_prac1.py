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
            
    def clear_inv(self):
        if not self.inv:
            print(f"Inventory is already empty")
        else:
            self.inv.pop()
 
class Stage_1():
    def __init__(self, grid, pl_i, outcome):
        self.grid = grid
        self.pl_i = pl_i
        self.grid[self.pl_i.y][self.pl_i.x] = "L"
        self.outcome = 0
        
    def move(self, move_sequence, y, x):
        for _ in move_sequence:
            if _.upper() in ("U", "D", "L", "R"):
                self.pl_i.x += 1 if (_ == "R" and self.pl_i.x < len(self.grid[0]) - 1 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else -1 if (_ == "L" and self.pl_i.x > 0 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else 0
                self.pl_i.y += 1 if (_ == "D" and self.pl_i.y < len(self.grid) - 1 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else -1 if (_ == "U" and self.pl_i.y > 0 and self.analyze(_, self.pl_i.x, self.pl_i.y) and not self.outcome) else 0
            else:
                self.pl_i.x = x
                self.pl_i.y = y
                if move_sequence != "E": print("Broken input")
                return
        else:
            self.grid[y][x] = "."
            self.grid[self.pl_i.y][self.pl_i.x] = "L"
        
    def clear_modify(self, new_grid):
        for _ in range(len(self.grid) + 7):
            sys.stdout.write("\033[F")  # Move cursor up one line
            sys.stdout.write("\033[K")  # Clear line from cursor to end
        
        for line in new_grid:
            sys.stdout.write("".join(line) + "\n")
        sys.stdout.flush()
        
    def analyze(self, direction, x, y):
        x += 1 if direction == "R" and self.pl_i.x < len(self.grid[0]) - 1 else -1 if direction == "L" and self.pl_i.x > 0 else 0
        y += 1 if direction == "D" and self.pl_i.y < len(self.grid) - 1 else -1 if direction == "U" and self.pl_i.y > 0 else 0
        
        match(self.grid[y][x]):
            case '.': return True
            case 'L': return True
            case 'T': return False
            case '~':
                self.outcome = 2
                return False        
          
def main_menu():
    lara = Player(2, 3)
    gs1 = Stage_1([
        ["T", "T", "T", "T", "T", "T", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", "~", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", "T", "T", "T", "T", "T", "T"],
        ], lara, 0)
    skipped = False
    
    while(not (skipped or gs1.outcome)):
        gs1.clear_modify(gs1.grid)
       
        a = input("\nWelcome to the Main Menu of \"Shroom Runner!\" \n[1] Play\n[2] Options\n\nEnter moves: ")
        skipped = True if a == "E" else False
        
        gs1.move(a, gs1.pl_i.y, gs1.pl_i.x)
    else:
        if not skipped:
            gs1.clear_modify(gs1.grid)
            
            print("\nYou won!" if gs1.outcome == 1 else "\nYou lost!")
        
def main():
    main_menu()
        
main()

'''
STAGE DOCUMENTATION

    # Water Test
    gs1 = Stage_1([
        ["T", "T", "T", "T", "T", "T", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", "~", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", ".", ".", ".", ".", ".", "T"],
        ["T", "T", "T", "T", "T", "T", "T"],
        ], lara, 0)
       
    # Maximum Parameter Test 
    gs1 = Stage_1([
        ["T" for i in range(30)],
        *[["T", *["." for j in range(28)], "T"] for k in range(28)],
        ["T" for m in range(30)]
        ], lara, 0)
'''
    
