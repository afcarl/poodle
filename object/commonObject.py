from poodle.poodle import *

class Number(Digit): # alias for Digit!!! TODO rename number to digit
    pass
Number.higher_than = Relation(Number)

class Number4Bit(Imaginary):
    pass
