from poodle import *
import pytest
from poodle.poodle_main import String, stringFactory

class StringCompareTest(Object):
    s: str
    ok: str


def test_two_string_equality():
    s1 = String("test")
    s2 = String("test")
    assert s1 == s2

def test_two_string_equality_fail():
    from poodle.poodle_main import String
    s1 = String("test")
    s2 = String("test2")

    try:
        assert s1 == s2
    except AssertionError:
        return
    raise

def test_String_to_prop_compare():
    from poodle.poodle_main import String
    s1 = String("test")
    o = StringCompareTest()
    o.s = "test"
    assert o.s == s1

def test_String_to_prop_compare_reverse():
    s1 = String("test")
    o = StringCompareTest()
    o.s = "test"
    # print(repr(s1), repr(o.s))
    assert s1 == o.s

def test_String_to_prop_compare_fail():
    s1 = String("test2")
    o = StringCompareTest()
    o.s = "test"
    try:
        assert o.s == s1
    except AssertionError:
        return
    raise

def test_String_to_prop_compare_reverse_fail():
    s1 = String("test")
    o = StringCompareTest()
    o.s = "test2"
    try:
        assert s1 == o.s
    except AssertionError:
        return
    raise

def test_string_compare():
    o = StringCompareTest()
    o.s = "test"
    assert o.s == "test"

def test_string_compare():
    o = StringCompareTest()
    o.s = "test"
    assert "test" == o.s

def test_string_notcompare():
    o = StringCompareTest()
    o.s = "test"
    assert o.s != "test2"

def test_string_notcompare():
    o = StringCompareTest()
    o.s = "test"
    assert not o.s == "test2"

def test_string_notcompare():
    o = StringCompareTest()
    o.s = "test"
    ok = False
    try:
        assert o.s == "test2"
    except AssertionError:
        ok = True
    assert ok

def test_string_dereferencing():
    o = StringCompareTest()
    o.s = "test"
    a = o.s
    assert a == "test"

def test_string_multideref_compare():
    o = StringCompareTest()
    o.s = "test"

    o2 = StringCompareTest()

def test_solve_equality():
    "direct equality"
    def check_if_equal(s1: StringCompareTest):
        assert s1.s == "test"
        s1.ok = "OK"
        return "OK"
    s = StringCompareTest()
    s.s = "test"
    s.ok = "FAIL"

    assert xschedule([check_if_equal], space=[s], goal=lambda: s.ok=="OK") == "OK"
    assert s.ok == "OK"


def test_solve_deref_equality():
    "test dereferencing eq"
    def check_if_equal(s1: StringCompareTest):
        assert s1.s == s1.ok
        s1.ok = "OK"
        return "OK"
    s = StringCompareTest()
    s.s = "test"
    s.ok = "test"

    assert xschedule([check_if_equal], space=[s], goal=lambda: s.ok=="OK") == "OK"
    assert s.ok == "OK"


@pytest.mark.skip(reason="this does not work as we need a factory")
def test_solve_partial_deref1():
    "test partial deref = a"
    ss = String("test")
    def check_if_equal(s1: StringCompareTest):
        assert s1.s == ss
        s1.ok = "OK"
        return "OK"
    s = StringCompareTest()
    s.s = "test"
    s.ok = "test"

    assert xschedule([check_if_equal], space=[s], goal=lambda: s.ok=="OK") == "OK"
    assert s.ok == "OK"

def test_solve_partial_deref1():
    "test partial deref = a"
    ss = stringFactory.get("test")
    def check_if_equal(s1: StringCompareTest):
        assert s1.s == ss
        s1.ok = "OK"
        return "OK"
    s = StringCompareTest()
    s.s = "test"
    s.ok = "test"

    assert xschedule([check_if_equal], space=[s], goal=lambda: s.ok=="OK") == "OK"
    assert s.ok == "OK"

def test_solve_partial_deref_reverse():
    "test partial deref same but reverse"
    ss = stringFactory.get("test")
    def check_if_equal(s1: StringCompareTest):
        assert ss == s1.s
        s1.ok = "OK"
        return "OK"
    s = StringCompareTest()
    s.s = "test"
    s.ok = "test"

    assert xschedule([check_if_equal], space=[s], goal=lambda: s.ok=="OK") == "OK"

def test_solve_with_object():
    "test with string object in state space"
    ss2 = stringFactory.get("test")
    def check_if_equal(s1: StringCompareTest, ss: String):
        assert ss == s1.s
        s1.ok = "OK"
        return "OK"
    s = StringCompareTest()
    s.s = "test"
    s.ok = "test"

    assert xschedule([check_if_equal], space=[s, ss2], goal=lambda: s.ok=="OK") == "OK"
