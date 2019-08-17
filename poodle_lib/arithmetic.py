import poodle
import itertools
from .poodle_main import _system_objects

class IntegerType(poodle.Object):
    pass

class LogSparseInteger(IntegerType):
    def add(self, num: "LogSparseInteger"):
        resultVar = poodle.Any(LogSparseInteger, space=_system_objects)  # TODO: implicit search in current context?
        sumRes = poodle.Any(SumResult, space=_system_objects)
        assert sumRes.operator1 == self
        assert sumRes.operator2 == num
        assert sumRes.result == resultVar

        return resultVar

    def __add__(self, other):
        if isinstance(other, int):
            return self.add(logSparseIntegerFactory.get(other))
        elif type(other) == LogSparseInteger:
            return self.add(other)
        raise ValueError("Unsupported type for arithmetic operator")

    def __radd__(self, other):
        return self.__add__(self, other)
        
    def gen_name(self, name):
        return super().gen_name(name+"-num-"+str(self.value))

    def sub(self, other: "LogSparseInteger"):
        resultVar = poodle.Any(LogSparseInteger, space=_system_objects)
        sumRes = poodle.Any(SumResult, space=_system_objects)
        assert sumRes.operator1 == resultVar
        assert sumRes.operator2 == other
        assert sumRes.result == self

        return resultVar

    def __sub__(self, other):
        if isinstance(other, int):
            return self.sub(logSparseIntegerFactory.get(other))
        elif type(other) == LogSparseInteger:
            return self.sub(other)
        raise ValueError("Unsupported type for arithmetic operator")
        
    # TODO: __rsub__

    # def mul(self, other: LogSparseInteger, mulres: MulResult):
    #     resultVar = LogSparseInteger()
    #     assert mulres.operator1 == self
    #     assert mulres.operator2 == other
    #     assert mulres.result == resultVar

    #     return resultVar

    # def __mul__(self, other):
    #     return self.mul(other)

    # # TODO: add division

def logexp(x,a,b,c):
    return int(a*pow(b,x*c))

class LogSparseIntegerFactory:
    def __init__(self, start=0, count=21, func=logexp, args={"a":0.0717876, "b":1.25545, "c":2.6032}):
        base10 = {i:LogSparseInteger(i) for i in range(start,10)}
        base10.update({func(i, **args):LogSparseInteger(func(i, **args)) for i in range(start, count)})
        self.numbers=base10
        self.NONE = LogSparseInteger("NONE")
        self.NaN = LogSparseInteger("NaN")
        self.generate_sparse_sums()
    def get(self, x):
        if x < list(self.numbers.keys())[0]: raise ValueError(f"Value of {x} is not supported (lower than %s)" % list(self.numbers.keys())[0])
        for n, obj in reversed(list(self.numbers.items())):
            if x >= n: return obj
        raise ValueError(f"Value of {x} is not supported (bigger than %s)" % list(self.numbers.keys()[-1]))
    def get_objects(self):
        return list(self.numbers.values()) + \
                list(self.sums)
    def generate_sparse_sums(self):
        self.sums=[]
        for a, b in itertools.permutations(self.numbers.items(), 2):
            s = SumResult()
            s.operator1 = a[1]
            s.operator2 = b[1]
            sumn = a[0]+b[0]
            try:
                s.result = self.get(sumn)
                # print("MY CHECK SUM", s.operator1, "+", s.operator2, "=", s.result) # TODO: this does not work
                # print("MY CHECK SUM", a[0], "+", b[0], "=", self.get(sumn), s, "need===", sumn)
                self.sums.append(s)
            except:
                pass
        
    # TODO: spase_mults


class SumResult(poodle.Object):
    operator1: LogSparseInteger
    operator2: LogSparseInteger
    result: LogSparseInteger

class MulResult(poodle.Object):
    operator1: LogSparseInteger
    operator2: LogSparseInteger
    result: LogSparseInteger


logSparseIntegerFactory = LogSparseIntegerFactory()

_system_objects.update({ob.name:ob for ob in logSparseIntegerFactory.get_objects()})
# TODO HERE: generate all SumResult
# ... add SumResult to _system_facts

# TODO HERE: generate all MulResult 

# TODO HERE: add generated lists to planning problem to _collected_facts
#                   or use other poodle3 methods

