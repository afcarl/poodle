import pytest
from poodle import *
from poodle.schedule import _objwalk, _get_recursive_objects
from poodle.arithmetic import logSparseIntegerFactory, LogSparseInteger
from typing import Set

def test_objwalk():
    class OT(Object):
        a: int
        b: "Newo"
        default: "Newo"
    
    class Newo(Object):
        t: OT
        d: int
        default_n: OT
    
    n = Newo()
    n.d=2
    t = OT()
    t.b=n

    assert [p[0] for p in _objwalk(t)] == \
        [(('a',)), (('b',)), (('b', 'd')), (('b', 'default_n') ), (('b', 't') ), (('default',) )]

def test_recursive_obj():
    class OT(Object):
        a: int
        b: "Newo"
        default: "Newo"
    
    class Newo(Object):
        t: OT
        d: int
        default_n: OT
    
    n = Newo()
    n.d=2
    t = OT()
    t.b=n

    ro = _get_recursive_objects(t)
    assert n in ro and \
        logSparseIntegerFactory.get(2) in ro and\
        t in ro and\
        OT._none_object in ro and\
        LogSparseInteger._none_object in ro and\
        Newo._none_object in ro

def test_integer_set_obj():
    class S(Object):
        i: Set[int]
        r: int
    
    @planned
    def check_int_in_set(o: S, i: int):
        assert i in o.i
        o.r = i

    s=S()
    s.i.add(2)
    s.i.add(1)

    for p in schedule([check_int_in_set], space=[s], goal=lambda:(s.r==1),
                sessionName="test_integer_set_obj"): p

def test_integer_set_obj_forward_ref_method():
    class S(Object):
        i: Set[int]
        r: int
    
    @planned
    def check_int_in_set(o: "S", i: int):
        assert i in o.i
        o.r = i

    s=S()
    s.i.add(2)
    s.i.add(1)

    for p in schedule([check_int_in_set], space=[s], goal=lambda:(s.r==1),
                sessionName="test_integer_set_obj"): p
@pytest.mark.skip(reason="TODO")
def test_integer_set():
    class S(Object):
        i: Set[int]
        r: int
    
    @planned
    def check_int_in_set(o: S, i: int):
        assert 1 in o.i
        o.r = i

    s=S()
    s.i.add(2)
    s.i.add(1)

    for p in schedule([check_int_in_set], space=[s], goal=lambda:(s.r==1)): p

def test_normal_numeric_asserts():
    class TestObj(Object):
        i1: int
        i2: int
    o = TestObj()
    o.i1 = 1
    o.i2 = 1
    assert o.i1 == 1
    assert o.i2 == 1

# def test_numeric_ineq_asserts():
#     class TestObj(Object):
#         i1: int
#         i2: int
#     o = TestObj()
#     o.i1 = 1
#     o.i2 = 1
#     assert o.i1 > 0
#     assert o.i2 >= 1

