from poodle import *

def test_ingeritance():
    class TestObjBase(Object):
        c1: int

    class TestObjInherit(TestObjBase):
        c2: int

    obj = TestObjInherit()

    assert hasattr(obj, "c1")

