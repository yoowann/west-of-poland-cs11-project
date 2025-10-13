import pytest, sys
from proj_prac1 import Player, Stage_1, read_stage_file

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
    stage = Stage_1(request.param[1], Player(*request.param[0]))
    stage.move(request.param[2], stage.pl_i.y, stage.pl_i.x)
    return stage

try:
    correct = read_stage_file("./correct/std-tests.txt", True)
except FileNotFoundError as e:
    correct = read_stage_file("./tests/correct/std-tests.txt", True)

def test_new_stage(modified_instance):
    assert modified_instance.grid in correct, f"\nReturned\n{"\n".join("".join(a) for a in modified_instance.grid)} \nInventory:{modified_instance.pl_i.inv}"
    