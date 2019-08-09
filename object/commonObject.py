from poodle import *

class Number(Digit): # alias for Digit!!! TODO rename number to digit
    higher_than = Relation("Number")
    lower_than = Relation("Number")
    pass
Number.higher_than = Relation(Number)
Number.lower_than = Relation(Number)

class Number4Bit(Imaginary):
    pass

         
class AddedNumber(Object):
    cost = 1
    operator1 = Property(Number)
    operator2 = Property(Number)
    result = Property(Number)

class GreaterThan(Object):

    lower = Property(Number)
    higher = Property(Number)

