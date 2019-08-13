from poodle import Object, SystemAny

psystem = [] # Stub.


class Number(Object):
    def add(self, num: Number):
        resultVar = Any(Number, space=psystem)  # TODO: implicit search in current context?
        sumRes = Any(SumResult, space=psystem)
        assert sumRes.operator1 == self
        assert sumRes.operator2 == num
        assert sumRes.result == resultVar

        return resultVar

    def __add__(self, other):
        if isinstance(other, int):
            return self.add(numberFactory.getNumber(other))
        elif type(other) == Number:
            return self.add(other)
        raise ValueError("Unsupported type for arithmetic operator")

    def __radd__(self, other):
        return self.__add__(self, other)

    def sub(self, other: Number):
        resultVar = Any(Number, space=psystem)
        sumRes = Any(SumResult, space=psystem)
        assert sumRes.operator1 == resultVar
        assert sumRes.operator2 == other
        assert sumRes.result == self

        return resultVar

    def __sub__(self, other):
        if type(other) == type(0):
            return self.sub(numberFactory.getNumber(other))
        elif type(other) == Number:
            return self.sub(other)
        raise ValueError("Unsupported type for arithmetic operator")

    # def mul(self, other: Number, mulres: MulResult):
    #     resultVar = Number()
    #     assert mulres.operator1 == self
    #     assert mulres.operator2 == other
    #     assert mulres.result == resultVar

    #     return resultVar

    # def __mul__(self, other):
    #     return self.mul(other)

    # # TODO: add division


class NumberFactory():
    pass  # TODO
    # generate all numbers and generate all results/mults etc. (when space accessed)
    # implement logarithmic generation based on settings


class SumResult(Object):
    operator1: Number
    operator2: Number
    result: Number


class MulResult(Object):
    operator1: Number
    operator2: Number
    result: Number
