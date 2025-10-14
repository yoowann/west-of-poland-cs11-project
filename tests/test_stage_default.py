import pytest
from Player import Player
from Stage import Stage
from shroom_raider import read_stage_file

try:
    draft = read_stage_file("../stage-files/stage-file-default.txt")
    path = "../stage-files/stage-file-default.txt"
except FileNotFoundError as e:
    path = "./stage-files/stage-file-default.txt"

@pytest.fixture(params=[
    (*read_stage_file(path), "rRuUPPPPPPuDrPPP"),
    (*read_stage_file(path), "rrRlrlrlrlrLLudUuuR"),
    (*read_stage_file(path), "rrRlrlrlrlrLLudUuR"),
    (*read_stage_file(path), "rrRlrPPPPPppppPlrlrlrLLudUuRPPPPPPL"),
    (*read_stage_file(path), "rrRlrPPPPPpGppPlrlrlrLLudUuRPPPPPPL")])
def modified_instance(request):
    stage = Stage(request.param[1], Player(*request.param[0]))
    stage.move(request.param[2], stage.pl.y, stage.pl.x)
    return stage

try:
    correct = read_stage_file("./correct/std-tests.txt", True)
except FileNotFoundError as e:
    correct = read_stage_file("./tests/correct/std-tests.txt", True)

def test_new_stage(modified_instance):
    print("CURRENT")
    for x in modified_instance.grid:
        print(''.join(x))
    for x in correct:
        for y in x:
            print(''.join(y))
        print()
    

    assert modified_instance.grid in correct, f"\nReturned\n{"\n".join("".join(a) for a in modified_instance.grid)} \nInventory:{modified_instance.pl.inv}"
    