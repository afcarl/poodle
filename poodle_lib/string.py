import poodle
from .poodle_main import resolve_poodle_special_object, Property

class String(poodle.Object):
    def __str__(self):
        return str(self._get_value())
    def __repr__(self):
        return repr(str(self))
    def __hash__(self):
        return hash(self.poodle_internal__value)
    def __eq__(self, other):
        if isinstance(other, Property):
            other._property_of_inst == self
        other = resolve_poodle_special_object(other)
        if self._variable_mode or other._variable_mode: 
            assert self == other
            return True
        if isinstance(other, String):
            return self._get_value() == other._get_value()


