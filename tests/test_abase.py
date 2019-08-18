import pytest
from poodle import *
from poodle.schedule import _objwalk, _get_recursive_objects
from poodle.arithmetic import logSparseIntegerFactory, LogSparseInteger

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
        
