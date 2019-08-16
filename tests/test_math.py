import pytest
from poodle import *
from poodle.arithmetic import *

class Obj(Object):
    type: "ObjType"
    count: LogSparseInteger
    value2: LogSparseInteger
    not_initialized: LogSparseInteger
    not_initialized2: "ObjType"
    
class ObjType(Object):
    pass

TYPE_1 = ObjType()
TYPE_2 = ObjType()

@planned
def addValues(o1: Obj, o2: Obj):
    assert o1.type == TYPE_1
    o1.count += o2.value2
    
cobj1 = Obj()
cobj1.type = TYPE_1
cobj1.value2 = 1
cobj1.count = 1

cobj2 = Obj()
cobj2.type = TYPE_2
cobj2.value2 = 2
cobj2.count = 1

def test_math_add():
    xschedule([addValues], space=globals(), goal=Select(cobj2.count==3))

@planned
def plus1(o1: Obj):
    assert o1.type == TYPE_1
    o1.count += 1
    
@pytest.mark.skip(reason="no way of currently testing this")
def test_math_plus1():
    xschedule([plus1], space=globals(), goal=(cobj2.count==3))
    
@planned
def check3(obj: Obj):
    assert obj.count == 3

@pytest.mark.skip(reason="no way of currently testing this")
def test_math_add_funcgoal():
    xschedule([addValues], space=globals(), exit=check3)
    
    