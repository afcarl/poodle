import poodle
import itertools
from .poodle_main import _system_objects, resolve_poodle_special_object

class IntegerType(poodle.Object):
    pass

class LogSparseInteger(IntegerType):
    def add(self, num: "LogSparseInteger"):
        num = resolve_poodle_special_object(num)
        resultVar = poodle.Any(LogSparseInteger, space=_system_objects)  # TODO: implicit search in current context?
        sumRes = poodle.Any(SumResult, space=_system_objects)
        assert sumRes.operator1 == self
        assert sumRes.operator2 == num
        assert sumRes.result == resultVar
        if not self._variable_mode: resultVar.poodle_internal__value = self.poodle_internal__value + num.poodle_internal__value

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
        return super().gen_name(name+"-num-"+str(self.poodle_internal__value))

    # TODO: for every method here, support 'other' to be a 'int' value
    def sub(self, other: "LogSparseInteger"):
        other = resolve_poodle_special_object(other)
        resultVar = poodle.Any(LogSparseInteger, space=_system_objects)
        sumRes = poodle.Any(SumResult, space=_system_objects)
        assert sumRes.operator1 == resultVar
        assert sumRes.operator2 == other
        assert sumRes.result == self
        if not self._variable_mode: resultVar.poodle_internal__value = self.poodle_internal__value - other.poodle_internal__value

        return resultVar

    def __sub__(self, other):
        other = resolve_poodle_special_object(other)
        if isinstance(other, int):
            return self.sub(logSparseIntegerFactory.get(other))
        elif type(other) == LogSparseInteger:
            return self.sub(other)
        raise ValueError("Unsupported type for arithmetic operator")
    
    def __gt__(self, other):
        other = resolve_poodle_special_object(other)
        gt = poodle.Any(GreaterThan, space=_system_objects)
        assert gt.val1 == self and gt.val2 == other
        if self._variable_mode: return True
        else: return self.poodle_internal__value > other.poodle_internal__value

    def __lt__(self, other):
        other = resolve_poodle_special_object(other)
        gt = poodle.Any(GreaterThan, space=_system_objects)
        assert gt.val2 == self and gt.val1 == other
        if self._variable_mode: return True
        else: return self.poodle_internal__value < other.poodle_internal__value

    def __ge__(self, other):
        other = resolve_poodle_special_object(other)
        ge = poodle.Any(GreaterEqual, space=_system_objects)
        assert ge.val1 == self and ge.val2 == other
        if self._variable_mode: return True
        else: return self.poodle_internal__value >= other.poodle_internal__value
    
    def __le__(self, other):
        other = resolve_poodle_special_object(other)
        ge = poodle.Any(GreaterEqual, space=_system_objects)
        assert ge.val2 == self and ge.val1 == other
        if self._variable_mode: return True
        else: return self.poodle_internal__value <= other.poodle_internal__value



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
    def __init__(self, start=0, lincount=10, logcount=15, func=logexp, args={"a":0.0717876, "b":1.25545, "c":2.6032}):
        base10 = {i:LogSparseInteger(i) for i in range(-1,lincount)}
        base10.update({func(i, **args):LogSparseInteger(func(i, **args)) \
            for i in range(0, logcount)})
        self.numbers=base10
        self.NONE = LogSparseInteger("NONE")
        self.NaN = LogSparseInteger("NaN")
        self.generate_sparse_sums()
        self.generate_gt_ge()
    def get(self, x):
        if x < list(self.numbers.keys())[0]: raise ValueError(f"Value of {x} is not supported (lower than %s)" % list(self.numbers.keys())[0])
        for n, obj in reversed(list(self.numbers.items())):
            if x >= n: return obj
        raise ValueError(f"Value of {x} is not supported (bigger than %s)" % list(self.numbers.keys()[-1]))
    def get_objects(self):
        return list(self.numbers.values()) + \
                list(self.sums) + self.gts + self.ges
    def generate_sparse_sums(self):
        self.sums=[]
        for a, b in itertools.product(self.numbers.items(), repeat=2):
            s = SumResult("%s+%s"%(a[0],b[0]))
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
    
    def generate_gt_ge(self):
        self.gts = []
        self.ges = []
        for a, b in itertools.product(self.numbers.items(), repeat=2):
            if a[0] > b[0]:
                gt = GreaterThan("%s>%s"%(a[0],b[0]))
                gt.val1 = a[1]
                gt.val2 = b[1]
                self.gts.append(gt)
            if a[0] >= b[0]:
                ge = GreaterEqual("%s>=%s"%(a[0],b[0]))
                ge.val1 = a[1]
                ge.val2 = b[1]
                self.ges.append(ge)

        
    # TODO: spase_mults


class SumResult(poodle.Object):
    operator1: LogSparseInteger
    operator2: LogSparseInteger
    result: LogSparseInteger

class GreaterThan(poodle.Object):
    val1: LogSparseInteger
    val2: LogSparseInteger

class GreaterEqual(poodle.Object):
    val1: LogSparseInteger
    val2: LogSparseInteger
class MulResult(poodle.Object):
    operator1: LogSparseInteger
    operator2: LogSparseInteger
    result: LogSparseInteger


logSparseIntegerFactory = LogSparseIntegerFactory(lincount=17, logcount=15)

_system_objects.update({ob.poodle_internal__sym_name:ob for ob in logSparseIntegerFactory.get_objects()})
# TODO HERE: generate all SumResult
# ... add SumResult to _system_facts

# TODO HERE: generate all MulResult 

# TODO HERE: add generated lists to planning problem to _collected_facts
#                   or use other poodle3 methods

