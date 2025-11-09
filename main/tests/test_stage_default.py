import pytest, copy
from main.Player import Player
from main.Stage import Stage
from main.Processing import read_stage_file

try:
    player, path = read_stage_file("../stage-files/stage-file-default.txt")
except FileNotFoundError as e:
    try:
        player, path = read_stage_file("./stage-files/stage-file-default.txt")
    except FileNotFoundError as f:
        player, path = read_stage_file("./main/stage-files/stage-file-default.txt")

# test_cases takes in the moves the user wants to include in the unit tests.
# deepcopies of the original path variable from the try-except block above is duplicated,
# along with the player information and moves in a comprehension

# To add a test case, add a new string of moves here
test_cases = ["dDwWPPPPPPwSdPPP", "ddDadadadadAAwsWwwD", "ddDadadadadAAwsWwD",
    "ddDadPPPPPppppPadadadAAwsWwaaSsSdPAa", "WWDddDPSssAPWPpGppPadaZX!^lMOVEdAAwsWwDPPPPPPA",
    "sAApaaDdDdSssSSsSddWwWwwwPwAawWwWPpppWP", "WWsPpPSSDdPppPPpDdAaaAWWWWWwwPPpDSWA",
    "DddDAdaApPpPWDWSddWApPpDDSssSssSdAWw", "SAAPSDDWSWSWSADdDwPPpPWaaAAWsAAwWWWWP",
    "wWAaAASsSDWWwwwWpPppPPPpWdDWWwPPPSAD", "AWDAAASSDPppPDddDPdDAaPsSdwwDAaAaWwwW",
    "DddSWwWWDDSSAAWAswSDsswsddsAASdSWSDs", "AwWDSSWWaasWDSwsSDSwWssdWASDPpPpsWwWw",
    "SaAPaWADSdPDdDddWwwAaSAaaaAwaSDdSSddDPDdWWWWWwwwWWAaAaSsssSsP", "SddPWaaAWDDWDssSASd"
]
#test cases 3, 13 share the same case
#test cases 1, 11 share the same case

@pytest.fixture(params=[
    (copy.deepcopy(path), player, moves) for moves in test_cases
])
def modified_instance(request):
    stage = Stage(request.param[0], Player(*request.param[1]))
    stage.move(request.param[2], stage.pl.y, stage.pl.x)
    return stage

try:
    correct = read_stage_file("./correct/std-tests.txt", True)
except FileNotFoundError as e:
    try:
        correct = read_stage_file("./tests/correct/std-tests.txt", True)
    except FileNotFoundError as f:
        correct = read_stage_file("./main/tests/correct/std-tests.txt", True)

def test_new_stage(modified_instance):
    
    # print("CURRENT")
    # for x in modified_instance.grid:
    #     print(''.join(x))
    # for x in correct:
    #     for y in x:
    #         print(''.join(y))
    #     print()

    assert modified_instance.grid in correct, f"\nReturned\n{"\n".join("".join(a) for a in modified_instance.grid)} \nInventory:{modified_instance.pl.inv}"
    