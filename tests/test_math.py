import pytest
from poodle import *
from poodle.arithmetic import *
import poodle.problem
from poodle.schedule import SchedulingError

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
    return "HI"

cobj1 = Obj()
cobj2 = Obj()

def test_math_sub():

    cobj1.type = TYPE_2
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
  
    # debug_plan([subValues], space=globals(), goal=lambda:(cobj2.value2==1), plan=[subValues])
    # for p in schedule([subValues], space=globals(), goal=lambda:(cobj2.value2==1)): p
    xschedule([subValues], space=globals(), goal=lambda:(cobj2.value2==1)) == "DONE"

def test_integers_parameters():
    cobj1.type = TYPE_2
    cobj1.value2 = 0
    cobj1.count = 1
    for p in schedule([
        findNonNegativeIngeger], 
        space=globals(), 
        goal=lambda:(cobj1.value2==1)): p

def test_exec_integers_parameters():
    cobj1.type = TYPE_2
    cobj1.value2 = 0
    cobj1.count = 1
    assert xschedule([ findNonNegativeIngeger], space=globals(), 
        goal=lambda:(cobj1.value2==1)) == "HI"


def test_math_sub_multigoal():

    cobj1.type = TYPE_2
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
  
    # debug_plan([subValues], space=globals(), goal=lambda:(cobj2.value2==1), plan=[subValues])
    assert xschedule([subValues], space=globals(), goal=lambda:(cobj2.value2==1 and cobj1.type==TYPE_2))=="DONE"
    
@pytest.mark.skip(reason="TODO")
def test_isolation():

    cobj1.type = TYPE_2
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
  
    # debug_plan([subValues], space=globals(), goal=lambda:(cobj2.value2==1), plan=[subValues])
    try:
        for p in schedule([subValues], space=globals(), goal=lambda:(cobj2.value2==1 and cobj.type==TYPE_2)): p
    except:
        pass
    for p in schedule([subValues], space=globals(), goal=lambda:(cobj2.value2==1 and cobj1.type==TYPE_2)): p

def test_math_add():

    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 1
    
    # debug_plan([addValues], space=globals(), goal=Select(cobj2.count==3), plan=[addValues])
    # TODO: these two combined do not work
    assert xschedule([addValues], space=globals(), goal=lambda:(cobj1.count==3)) == "DONE"
    # print(xschedule([addValues], space=globals(), goal=lambda:(cobj1.count==3)))

@planned
def addIfGreater(o1: Obj, o2: Obj):
    assert o1.count > o2.count
    o1.count = o1.count - o2.count
    return "DONE"

def test_greater_than():
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    # debug_plan([addIfGreater], space=globals(), goal=lambda:(cobj1.count==2), plan=[addIfGreater])
    assert xschedule([addIfGreater], space=globals(), goal=lambda:(cobj2.count==2)) == "DONE"

def test_debugging_formally_executes():
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    assert debug_plan([addIfGreater], space=globals(), goal=lambda:(cobj1.count==2), plan=[addIfGreater])
 
def test_complex_integer_comp():
    @planned
    def findNonNegativeIngegerObj(o: Obj):
        assert o.count > -1
        o.value2 = o.count
        return "DONE"
    cobj1.type = TYPE_1
    cobj1.value2 = 0
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = -1
    assert xschedule([findNonNegativeIngegerObj], space=[cobj1, cobj2], goal=lambda:(cobj1.value2==1)) == "DONE"


@planned
def addComplecIneq(o1: Obj, o2: Obj):
    assert o1.count + o2.count > o1.value2 - o2.value2
    o1.count = o1.count - o2.count
    return "DONE"

def test_advanced_multi_add_inequality_timout():
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    ok = False
    try:
        for p in schedule([addComplecIneq], space=globals(), goal=lambda:(cobj2.count==2), sessionName="test_advanced_multi_add_inequality", timeout=2): p
    except SchedulingError:
        ok = True
    assert ok

def test_advanced_multi_add_inequality():
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    assert xschedule([addComplecIneq], space=globals(), goal=lambda:(cobj2.count==2), sessionName="test_advanced_multi_add_inequality", timeout=60) == "DONE"



class ProblemExample(poodle.problem.Problem):
    @planned
    def addComplecIneq(self, o1: Obj, o2: Obj):
        assert o1.count + o2.count > o1.value2 - o2.value2
        o1.count = o1.count - o2.count
        return "DONE"
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

def test_math_add_int():
    @planned
    def addComplecIneq_num(o1: Obj, o2: Obj):
        assert o1.count + 1 > o1.value2 - o2.value2
        o1.count = o1.count - o2.count
        return "DONE"
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    assert xschedule([addComplecIneq_num], space=globals(), goal=lambda:(cobj2.count==2)) == "DONE"

def test_math_multi_eq():
    @planned
    def addComplecIneq_num(o1: Obj, o2: Obj):
        assert o1.count == 3
        assert o1.value2 == 2
        o1.count = 4
        return "DONE"
    cobj1.type = TYPE_1
    cobj1.value2 = 1
    cobj1.count = 1

    cobj2.type = TYPE_2
    cobj2.value2 = 2
    cobj2.count = 3
    assert xschedule([addComplecIneq_num], space=globals(), goal=lambda:(cobj2.count==4)) == "DONE"

@planned
def plus1(o1: Obj):
    assert o1.type == TYPE_1
    o1.count += 1
    return "DONE"
    
@pytest.mark.skip(reason="no way of currently testing this")
def test_math_plus1():
    assert xschedule([plus1], space=globals(), goal=(cobj1.count==3)) == "DONE"
    
@planned
def check3(obj: Obj):
    assert obj.count == 3
    return "DONE"

@pytest.mark.skip(reason="no way of currently testing this")
def test_math_add_funcgoal():
    xschedule([addValues], space=globals(), exit=check3)
    
    