from poodle import *

class SumResult(Object):
    operator1: Number
    operator2: Number
    result: Number

class MulResult(Object):
    operator1: Number
    operator2: Number
    result: Number

class Number(Object):
    def add(self, num: Number, sumResult: SumResult):
        resultVar = Number()
        assert sumResult.operator1 == self
        assert sumResult.operator2 == num
        assert sumResult.result == resultVar

        return resultVar

    def __add__(self, other):
        return self.add(other)
    def sub(self, other: Number, sumRes: SumResult):
        # c = a - b
        resultVar = Number()
        assert sumRes.operator1 == resultVar
        assert sumRes.operator2 == other
        assert sumRes.result == self

        return resultVar

    def __sub__(self, other):
        return self.sub(other)

    def mul(self, other: Number, mulres: MulResult):
        resultVar = Number()
        assert mulres.operator1 == self 
        assert mulres.operator2 == other
        assert mulres.result == resultVar 

        return resultVar

    def __mul__(self, other):
        return self.mul(other)



class NumberFactory():
    pass # TODO
    # generate all numbers and generate all results/mults etc. (when space accessed)
    # implement logarithmic generation based on settings