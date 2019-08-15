import poodle

psystem = [] # Stub.

class IntegerType(poodle.Object):
    pass

class LogSparseInteger(IntegerType):
    def add(self, num: "LogSparseInteger"):
        resultVar = Any(LogSparseInteger, space=psystem)  # TODO: implicit search in current context?
        sumRes = Any(SumResult, space=psystem)
        assert sumRes.operator1 == self
        assert sumRes.operator2 == num
        assert sumRes.result == resultVar

        return resultVar

    def __add__(self, other):
        if isinstance(other, int):
            return self.add(logSparseIntegerFactory.getLogSparseInteger(other))
        elif type(other) == LogSparseInteger:
            return self.add(other)
        raise ValueError("Unsupported type for arithmetic operator")

    def __radd__(self, other):
        return self.__add__(self, other)

    def sub(self, other: "LogSparseInteger"):
        resultVar = Any(LogSparseInteger, space=psystem)
        sumRes = Any(SumResult, space=psystem)
        assert sumRes.operator1 == resultVar
        assert sumRes.operator2 == other
        assert sumRes.result == self

        return resultVar

    def __sub__(self, other):
        if isinstance(other, int):
            return self.sub(logSparseIntegerFactory.getLogSparseInteger(other))
        elif type(other) == LogSparseInteger:
            return self.sub(other)
        raise ValueError("Unsupported type for arithmetic operator")

    # def mul(self, other: LogSparseInteger, mulres: MulResult):
    #     resultVar = LogSparseInteger()
    #     assert mulres.operator1 == self
    #     assert mulres.operator2 == other
    #     assert mulres.result == resultVar

    #     return resultVar

    # def __mul__(self, other):
    #     return self.mul(other)

    # # TODO: add division


class LogSparseIntegerFactory():
    pass  # TODO
    # generate all LogSparseIntegers and generate all results/mults etc. (when space accessed)
    # implement logarithmic generation based on settings


class SumResult(poodle.Object):
    operator1: LogSparseInteger
    operator2: LogSparseInteger
    result: LogSparseInteger


class MulResult(poodle.Object):
    operator1: LogSparseInteger
    operator2: LogSparseInteger
    result: LogSparseInteger
