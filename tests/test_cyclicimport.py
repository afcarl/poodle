import poodle
import tests.cyclic1
import tests.cyclic2

def test_cyclic_import_nodot():
    o = tests.cyclic1.CTest1()
    assert o.o._value == tests.cyclic2.CTest2

def test_cyclic_import_dot():
    o = tests.cyclic1.DCTest1()
    assert o.o._value == tests.cyclic2.DCTest2