import sys
import argparse

from Player import Player
from Stage import Stage

def read_stage_file(stage_file, testing = False): # Returns player location as well as array-fied stage file
    f = open(stage_file)
    if not testing: r, c = (int(i) for i in f.readline().split())
    
    player_found = False
    player_x, player_y = 0, 0

    if not testing:
        stage = [list(row) for row in f.read().split('\n')]
    else:
        stages = [[list(row) for row in section.split('\n')] for section in f.read().split('\n\n')]
        return stages

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

    return (player_x, player_y), stage

def main_menu(stage_file, moves, output_file):
    if not stage_file:
        stage_file = "stage-files/stage-file-default.txt"

    player_location, stage = read_stage_file(stage_file)

    lara = Player(*player_location)
    gs1 = Stage(stage, lara)
    
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
        
            a = input(f"\nWelcome to the Main Menu of \"Shroom Runner!\" \n\n[Controls]\n1. U - Move Up\n2. D - Move Down\n3. L - Move Left\n4. R - Move Right\n5. P - Pick Up Item\n6. ! - Reset Stage\n\n[i] Number of Mushrooms Collected: {gs1.mushrooms} 🍄\n[i] Currently Holding: {gs1.pl_i.inv}\n\nEnter moves: ")
            skipped = True if a.upper() == "E" else False
            
            gs1.move(a, gs1.pl_i.y, gs1.pl_i.x)
            first = False
        else:
            if not skipped:
                gs1.clear_modify(gs1.grid, False)
                
                print("\nYou won!" if gs1.outcome == 1 else "\nYou lost!")
                print(f"Number of Mushrooms Collected: {gs1.mushrooms} 🍄")

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
        
if __name__ == "__main__":
    main()