import poodle
from .poodle_main import resolve_poodle_special_object, Property, new_internal

class String(poodle.Object):
    def __str__(self):
        return str(self._get_value())
    def __repr__(self):
        return repr(str(self))
    def __hash__(self):
        return hash(self.poodle_internal__value)
    def __eq__(self, other):
        other = resolve_poodle_special_object(other)
        # if isinstance(other, str): other = stringFactory.get(other)
        # if isinstance(other, Property):
        #     return other._property_value == self
        if isinstance(other, poodle.Object) and isinstance(self.poodle_internal__value, str) \
                        and isinstance(other.poodle_internal__value, str) \
                        and not self._variable_mode \
                        and not other._variable_mode:
            return self.poodle_internal__value == other.poodle_internal__value
        return super().__eq__(other)

class _StringFactory:
    def __init__(self):
        self.reset()
    def get(self, value):
        if not value in self.values:
            self.values[value] = new_internal(String, value) # needed to indicate internal call
        return self.values[value]
    def get_objects(self):
        return list(self.values.values())
    def reset(self):
        self.values = {}

stringFactory = _StringFactory()
