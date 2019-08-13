import pytest
from poodle import *
from poodle.arithmetic import *

class Obj(Object):
    type: "Type"
    count: LogSparseInteger
    value: LogSparseInteger
    
class ObjType(Object):
    pass

TYPE_1 = ObjType()
TYPE_2 = ObjType()

@planned
def addValues(o1: Obj, o2: Obj):
    assert o1.type == TYPE_1
    o1.count += o2.value
    
cobj1 = Obj()
cobj1.type = TYPE_1
cobj1.value = 1
cobj1.count = 1

cobj2 = Obj()
cobj2.type = TYPE_2
cobj2.value = 2
cobj2.count = 1

def test_math_add():
    xschedule([addValues], space=globals(), goal=(cobj2.count==3))
    
@planned
def check3(obj: Obj):
    assert obj.count == 3

@pytest.mark.skip(reason="no way of currently testing this")
def test_math_add_funcgoal():
    xschedule([addValues], space=globals(), exit=check3)
    
    