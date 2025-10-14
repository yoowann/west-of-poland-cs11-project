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