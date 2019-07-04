from poodle.poodle import *

class Number(Digit): # alias for Digit!!! TODO rename number to digit
    pass
Number.higher_than = Relation(Number)

class Number4Bit(Imaginary):
    # ... ...
    identified_by = Property(sig2=Digit, sig1=Digit, sig0=Digit)
