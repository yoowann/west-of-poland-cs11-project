import os

from termcolor import colored

def read_stage_file(stage_file, testing = False): # Returns player location as well as array-fied stage file
    '''
    Reads a file and returns 1 of 2 objects:
    1. a pair tuple of ints and grid (2D list of str)
        - Activates when testing = False and is intended to read a .txt file containing 1 grid.
    2. a list of grids (2D lists of str) - if testing is True
        - Activates when testins = True and is intended to read a .txt file containing multiple grids.
    '''
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

def determine_if_high_score(new_score, stage_name):
    score_file = "scoreboard/score-" + stage_name.split("\\")[-1]
    is_high_score = False

    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            leaderboard = [(i.split()) for i in f.readlines()]

            current_top_score = int(leaderboard[0][0])
            if new_score <= current_top_score:
                is_high_score = True 
    else:
        is_high_score = True

    return is_high_score

def update_scoreboard(new_score, player_name, stage_name):
    score_file = "scoreboard/score-" + stage_name.split("\\")[-1]

    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            leaderboard = [(i.split()) for i in f.readlines()]
            leaderboard.append((new_score, player_name))
            leaderboard.sort(key=lambda x: int(x[0]))

        with open(score_file, 'w') as f:
            f.writelines([f'{i[0]} {" ".join(i[1:])}\n' for i in leaderboard])
    else:
        x = open(score_file, "x")
        
        with open(score_file, 'w') as f:
            f.write(f'{new_score} {player_name}\n')
 
def print_scoreboard(stage_name):
    score_file = "scoreboard/score-" + stage_name.split("\\")[-1]

    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            leaderboard = f.readlines()
            leaderboard.sort(key=lambda x: int(x[0]))

        rank = 1
        print("\n" + f"{colored("Leaderboard".center(31), "yellow", attrs=["bold"])}" + "\nRank |       Name       | Score  ")
        for i in leaderboard:
            dummy = i.split()
            score, name = dummy[0], " ".join(dummy[1:])

            rank_string = f"[{rank}]".ljust(5)
            name_string = f"{name[:13] + ("..." if len(name) > 14 else "")}".center(16)
            print(f"{rank_string}| {name_string} | " + f"{score}".center(5))
            rank += 1


            
