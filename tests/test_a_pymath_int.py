from poodle import *
import pytest
# pytestmark = pytest.mark.skip("all tests still WIP")

class S1(Object):
    a: int

def test_pyadd_internal_eq():

    x = S1()
    y = S1()

    x = S1()
    y = S1()

    x.a = 2
    y.a = 2

    assert (x.a + y.a).poodle_internal__value == 4

def test_pyadd_internal_neq():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 2

    ok = False
    try:
        assert (x.a + y.a).poodle_internal__value == 5
    except AssertionError:
        ok = True
    assert ok

def test_pyadd_py():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 2

    assert x.a + y.a == 4


def test_pyadd_py_neq():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 2

    ok = False
    try:
        assert x.a + y.a == 5
    except AssertionError:
        ok = True
    assert ok


def test_pycmp_obj_eq():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 2

    assert x.a == y.a


def test_pycmp_obj_neq():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 2
    ok = False
    try:
        assert x.a != y.a
    except AssertionError:
        ok = True
    assert ok

def test_py_gt():
    x = S1()
    y = S1()

    x.a = 2
    y.a = 3

    assert x.a < y.a

def test_py_gt_err():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 3

    try:
        assert x.a > y.a
    except AssertionError:
        ok = True
    assert ok

def test_py_gt_num():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 3

    assert x.a > 1


def test_py_gt_num_err():

    x = S1()
    y = S1()

    x.a = 2
    y.a = 3

    try:
        assert x.a > 4
    except AssertionError:
        ok = True
    assert ok

def test_py_iadd_inplace():

    x = S1()

    x.a = 2
    x.a += 1

    assert x.a == 3

def test_py_iadd_err():

    x = S1()

    x.a = 2
    x.a += 1

    ok = False
    try:
        assert x.a == 4
    except AssertionError:
        ok = True
    assert ok

