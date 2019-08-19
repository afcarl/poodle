import pytest
from poodle import *
from poodle.arithmetic import *
import poodle.problem

class Obj(Object):
    type: "ObjType"
    count: int
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

@planned
def findNonNegativeIngeger(i: int, o: Obj):
    assert i > 0 and i == 1
    o.value2 = i

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
    for p in schedule([subValues], space=globals(), goal=goal(cobj2.value2==1)): p

def test_integers_parameters():
    cobj1.type = TYPE_2
    cobj1.value2 = 0
    cobj1.count = 1
    for p in schedule([
        findNonNegativeIngeger], 
        space=globals(), 
        goal=goal(cobj1.value2==1)): p

def test_math_sub_multigoal():

    cobj1.type = TYPE_2
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
  
    # debug_plan([subValues], space=globals(), goal=goal(cobj2.value2==1), plan=[subValues])
    for p in schedule([subValues], space=globals(), goal=goal(cobj2.value2==1 and cobj1.type==TYPE_2)): p
    
@pytest.mark.skip(reason="TODO")
def test_isolation():

    cobj1.type = TYPE_2
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
  
    # debug_plan([subValues], space=globals(), goal=goal(cobj2.value2==1), plan=[subValues])
    try:
        for p in schedule([subValues], space=globals(), goal=goal(cobj2.value2==1 and cobj.type==TYPE_2)): p
    except:
        pass
    for p in schedule([subValues], space=globals(), goal=goal(cobj2.value2==1 and cobj1.type==TYPE_2)): p

def test_math_add():

    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
    
    # debug_plan([addValues], space=globals(), goal=Select(cobj2.count==3), plan=[addValues])
    # TODO: these two combined do not work
    for p in schedule([addValues], space=globals(), goal=goal(cobj1.count==3)): p
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
    # debug_plan([addIfGreater], space=globals(), goal=goal(cobj1.count==2), plan=[addIfGreater])
    for p in schedule([addIfGreater], space=globals(), goal=goal(cobj2.count==2)): p

def test_debugging_formally_executes():
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    assert debug_plan([addIfGreater], space=globals(), goal=goal(cobj1.count==2), plan=[addIfGreater])
 
@planned
def addComplecIneq(o1: Obj, o2: Obj):
    assert o1.count + o2.count > o1.value2 - o2.value2
    o1.count = o1.count - o2.count

def test_advanced_multi_add_inequality():
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    for p in schedule([addComplecIneq], space=globals(), goal=goal(cobj2.count==2)): p


class ProblemExample(poodle.problem.Problem):
    @planned
    def addComplecIneq(self, o1: Obj, o2: Obj):
        assert o1.count + o2.count > o1.value2 - o2.value2
        o1.count = o1.count - o2.count
    def problem(self):
        self.cobj1 = self.addObject(Obj())
        self.cobj2 = self.addObject(Obj())

        self.cobj1.type = TYPE_1 # test for recursive object imports
        self.cobj1.value2 = 1
        self.cobj1.count = 1

        self.cobj2.type = TYPE_2
        self.cobj2.value2 = 2
        self.cobj2.count = 3
    def goal(self):
        return self.cobj2.count == 2

def test_class_and_recursive_object_import():
    p = ProblemExample()
    p.run()
    for a in p.plan: a


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
    
    