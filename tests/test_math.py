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
    return "DONE"
    
@planned
def subValues(o1: Obj, o2: Obj):
    assert o1.type == TYPE_2
    o1.value2 -= o2.value2
    return "DONE"


cobj1 = Obj()
cobj2 = Obj()
def test_math_sub():

    cobj1.type = TYPE_2
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
  
    # debug_plan([subValues], space=globals(), goal=goal(cobj2.value2==1), plan=[subValues])
    for p in schedule([subValues], space=globals(), goal=goal(cobj2.value2==1)): print(p)


def test_math_add():

    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
    
    # debug_plan([addValues], space=globals(), goal=Select(cobj2.count==3), plan=[addValues])
    # TODO: these two combined do not work
    for p in schedule([addValues], space=globals(), goal=goal(cobj1.count==3)): print(p)
    # print(xschedule([addValues], space=globals(), goal=goal(cobj1.count==3)))

@planned
def addIfGreater(o1: Obj, o2: Obj):
    assert o1.count > o2.count
    o1.count = o1.count - o2.count

def test_greater_than():
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    for p in schedule([addIfGreater], space=globals(), goal=goal(cobj1.count==2)): print(p)

@planned
def plus1(o1: Obj):
    assert o1.type == TYPE_1
    o1.count += 1
    
@pytest.mark.skip(reason="no way of currently testing this")
def test_math_plus1():
    xschedule([plus1], space=globals(), goal=(cobj1.count==3))
    
@planned
def check3(obj: Obj):
    assert obj.count == 3

@pytest.mark.skip(reason="no way of currently testing this")
def test_math_add_funcgoal():
    xschedule([addValues], space=globals(), exit=check3)
    
    