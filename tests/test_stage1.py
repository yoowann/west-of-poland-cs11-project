import pytest, sys
from proj_prac1 import Player, Stage_1, read_stage_file

try:
    draft = read_stage_file("../stage-files/stage1.txt")
    path = "../stage-files/stage1.txt"
except FileNotFoundError as e:
    path = "./stage-files/stage1.txt"

@pytest.fixture(params=[
    (*read_stage_file(path), "rPRLLRRuRRDDpD"),
    (*read_stage_file(path), "DlRduUpDRlddDRRRr"),
    (*read_stage_file(path), "UUuuuuuURRrDDDdddUUUdPUU"),
    (*read_stage_file(path), "RpUUDrRDpDDLLRRDDRLUuUUulDDldRRrrRrPp"),
    (*read_stage_file(path), "RpUUDrRDpDZLLRRDDRLUuUUulDDldRRrrRrPp")])
def modified_instance(request):
    stage = Stage_1(request.param[1], Player(*request.param[0]))
    stage.move(request.param[2], stage.pl_i.y, stage.pl_i.x)
    return stage

try:
    correct = read_stage_file("./correct/st1-tests.txt", True)
except FileNotFoundError as e:
    correct = read_stage_file("./tests/correct/st1-tests.txt", True)

def test_new_stage(modified_instance):
    assert modified_instance.grid in correct, f"\nReturned\n{"\n".join("".join(a) for a in modified_instance.grid)} \nInventory:{modified_instance.pl_i.inv}"
        
        
        