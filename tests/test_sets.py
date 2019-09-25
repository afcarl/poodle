from typing import Set
from poodle import Object, xschedule

class Obj(Object):
    pass

class SetTest(Object):
    a: Set[Obj]
    done: bool

class IntSetTest(Object):
    i: Set[int]

class StrSetTest(Object):
    s: Set[str]

def test_py_o_set_init():
    o = Obj()
    a = SetTest()
    a.a.add(o)
    a.done = False

    def done_if_in(o1: SetTest):
        assert o in o1.a
        o1.done = True
        return True

    assert xschedule([done_if_in], [a], goal=lambda: a.done==True)
