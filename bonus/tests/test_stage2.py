import pytest, copy
from Stage import Stage
from Player import Player
from Processing import read_stage_file

try:
    player, path = read_stage_file("../stage-files/stage2.txt")
except FileNotFoundError as e:
    player, path = read_stage_file("./stage-files/stage2.txt")

# test_cases takes in the moves the user wants to include in the unit tests.
# deepcopies of the original path variable from the try-except block above is duplicated,
# along with the player information and moves in a comprehension

# To add a test case, add a new string of moves here
test_cases = ["DdDdSAapaAAPs", "SPsSSPSssSSDSddDdDdP", "SPDddSSDDDDdAWwDsAsDDDd",
    "AaWwWPwWDDdDdPAaAaASSsDdDPPpppPpDssD", "SPwDdSssssDddDSdssDdddDdDSSa",
    "SPSSSPSSSSSDSdddddDAAAAAAWAaaWWWWWWwwwwwWDddDDPSSSDdWDDDddWDW", "DPDPSdddWWssAAAaaPSsSPW",
    "WASDWASDWASDSPDDDDDddddDDdddDDppPPPAAWSSassdasw", "aaWPWWDDDddPWDdddddDDDdddDSaPss", 
    "SPSSSPSssssDSDDDdddAAaaAAWaAAWwWWwWwwwWwwDdDdDPWDDDDDDDDDDSAPsaaAsAAAsSSSDdDdd",
    "SpDDDddSsDDdaWWdSAsDdawWAwWaAdDDddwDPWWpWssS", "SpSSsPSssSsDsdDDDddAAAaaAWAaAWWWwwwwWwWwwPwwDddDDPW",
    "DDsDddWWdddDdWDwPsAsAAAaASSsSDSsSDwWwDWwD", "WAaPssSSsDdpWSaASsSsDDwwWWSsSsAAWwWwwWWDdPSsDSAASSsssS",
    "WAAPddDDSsSsSSDddaAAWwWWAAPDDssSSDDDSWDSDAWWWwWwDDwwwWwa"
]

@pytest.fixture(params=[
    (copy.deepcopy(path), player, moves) for moves in test_cases
])
def modified_instance(request):
    stage = Stage(request.param[0], Player(*request.param[1]))
    stage.move(request.param[2], stage.pl.y, stage.pl.x)
    return stage


try:
    correct = read_stage_file("./correct/st2-tests.txt", True)
except FileNotFoundError as e:
    correct = read_stage_file("./tests/correct/st2-tests.txt", True)

def test_new_stage(modified_instance):
    
    # print("OUTPUT WAS:")
    # for row in modified_instance.grid:
    #     print(''.join(row))
    # for x in correct:
    #     for row in x:
    #         print(''.join(row))
    #     print()
    
    assert modified_instance.grid in correct, f"\nReturned\n{"\n".join("".join(a) for a in modified_instance.grid)} \nInventory:{modified_instance.pl.inv}"