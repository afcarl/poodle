from poodle import *
from typing import Set
import sys
sys.path.append("./tests")
import cyclic2

class CTest1(Object):
    o: Set["cyclic2.CTest2"]

class DCTest1(Object):
    o: Set["cyclic2.DCTest2"]