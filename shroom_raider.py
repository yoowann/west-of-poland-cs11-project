import argparse

from Player import Player
from Stage import Stage
from Processing import read_stage_file

def main_menu(stage_file, moves, output_file):
    if not stage_file:
        stage_file = "stage-files/stage-file-default.txt"

    player_location, stage = read_stage_file(stage_file)
    level = Stage(stage, Player(*player_location))
    
    skipped = False
    first = True
    
    if moves:
        for move in moves:
            a = move
            skipped = True if a.upper() == "E" else False
            
            level.move(a, level.pl.y, level.pl.x)
            first = False
    else:
        while(not (skipped or level.outcome)):
            level.clear_modify(level.grid, first)
        
            a = input(f"\nWelcome to the Main Menu of \"Shroom Runner!\" \n\n[Controls]\n1. U - Move Up\n2. D - Move Down\n3. L - Move Left\n4. R - Move Right\n5. P - Pick Up Item\n6. ! - Reset Stage\n\n[i] Number of Mushrooms Collected: {level.mushrooms} 🍄\n[i] Currently Holding: {level.pl.inv}\n\nEnter moves: ")
            skipped = True if a.upper() == "E" else False
            
            level.move(a, level.pl.y, level.pl.x)
            first = False
        else:
            if not skipped:
                level.clear_modify(level.grid, False)
                
                print("\nYou won!" if level.outcome == 1 else "\nYou lost!")
                print(f"Number of Mushrooms Collected: {level.mushrooms} 🍄")

    if output_file:
        with open(output_file, "w") as file:
            if level.outcome == 1:
                file.write("CLEAR \n")
            else:
                file.write("NOT CLEAR \n")

            file.write("\n".join(("".join(i) for i in level.grid)))
            
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="Returns the results of the game in a text file")
    parser.add_argument("-m", "--move", help="String of player moves")
    parser.add_argument("-f", "--stage", help="Use a stage file")

    args = parser.parse_args()

    main_menu(args.stage, args.move, args.output)
        
if __name__ == "__main__":
    main()