import pytest
from Stage import Stage
from Player import Player
from shroom_raider import read_stage_file

try:
    draft = read_stage_file("../stage-files/stage3.txt")
    path = "../stage-files/stage3.txt"
except FileNotFoundError as e:
    path = "./stage-files/stage3.txt"

@pytest.fixture(params=[
    (*read_stage_file(path), "RPR")])
def modified_instance(request):
    stage = Stage(request.param[1], Player(*request.param[0]))
    stage.move(request.param[2], stage.pl.y, stage.pl.x)
    return stage

try:
    correct = read_stage_file("./correct/st3-tests.txt", True)
except FileNotFoundError as e:
    correct = read_stage_file("./tests/correct/st3-tests.txt", True)

def test_new_stage(modified_instance):
    for x in correct:
        for row in x:
            print(''.join(row))
        print()
    
    print("OUTPUT WAS:")
    for row in modified_instance.grid:
        print(''.join(row))
    assert modified_instance.grid in correct, f"\nReturned\n{"\n".join("".join(a) for a in modified_instance.grid)} \nInventory:{modified_instance.pl.inv}"
        
        
        