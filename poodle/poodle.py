# the lang has enough info to say that:
#   (has-table ?host ?table)
#   (has-route ?table ?route) ;; equals exists
# ... is equal to (has-table-route ?host ?table ?route)

# expressing imaginary objects is the key..
# PLAN: 1. do imaginary route object
# 2. do imaginary number object

# TODO: required properties
# TODO: difference property vs. relation? one-to-many?
# TODO: if property is not protected; or it is a stateRelation: 
#       explicitly define the state changes that it can take!

# TODO: required properties
# TODO: if/else concept!

import string
import random
import inspect
import copy, subprocess
from collections import OrderedDict
import os
import datetime

# import wrapt
# import infix

_compilation = False
_problem_compilation = False
_collected_predicates = []
_collected_effects = []
_collected_parameters = {}
_selector_out = None
_collected_predicate_templates = [] # TODO: localize state! also not all predicates may be used in problem actions
_collected_object_classes = set()
_collected_objects = {} # format: { "class": [ ... objects ... ] }
_collected_facts = []

from functools import partial

# class Prox(wrapt.ObjectProxy):
#     isproxy = True

class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)
        
@Infix
def IN(what, where):
    # frame = inspect.currentframe()
    # frame = inspect.getouterframes(frame)[2]
    # c_string = inspect.getframeinfo(frame[0]).code_context[0].strip()
    # print("FRAME", c_string)
    ret = where.contains(what)
    global _selector_out
    _selector_out = None
    return ret
    
@Infix
def EQ(what1, what2):
    ret = what1.equals(what2)
    global _selector_out
    _selector_out = None
    return ret

def Select(what):
    "Selector decorator"
    # WARNING! This is very thread unsafe!!!
    global _selector_out
    ret = _selector_out
    _selector_out = None
    return ret

# https://stackoverflow.com/a/2257449
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

id_counter = 0
def new_id():
    global id_counter
    id_counter += 1
    return id_counter

def gen_var(name):
    return "?%s-%s" % (name, new_id())
    
def get_property_class_name(prop):
    # PART 2.
    # We can have either of the following:
    #    _property_of, no _property_of_inst - means that we are direct clas-property of some class Object
    # no _property_of,    _property_of_inst - we are property of instantiated object
    #    _property_of and _property_of_inst - means we were returned by another call to operator
    #                                         operator instantiates returning object to allow attributes modification
    has_po = False
    has_poi = False
    if hasattr(prop, "_property_of_inst"): 
        has_poi = prop._property_of_inst
    if hasattr(prop, "_property_of"):
        has_po = prop._property_of
    #print("get_property_class: _property_of:", has_po, "_property_of_inst:", has_poi)
    
    if has_po and not has_poi:
        my_class = prop._property_of.__name__
    elif not has_po and has_poi:
        my_class = type(prop._property_of_inst).__name__
    elif has_po and has_poi:
        my_class = prop._property_of.__name__
    else:
        raise ValueError("Can not detect who I am")
    return my_class

def gen_text_predicate_push_globals(class_name, property_name, var1, var1_class, var2, var2_class):
    # return gen_text_predicate_globals(class_name+"-"+property_name, var1, var1_class, var2, var2_class)
# def gen_text_predicate_globals(predicate_name, var1, var1_class, var2, var2_class):
    global _collected_predicate_templates
    global _collected_object_classes
    predicate_name = class_name+"-"+property_name
    # text_predicate = "(" + predicate_name + " " + var1 + " - " + var1_class + " " + var2 + " - " + var2_class + ")" # preconditions with classes not supported
    text_predicate = "(" + predicate_name + " " + var1 + " " + var2 + ")"
    _collected_predicate_templates.append("(" + predicate_name + " ?var1 - " + var1_class + " ?var2 - " + var2_class + ")")
    _collected_object_classes.update([class_name, var1_class, var2_class])
    return text_predicate

def gen_one_predicate(predicate_name, var, var_class_name):
    global _collected_predicate_templates
    global _collected_object_classes
    text_predicate = "("+predicate_name+" "+var+")"
    _collected_predicate_templates.append("(" + predicate_name + " ?var1 - "+var_class_name+")")
    #_collected_object_classes.update([class_name, var1_class, var2_class])
    return text_predicate
    

class Property(object):
    def __init__(self, *initial_data, **kwargs):
        # WARNGING
        # in some cases, property is not being requested from a class (???)
        # (probably when we're instantiating and it is requested from an instance)
        # in this case we have no idea about our name 
        #    THIS has since been fixed by __set_name__ hack. Think what to do.
        self._property_of = None # for reference only
        self._order = []
        self._unset = False
        if len(initial_data) == 1 and issubclass(initial_data[0], Object):
            self._singleton = True
            self._value = initial_data[0]
            return
        else:
            self._singleton = False
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
            self._order.append(key)
        for key in kwargs:
            setattr(self, key, kwargs[key])
            
    def __set_name__(self, owner, name):
        if not hasattr(self, "_property_name"):
            self._property_name = name
            
    def get_property_class_name(prop):
        # PART 2.
        # We can have either of the following:
        #    _property_of, no _property_of_inst - means that we are direct clas-property of some class Object
        # no _property_of,    _property_of_inst - we are property of instantiated object
        #    _property_of and _property_of_inst - means we were returned by another call to operator
        #                                         operator instantiates returning object to allow attributes modification
        has_po = False
        has_poi = False
        if hasattr(prop, "_property_of_inst"): 
            has_poi = prop._property_of_inst
        if hasattr(prop, "_property_of"):
            has_po = prop._property_of
        #print("get_property_class: _property_of:", has_po, "_property_of_inst:", has_poi) # nosiy!
        
        if has_po and not has_poi:
            my_class = prop._property_of.__name__
        elif not has_po and has_poi:
            my_class = type(prop._property_of_inst).__name__
        elif has_po and has_poi:
            my_class = prop._property_of.__name__
        else:
            raise ValueError("Can not detect who I am")
        return my_class

    def gen_predicate_name(self):
        return self.get_property_class_name()+"-"+self._property_name
        
    def find_parameter_variable(self):
        "finds the variable that holds the class"
        my_class = self._value.__name__ # _value is always a class
        myclass_genvar = None
        for ph in reversed(self._property_of_inst.parse_history):
            if my_class in ph["variables"]:
                myclass_genvar = ph["variables"][my_class]
                break
        return myclass_genvar
    
    
    def find_class_variable(self):
        "finds the variable that holds the class"
        my_class = self.get_property_class_name()
        myclass_genvar = None
        for ph in reversed(self._property_of_inst.parse_history):
            if my_class in ph["variables"]:
                myclass_genvar = ph["variables"][my_class]
                break
        return myclass_genvar
    
    def operator(self, other, operator="equals"):
        assert operator == "equals" or operator == "contains"
        global _compilation
        global _collected_predicates
        global _collected_parameters
        global _collected_predicate_templates
        global _collected_object_classes
        # TODO: multi-positional checks
        
        # PART 1.
        # If type of the thing we are comparing ourself to (we are Property!!)
        #    is also Property (we also need to check if it is not a class (type obj)
        #          (note that Properties always go as instances!)
        # then subject to compare with is other._value (but still we generate other's name predicate)
        # otherwise, we are comparing ourself with an Object directly ...
        # ... (as in Interface in Host.has_interface or interface1 in Host.has_interface)
        # [ ] Predicate to be constructed: subj.__name__ + 
        if type(other) != type and isinstance(other, Property):
            assert other._value == self._value, "Property-Property check type mismatch: %s != %s" % (other._value, self._value)
            if operator == "contains":
                assert not isinstance(other, Relation), "Can not check Relation in Relation"
            subjObjectClass = other._value
            property_property_comparison = True
        else: # TODO: elif and else with ValueError
            assert other == self._value or type(other) == self._value, "Object-Property Type mismatch: %s != %s" % (other, self._value) # if we're working with pure classes of objects
            subjObjectClass = other # this object may not have any _property_of
            property_property_comparison = False
        
        print("OPERATOR-1:", self._property_name, operator, subjObjectClass, self._property_of, type(self._property_of))
        
        # PART 2.
        # We can have either of the following:
        #    _property_of, no _property_of_inst - means that we are direct clas-property of some class Object
        # no _property_of,    _property_of_inst - we are property of instantiated object
        #    _property_of and _property_of_inst - means we were returned by another call to operator
        #                                         operator instantiates returning object to allow attributes modification
        has_po = False
        has_poi = False
        if hasattr(self, "_property_of_inst"): 
            has_poi = self._property_of_inst
        if hasattr(self, "_property_of"):
            has_po = self._property_of
        # print("OPERATOR: _property_of:", has_po, "_property_of_inst:", has_poi) # nosiy!
        
        # if has_po and not has_poi:
        #     my_class = self._property_of.__name__
        # elif not has_po and has_poi:
        #     my_class = type(self._property_of_inst).__name__
        # elif has_po and has_poi:
        #     my_class = self._property_of.__name__
        # else:
        #     raise ValueError("Can not detect who I am")
        my_class = self.get_property_class_name()
        
        # PART 3.
        # We need to understand what are we going to return:
        #   an instance of Object that is selected from property of obj Class, 
        #   like: 
        #   Object in instance.my_prop,
        #   instance in Object.my_prop
        #   Object.my_prop in instance.my_prop
        #   finally instance1.my_prop in instance2.my_prop - in this case return True ...
        #           ... and store the constructed return in global Selector state (TODO XXX)
        
        # If we are property of an Object and this Object is not an instance
        #     then someone requested us to return our parent Object type when matched
        if type(self._property_of) is BaseObjectMeta and not hasattr(self, "_property_of_inst"):
            print("OPERATOR: Decided to return SELF.property_of()")
            obj=self._property_of() # contains who am I the property of.. (meta)
            who_instantiating = "self"
        # Else, if the thing we are comparing ourself to (subj) is class and not instance
        #    vvv---always-true--------------vvv         vvv----check-if-subj-is-instance--vvv
        elif type(subjObjectClass) is BaseObjectMeta and not isinstance(subjObjectClass, Object) and not hasattr(other, "_property_of_inst"):
            print("OPERATOR: Decided to return subj() objecs")
            obj = subjObjectClass()
            who_instantiating = "other"
        else:
            if _compilation: # actually means "running selector" and would be better renamed as `_selector_mode`
                # PART 3.1.
                # in compilation mode, we can return anything we want as result is not being used in later computations
                print("OPERATOR IN COMPILATION/SELECTOR MODE")
                obj = self._value()
                who_instantiating = None
            else:
                raise ValueError("No class to select is present in selector expression. Both LHS and RHS are instances.")
            
        if isinstance(subjObjectClass, Object):
            other_class = type(subjObjectClass).__name__
        else:
            other_class = subjObjectClass.__name__
        
        # Part 5. Get history of generated variables
        # Variants:
        # 1. we are property of instance, thus self._property_of_inst.parse_history
        # 2. the other is instance, thus other.parse_history
        # 3. the other is property of instance, thus other._property_of_inst.parse_history
        #    TODO XXX NOTE: need to look for toplevel object always, as we may be property-of-property
        parse_history = []
        if has_poi and hasattr(self._property_of_inst, "parse_history"):
            #print("OPERATOR HIST:", "1. we are property of instance")
            if not _compilation: assert parse_history == []
            parse_history += self._property_of_inst.parse_history
        if isinstance(other, Object) and hasattr(other, "parse_history"):
            #print("OPERATOR HIST:", "2. the other is instance")
            if not _compilation: assert parse_history == []
            parse_history += other.parse_history
        if isinstance(other, Property) and hasattr(other, "_property_of_inst") and hasattr(other._property_of_inst, "parse_history"):
            #print("OPERATOR HIST:", "3. the other is property of instance")
            if not _compilation: assert parse_history == []
            parse_history += other._property_of_inst.parse_history
        #print("OPERATOR-HIST-1", parse_history)
        other_genvar = None
        myclass_genvar = None
        
        # no need to generate other_genvar if other is an instance and already has a variable
        if who_instantiating != "other": # means that other is already an instance, both in regular and compilatioin mode
            # it is either an instance itself or is a property of instance
            if hasattr(other, "_property_of_inst") and other_class == other._property_of_inst.__class__.__name__: # weird check to figure out if this is applicable scenario...
                if other._property_of_inst._class_variable:
                    print("OPERATOR: Found other porperty variable", other._property_of_inst._class_variable, other_class, other._property_of_inst)
                    other_genvar = other._property_of_inst._class_variable
            elif not hasattr(other, "_property_of_inst"):
                if other._class_variable:
                    print("OPERATOR: Found other instance variable", other._class_variable, other_class)
                    other_genvar = other._class_variable
            else:
                print("OPERATOR Skipping getting variable from instances")
                pass
                
        # WARNING@!!!! finding variables in history is obsolete and UNSAFE!!!
        if parse_history:
            if not other_genvar:
                for ph in reversed(parse_history):
                    if other_class in ph["variables"] and who_instantiating != "other": # only generate new var if we are instantiating it here
                        other_genvar = ph["variables"][other_class]
                        print("WARNING! Variable found in history - resulted PDDL may be wrong")
                        break
            for ph in reversed(parse_history):
                if has_poi and self._property_of_inst._class_variable:
                    myclass_genvar = self._property_of_inst._class_variable
                else:
                    if my_class in ph["variables"] and who_instantiating != "self":
                        myclass_genvar = ph["variables"][my_class]
                        break
                    
        if myclass_genvar is None: myclass_genvar = gen_var(my_class)
        if other_genvar is None: 
            other_genvar = gen_var(other_class)
            print("OPERATOR: generating new var for other!", other_genvar)
        
        collected_parameters = {other_genvar: other_class, myclass_genvar: my_class}
        
        if property_property_comparison:
            other_property_class = get_property_class_name(other)
            other_property_genvar = None
            if parse_history:
                for ph in reversed(parse_history):
                    if other_property_class in ph["variables"] and who_instantiating != "other": # only generate new var if we are instantiating it here
                        other_property_genvar = ph["variables"][other_property_class]
                        break
            if other_property_genvar is None: other_property_genvar = gen_var(other_property_class)
            collected_parameters[other_property_genvar] = other_property_class
            text_predicate = gen_text_predicate_push_globals(my_class, self._property_name, myclass_genvar, my_class, other_genvar, other_class)
            text_predicate_2 = gen_text_predicate_push_globals(other_property_class, other._property_name, other_property_genvar, other_property_class, other_genvar, other_class)
            print("OPERATOR-PRECOND-PDDL1: ", text_predicate)
            print("OPERATOR-PRECOND-PDDL2: ", text_predicate_2)
        else:
            text_predicate = gen_text_predicate_push_globals(my_class, self._property_name, myclass_genvar, my_class, other_genvar, other_class)
            text_predicate_2 = None
            print("OPERATOR-PRECOND-PDDL:  ", text_predicate)
        
        # print("OPERATOR-PARAM-PDDL:", collected_parameters)
        
        if not hasattr(obj, "parse_history"):
            obj.parse_history = parse_history
        
        # TODO: what if we have two same classes?
        
        # TODO: a new method for variable storage!
        #       store the variable in object returned - and use it first whenever needed

        # store variable that we created for the returning object
        if who_instantiating == "self": # returning object is our class, and we just invented a new variable name for us
            print("OPERATOR setting class variable myclass genvar to ", myclass_genvar, my_class)
            obj._class_variable = myclass_genvar
        if who_instantiating == "other": # returning object is who we are being compared to, and we invented variable for that
            print("OPERATOR setting class variable ohter genvar to ", other_genvar, other_class)
            obj._class_variable = other_genvar
            
        # also store variable for the instantiated object that we are comparing with, if not created before
        if has_poi: # is exactly equivalent to who_instantiating == other, means that we(who we property of) are not a class
            if not self._property_of_inst._class_variable is None:
                print("WARNING! _class_variable is ", self._property_of_inst._class_variable, "but we are generating", myclass_genvar)
                pass
            else:
                self._property_of_inst._class_variable = myclass_genvar
        
        # in compilation mode, we need to set other variable's class variable with ours
        # if _compilation:
        if who_instantiating is None:
            if isinstance(other, Object):
                if other._class_variable is None:
                    other._class_variable = other_genvar
                else:
                    print("WARNING! Not setting other variable to %s as it already has %s" % (other_genvar, other._class_variable))

        
        obj.parse_history.append({
            "operator": operator, 
            "self": self, 
            "other": subjObjectClass, 
            "self-prop": self._value, 
            #"variables": { other_class: other_genvar , my_class: myclass_genvar }, # TODO: what if we have two same classes?
            "variables": {my_class: myclass_genvar, other_class: other_genvar }, # TODO: what if we have two same classes?
            "class_variables": { my_class: myclass_genvar },
            "text_predicates": [text_predicate, text_predicate_2],
            "parameters": collected_parameters
        })
        #print("OPERATOR-HIST-2", parse_history)

        # this is required for the variables to become available at selector compilation
        # if has_poi and _compilation and not hasattr(self._property_of_inst, "parse_history"): self._property_of_inst.parse_history = parse_history
        if has_poi and not hasattr(self._property_of_inst, "parse_history"): self._property_of_inst.parse_history = parse_history
        if has_poi and hasattr(self._property_of_inst, "parse_history"): self._property_of_inst.parse_history += parse_history
        
        if _compilation:
            # because in compilation mode our parse_history now contains merged history ->>>
            for ph in obj.parse_history + parse_history: # WARNING! why do we need to add ph here??
                _collected_predicates += ph["text_predicates"]
                _collected_parameters.update(ph["parameters"])
        return obj
        
    def equals(self, other):
        return self.operator(other, "equals")

    def __eq__(self, other):
        global _selector_out
        if hasattr(self, "_property_of_inst") and isinstance(other, Property) and not hasattr(other, "_property_of_inst"):
            print("!!!!!! ALT BEH 1 - me is ", self, self._property_of_inst, "other is", other)
            _selector_out = other.equals(self)
        else:
            _selector_out = self.equals(other)
        return True
    
    # TODO: write a setter operator to call this 
    
    def _prepare(self, valueObjectObject=None):
        global _compilation
        if not _compilation:
            raise BaseException("Parameter mutation outside of compilation")
        # TODO: also detect that we are outside of effect block!
        global _collected_predicates
        global _collected_parameters
        for ph in self._property_of_inst.parse_history:
            _collected_predicates += ph["text_predicates"]
            _collected_parameters.update(ph["parameters"])
        if valueObjectObject:
            for ph in valueObjectObject.parse_history:
                _collected_predicates += ph["text_predicates"]
                _collected_parameters.update(ph["parameters"])
        
    def set(self, value):
        global _problem_compilation
        assert type(value) == self._value, "Type mismatch: setting %s to %s.%s expecting %s" % (value, self._property_of_inst.__class__.__name__, self._property_name, self._value)
        self._actual_value = value
        if _problem_compilation:
            global _collected_facts
            _collected_facts.append("("+self.gen_predicate_name()+" "+self._property_of_inst.name + " " + value.name+ ")")
            return
        self._prepare(value)
        global _collected_effects
        _collected_effects.append("("+self.gen_predicate_name()+" "+self.find_class_variable()+" "+value.class_variable()+")")
        
    def unset(self, what = None):
        # we need to unset the value that we selected for us
        self._prepare()
        global _collected_effects
        if what is None: 
            print("WARNING! Using experimental support for what=None")
            _collected_effects.append("(not ("+self.gen_predicate_name()+" "+self.find_class_variable()+" "+self.find_parameter_variable()+"))")
        else:
            _collected_effects.append("(not ("+self.gen_predicate_name()+" "+self.find_class_variable()+" "+what._class_variable+"))")
        self._unset = True
   
    def __getattr__(self, attr):
        "get my value"
        # print("Property Getattr: request for", self, '.', attr, 'dict:', self.__dict__)
        # the following is official way of checking if we have an attribute 
        # https://docs.python.org/3.6/library/functions.html#hasattr
        me_has_attr = False
        try:
            super().__getattribute__(attr)
            me_has_attr = True
        except AttributeError:
            pass
        me_has_value = False
        try:
            super().__getattribute__("_value")
            me_has_value = True
        except AttributeError:
            pass
        # The above renders this obolete: (check!)
        if attr in [ "_property_of_inst", "_value", "_property_name", "myname" ]: # please delete 'myname'
            # return super().__getattr__(self, attr)
            return super().__getattribute__(attr)
        if hasattr(self, "_property_of_inst") and not me_has_attr:
            if me_has_value:
                if hasattr(self._value, attr):
                    ob = copy.copy(getattr(self._value, attr))
                    ob._orig_object = getattr(self._value, attr)
                    ob._property_of_inst = self._value # WARNING! property_of_inst is a PROPERTY!! i.e. TYPE of PROP
                    ob._type_of_property = self
                    print("%s is returning copy of val %s %s which is %s" % (self, attr, ob, self._value))
                    return ob
                else:
                    raise AttributeError("Property type `%s` does not have `%s`" % (self._value, attr)) 
            #print("returning val %s %s" % (attr, self._value)) # This is wrong
            raise NotImplementedError("`%s` is not implemented in %s and no _value is assigned to %s" % (attr, self.__class__.__name__, self)) # you can add a stopword if you need this property upstream
        else:
            raise AttributeError('%s object has no attribute %s' % (self._value, attr))
        
        
    
class Relation(Property):
    "a property that can have multiple values"
    # https://stackoverflow.com/a/932580
    def contains(self, other):
        return self.operator(other, "contains")
        
    def __floordiv__(self, other):
        return self.contains(other)
        
    def set(self, what):
        raise NotImplementedError("Usage error: Relation can not be set to one value. Use .add() instead")
        
    def unset(self, what=None):
        raise NotImplementedError("Usage error: Relation can not be unset. Use .remove() instead")
    
    def add(self, what):
        super().set(what)
        
    def remove(self, what):
        super().unset(what)

    def __contains__(self, what):
        global _selector_out
        _selector_out = self.contains(what)
        return True

# class BidirectionalRelation(Relation):
#     pass

class StateRelation(Relation):
    "a state relation is a relation that is fast-changing, a state"
    # nothing special for now...
    pass

class StateProperty(Property):
    "a state relation is a relation that is fast-changing, a state"
    # nothing special for now...
    pass

class StateFact(Property):
    "state fact can only be set or unset and contains no relaitons"

    # TODO: remove this method as we have same one in base Property class!!
    def _prepare(self):
        global _compilation
        if not _compilation:
            raise BaseException("Parameter mutation outside of compilation")
        # TODO: also detect that we are outside of effect block!
        global _collected_predicates
        global _collected_parameters
        for ph in self._property_of_inst.parse_history:
            _collected_predicates += ph["text_predicates"]
            _collected_parameters.update(ph["parameters"])
        
    def set(self):
        global _collected_effects
        global _collected_facts
        global _problem_compilation
        # print("EFFECT-PDDL: TODO", self._property_of_inst.__class__.__name__)
        # print("EFFECT-PDDL: TODO", self._property_of_inst.parse_history)
        # now find in our instance's parse_history our instance's class name variable
        
        if _problem_compilation:
            text_predicate = gen_one_predicate(self.gen_predicate_name(), self._property_of_inst.name, self._property_of_inst.__class__.__name__)
            _collected_facts.append(text_predicate)
        else:
            self._prepare()
            text_predicate = gen_one_predicate(self.gen_predicate_name(), self.find_class_variable(), self._property_of_inst.__class__.__name__)
            _collected_effects.append(text_predicate)
    def unset(self):
        self._prepare()
        global _collected_effects
        # TODO: do we need to generate this??
        _collected_effects.append("(not ("+self.gen_predicate_name()+" "+self.find_class_variable()+"))")

    def __eq__(self, other):
        "StateFact can only be compared to True or False"
        assert other == True or other == False, "Only True or False for StateFact"
        global _collected_effects
        if other == False:
            # TODO: could call self.unset() if run in effect compilation, not problem compilation!!
            # (add below...)
            raise NotImplementedError("Comparing StateFact to False is not supported")
        global _problem_compilation
        if _problem_compilation:
            _collected_effects.append("("+self.gen_predicate_name()+" "+self._property_of_inst.name+")")
        else:
            self._prepare() # not sure if this is needed here???
            text_predicate = "("+self.gen_predicate_name()+" "+self.find_class_variable()+")"
            _collected_effects.append(text_predicate)
        return True
        #raise NotImplementedError("Equality of StateFact called outside of supported context")


class ActionMeta(type):
    def __new__(mcls, name, bases, attrs):
        # attempt to make in-action counter
        # complicated by having compilation after class gen
        # meaning that compilation must cause counter to restart
        #global id_counter
        #id_counter = 0
        cls = super(ActionMeta, mcls).__new__(mcls, name, bases, attrs)
        #for attr, obj in attrs.items():
        #    if isinstance(obj, Property):
        #        obj.__set_name__(cls, attr)
        return cls

class BaseObjectMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = super(BaseObjectMeta, mcls).__new__(mcls, name, bases, attrs)
        for attr, obj in attrs.items():
            if isinstance(obj, Property):
                obj.__set_name__(cls, attr)
        return cls
    def __getattribute__(self, what):
        #print("WHAT IS", what)
        if what == "_type_of_property":
            return super().__getattribute__(what)
        # if not hasattr(super(), what):
        #     if hasattr(self, "_type_of_property"):
        #         print("TOP!!")
        #         if hasattr(self._type_of_property, what):
        #             print("TOPHH!!")
        #             return getattr(self._type_of_property, what)
        #     print("No such attribute", what)
            # return super().__getattribute__(what)
        if hasattr(self, "_type_of_property"):
            print("GOP returning", what, self._type_of_property)
            #return self._type_of_property
            # print(self._type_of_property.set, self._type_of_property.__dict__)
            
        #if not what in ["__dict__", "__name__"]:
        #    print("BaseObjectMeta Getattr: self=", self, "getting what=", what, super().__getattribute__(what), type(super().__getattribute__(what)))
        
        # We are an Object,
        # now check if what is being requested is a Property:
        if issubclass(type(super().__getattribute__(what)), Property):
            # set an attribute for the returning Property object to indicate a property of where it is
            super().__getattribute__(what)._property_of = self
            # set an attribute for the returing property object to tell what is its name in Object class params
            super().__getattribute__(what)._property_name = what
        return super().__getattribute__(what)
    def __setattr__(self, name, value):
        if isinstance(value, Property):
            value._property_name = name
        return super().__setattr__(name, value)

    def __eq__(self, other):
        if isinstance(other, Property):
            print("!!!!!! ALT BEH 2")
            return other.__eq__(self)
        else:
            return super().__eq__(other)
        

class Object(metaclass=BaseObjectMeta):
    def __init__(self, value=None): # WARNING! name is too dangerous to put here!
        self.__unlock_setter = True
        name = None
        self._class_variable = None
        self.value = value
        if name is None: # WARNING name must always be none
            frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
            name = "%s-%s-%s-L%s" % (self.__class__.__name__, str(new_id()), frameinfo.filename, frameinfo.lineno)
        self.name = self.gen_name(name) # object name when instantiating..
        global _problem_compilation
        global _collected_objects
        global _collected_object_classes
        if _problem_compilation:
            _collected_object_classes.add(self.__class__.__name__)
            if not self.__class__.__name__ in _collected_objects:
                _collected_objects[self.__class__.__name__] = [ self.name ]
            else:
                _collected_objects[self.__class__.__name__].append(self.name)
        # when class is instantiated, make sure to "proxy" all properties
        for key in type(self).__dict__:
            # print(key)
            if isinstance(getattr(self, key), Property):
                # print("copying propeorty", key)
                setattr(self, key, copy.copy(getattr(self,key)))
                # for the every property in my Object, 
                #    when instantiating the class
                #    set _property_of_inst to:
                #    - indicate that we are now a property of instantiated object
                #    - have a reference to the mother instance of Object
                getattr(self, key)._property_of_inst = self
        self.__unlock_setter = False
    def gen_name(self, name):
        return ''.join([x if x in (string.ascii_letters+string.digits) else '-' for x in name])
    
    def class_variable(self):
        "we assume to have a variable assigned"
        if self._class_variable == None:
            raise ValueError("Trying to get class variable from unknown instance %s" % self)
        return self._class_variable
        #my_class = self.__class__.__name__
        #myclass_genvar = None
        #for ph in reversed(self.parse_history):
        #    if my_class in ph["variables"]:
        #        myclass_genvar = ph["variables"][my_class]
        #        break
        #return myclass_genvar
    
    def __eq__(self, other):
        if isinstance(other, Property):
            return other.__eq__(self)
        else:
            return super().__eq__(other)
    
    def __setattr__(self, name, value):
        global _problem_compilation
        # if _problem_compilation and isinstance(value, Object):
        #     print("EXEC PC TRYING TO SET ---------------------------------------", name, value)
            
        if _problem_compilation and isinstance(value, Object) and hasattr(self, name) and isinstance(getattr(self, name), Property):
            # print("EXEC SET ---------------------------------------", name, value)
            getattr(self, name).set(value)
        elif _problem_compilation and isinstance(value, bool) and hasattr(self, name) and isinstance(getattr(self, name), Property):
            if value == True:
                getattr(self, name).set()
            else:
                raise NotImplementedError("Boolean False is not supported")
        else:
            # TODO: check if we need this - we may just throw an error???
            if _problem_compilation and hasattr(self, name) and not self.__unlock_setter:
                raise AssertionError("Do not support setting of type %s to property %s (in compilation mode)" % (str(type(value)), name))
            super().__setattr__(name, value)



    # def __getattr__(self, attr):
    #     print ("getting arrt", attr)
    #     return super().__getattr__(self, attr)
    
    # def __getattr__(self, attr):
    #     if attr == "_type_of_property": return super().__getattr__(self, attr)
    #     if hasattr(self, "_type_of_property"):
    #         print("has top", attr)
    #     return super().__getattr__(self, attr)

# A static object initializes itself with instances static_values
class StaticObject(Object):
    # TODO
    pass

class Imaginary(Object):
    pass

class Digit(Object):
    pass


#########################################################################
##
##  Domain Definition
##


#class PlannedAction(metaclass=ActionMeta):
class PlannedAction():
    cost = 1
    
    @classmethod
    def compile(cls):
        # TODO: acquire lock for multithreaded!!!
        global _compilation
        global _collected_predicates
        global _collected_parameters
        global _collected_effects
        global _selector_out
        assert _selector_out is None, "Selector operators used outside of Select() decorator"
        _collected_predicates = []
        _collected_parameters = {}
        _collected_effects = []
        _compilation = True
        print(cls.selector(cls)) # this fills globals above
        print(cls.effect(cls))
        _compilation = False
        
        # _collected_predicates = filter(None, list(set(_collected_predicates)))
        _collected_predicates = list(filter(None, list(OrderedDict.fromkeys(_collected_predicates))))
        collected_parameters = ""
        assert len(_collected_effects) > 0, "Action %s has no effect" % cls.__name__
        assert len(_collected_predicates) > 0, "Action %s has no precondition" % cls.__name__
        for ob in _collected_parameters:
            collected_parameters += "%s - %s " % (ob, _collected_parameters[ob])
        
        return """
    (:action {action_name}
        :parameters ({parameters})
        :precondition (and
            {precondition}
        )
        :effect (and
            {effect}
        )
    )
        """.format(action_name = cls.__name__, 
            parameters=collected_parameters.strip(), 
            precondition='\n            '.join(_collected_predicates),
            effect='\n            '.join(_collected_effects)
        )
    
    def selector(self):
        raise NotImplementedError
        
    def effect(self):
        raise NotImplementedError
    
# problem definition
class Problem:
    
    def addObject(self, obj):
        "Stub method for future Imaginary object support"
        # TODO HERE: add global trigger to protect from objects not added
        return obj
    
    def actions(self):
        raise NotImplementedError("Please implement .actions() method to return list of planned action classes")

    def goal(self):
        raise NotImplementedError("Please implement .goal() method to return goal in XXX format") 

    def run(self, problemName=""):
        counter = 0
        try:
            with open("./.counter", "r") as fd:
                counter = int(fd.read())
        except:
            counter = 0
 
        counter += 1
        with open("./.counter", "w") as fd:
            fd.write(str(counter))
        

        rnd = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        folder_name = "./out/{0:05d}_{1}_{2}".format(counter, problemName,str(datetime.date.today()),rnd)
        os.makedirs(folder_name, exist_ok=True)
        with open("{0}/domain.pddl".format(folder_name), "w+") as fd:
            fd.write(self.compile_domain())
        with open("{0}/problem.pddl".format(folder_name), "w+") as fd:
            fd.write(self.compile_problem())
        max_time = 10000
        # TODO: create "debug" mode to run in os command and show output in real time
        runscript = 'pypy ../downward/fast-downward.py --plan-file "{folder}/out.plan" --sas-file {folder}/output.sas {folder}/domain.pddl {folder}/problem.pddl --evaluator "hff=ff()" --evaluator "hlm=cg(transform=no_transform())" --search "lazy_wastar(list(hff, hlm), preferred = list(hff, hlm), w = 5, max_time={maxtime})"'.format(folder=folder_name, maxtime=max_time)
        std = subprocess.Popen(runscript, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True).stdout
        for line in std:
            print(line.rstrip("\n"))

        
    def compile_actions(self):
        # TODO: collect all predicates while generating
        self.actions_text = ""
        for act in self.actions():
            act.problem = self
            self.actions_text += act.compile()
            act.problem = None
        return self.actions_text
    
    def get_predicates(self):
        global _collected_predicate_templates
        self.predicates_text = "\n        ".join(list(set(_collected_predicate_templates)))
        return self.predicates_text

    def get_actions(self):
        self.compile_actions()
        return self.actions_text

    def get_types(self):
        # collect all types used in both actions and problem objects
        global _collected_object_classes
        return ' '.join(list(_collected_object_classes))

    def compile_domain(self):
        actions = self.get_actions()
        predicates = self.get_predicates()
        types = self.get_types()
        return """
(define (domain poodle-generated)
    (:requirements :strips :typing :equality :negative-preconditions :disjunctive-preconditions)
    (:types
        {types} - object
    )

    (:predicates
        {predicates}
    )

    {actions}
)""".format(types=types, predicates=predicates, actions=actions)

    def compile_problem(self):
        global _problem_compilation
        global _compilation
        global _collected_objects
        global _collected_object_classes
        global _collected_facts
        global _collected_effects
        _problem_compilation = True
        _collected_object_classes = set()
        _collected_objects = {}
        _collected_facts = []
        self.problem()
        self.collected_objects = _collected_objects
        self.collected_object_classes = _collected_object_classes
        self.collected_facts = _collected_facts
        _compilation = True # required to compile the goal
        _collected_effects = []
        self.goal()
        self.collected_goal = _collected_effects
        _compilation = False
        _problem_compilation = False
        txt_objects = ""
        for cls in self.collected_objects:
            txt_objects += " ".join(list(set(self.collected_objects[cls]))) + " - " + cls + " "
        return """
(define (problem poodle-generated)
    (:domain poodle-generated)
    (:objects
        {objects}
    )
    (:init
        {facts}
    )
    (:goal (and
        {goal}
    ))
)
""".format(objects=txt_objects, facts='\n        '.join(self.collected_facts), goal='\n            '.join(self.collected_goal))
