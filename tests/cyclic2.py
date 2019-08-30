from poodle import *
from typing import Set
import sys
sys.path.append("./tests")
import cyclic1

class CTest2(Object):
    o: Set["CTest1"]

class DCTest2(Object):
    o: Set["cyclic1.DCTest1"]