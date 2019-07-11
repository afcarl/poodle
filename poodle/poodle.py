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

from jinja2 import Template
import string
import random
import inspect
import copy, subprocess
from collections import OrderedDict
import os
import datetime
import logging
import sys

# import wrapt
# import infix

log = logging.getLogger()
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout) # loggging driver
handler.setLevel(logging.DEBUG) #loglevel ->> CRITICAL ERROR WARNING INFO DEBUG NOTSET
log.addHandler(handler)

_compilation = False
_problem_compilation = False
_effect_compilation = False

_collected_predicates = []
_collected_effects = []
_collected_parameters = {}
_selector_out = None
_collected_predicate_templates = [] # TODO: localize state! also not all predicates may be used in problem actions
_collected_object_classes = set()
_collected_objects = {} # format: { "class": [ ... objects ... ] }
_collected_facts = []

HASHNUM_VAR_NAME = "hashnum"
HASHNUM_ID_PREDICATE = HASHNUM_VAR_NAME
HASHNUM_CLASS_NAME = "PoodleHashnum"
HASHNUM_EXISTS_PFX = "-hashnum-exists" # predicate postfix to indicate existence of imaginary object
HASHNUM_DEPTH_DEFAULT = 2 # "bit" depth of hashnums
HASHNUM_COUNT_DEFAULT = 10 # default amount of generated hashnums

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
    
def Unselect(what):
    global _collected_predicates
    ret = Select(what)
    if ret._parse_history[-1]["text_predicates"][-1] != None:
        raise AssertionError("Complex Unselect()'s are not supported")
    if _collected_predicates[-1] != None:
        raise AssertionError("Complex Unselect()'s are not supported")
    assert ret._parse_history[-1]["text_predicates"][0] == _collected_predicates[-2], "Internal Error: Could not find what to unselect"
    _collected_predicates[-2] = "(not %s)" % _collected_predicates[-2]
    return ret

# https://stackoverflow.com/a/2257449
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

id_counter = 0
def new_id():
    global id_counter
    id_counter += 1
    return id_counter

def gen_var(name, prefix=""):
    return "?%s%s-%s" % (prefix, name, new_id())

def gen_var_imaginary(name, depth=2, prefix=""):
    # TODO: depth support for more than 2 hashnums
    hid = new_id()
    return "?%s%s1-%s ?%s%s2-%s" % (prefix, HASHNUM_VAR_NAME, hid, prefix, HASHNUM_VAR_NAME, hid)

def gen_hashnums(amount):
    global _collected_facts
    hashnums_generated = []
    for i in range(amount): 
        hashnum = PoodleHashnum()
        hashnums_generated.append(hashnum)
        _collected_facts.append("({pred} {hname})".format(pred=HASHNUM_ID_PREDICATE, hname=hashnum.name))
    return hashnums_generated


def class_or_hash(var_name, class_name):
    if HASHNUM_VAR_NAME in var_name:
        return HASHNUM_CLASS_NAME
    return class_name
    
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
        my_class_name = prop._property_of.__name__
    elif not has_po and has_poi:
        my_class_name = type(prop._property_of_inst).__name__
    elif has_po and has_poi:
        my_class_name = prop._property_of.__name__
    else:
        raise ValueError("Can not detect who I am")
    return my_class_name

def gen_hashnum_templates(var, prefix="var"):
    return " ".join(["?%s%s - %s" % (prefix, i, HASHNUM_CLASS_NAME) for i, v in zip(range(len(var.split())), var.split())])

def gen_text_predicate_push_globals(class_name, property_name, var1, var1_class, var2, var2_class):
    # return gen_text_predicate_globals(class_name+"-"+property_name, var1, var1_class, var2, var2_class)
# def gen_text_predicate_globals(predicate_name, var1, var1_class, var2, var2_class):
    global _collected_predicate_templates
    global _collected_object_classes
    predicate_name = class_name+"-"+property_name
    #if not imaginary:
        # text_predicate = "(" + predicate_name + " " + var1 + " - " + var1_class + " " + var2 + " - " + var2_class + ")" # preconditions with classes not supported
    # TODO HERE: looks like we can match the class by "id" which is N-hashnum variable
    text_predicate = "(" + predicate_name + " " + var1 + " " + var2 + ")"
    if " " in var1 and not " " in var2:
        _collected_predicate_templates.append("(" + predicate_name + " " + gen_hashnum_templates(var1) + " ?var2 - " + var2_class + ")")
        _collected_object_classes.update([class_name, HASHNUM_CLASS_NAME, var2_class])
    elif not " " in var1 and " " in var2:
        _collected_predicate_templates.append("(" + predicate_name + " ?var1 - " + var1_class + " " + gen_hashnum_templates(var2) + ")")
        _collected_object_classes.update([class_name, var1_class, HASHNUM_CLASS_NAME])
    elif " " in var1 and " " in var2:
        _collected_predicate_templates.append("(" + predicate_name + " " + gen_hashnum_templates(var1) + " " + gen_hashnum_templates(var2, prefix="var2") + ")")
        _collected_object_classes.update([class_name, HASHNUM_CLASS_NAME])
    else:
        _collected_predicate_templates.append("(" + predicate_name + " ?var1 - " + var1_class + " ?var2 - " + var2_class + ")")
        _collected_object_classes.update([class_name, var1_class, var2_class])
    #else:
        #TODO HERE
    #    obj_predicate_id = get_imaginary_object_id()
    #    text_predicate = "(" + predicate_name + " " + obj_predicate_id + " " + var1 + " " + var2 + ")"

    return text_predicate

def gen_one_predicate(predicate_name, var, var_class_name):
    global _collected_predicate_templates
    global _collected_object_classes
    text_predicate = "("+predicate_name+" "+var+")"
    if " " in var:
        _collected_predicate_templates.append("(" + predicate_name + " " + gen_hashnum_templates(var) + ")")
    else:
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

    def get_property_class_name(self):
        return self.get_parent_class().__name__

    def get_parent_class(self):
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
        #print("get_property_class: _property_of:", has_po, "_property_of_inst:", has_poi) # nosiy!
        
        if has_po and not has_poi:
            my_class = self._property_of
        elif not has_po and has_poi:
            my_class = type(self._property_of_inst)
        elif has_po and has_poi:
            my_class = self._property_of
        else:
            raise ValueError("Can not detect who I am")
        return my_class

    def gen_predicate_name(self):
        return self.get_property_class_name()+"-"+self._property_name
        
    def find_parameter_variable(self):
        "finds the variable that holds the class"
        my_class_name = self._value.__name__ # _value is always a class
        myclass_genvar = None
        for ph in reversed(self._property_of_inst._parse_history):
            if my_class_name in ph["variables"]:
                myclass_genvar = ph["variables"][my_class_name]
                break
        return myclass_genvar
    
    
    def find_class_variable(self):
        "finds the variable that holds the class"
        my_class_name = self.get_property_class_name()
        myclass_genvar = None
        if self._property_of_inst._class_variable: return self._property_of_inst._class_variable
        for ph in reversed(self._property_of_inst._parse_history):
            if my_class_name in ph["variables"]:
                myclass_genvar = ph["variables"][my_class_name]
                break
        return myclass_genvar
    
    def operator(self, other, operator="equals", dir_hint="straight"):
        assert operator == "equals" or operator == "contains"
        global _compilation
        global _collected_predicates
        global _collected_parameters
        global _collected_predicate_templates
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
        
        log.debug("OPERATOR-1: {0}{1}{2}{3}{4}".format(self._property_name, operator, subjObjectClass, self._property_of, type(self._property_of)))
        
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
        #     my_class_name = self._property_of.__name__
        # elif not has_po and has_poi:
        #     my_class_name = type(self._property_of_inst).__name__
        # elif has_po and has_poi:
        #     my_class_name = self._property_of.__name__
        # else:
        #     raise ValueError("Can not detect who I am")
        my_class_name = self.get_property_class_name()
        my_class = self.get_parent_class()
        
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
        if not hasattr(self, "_property_of_inst") and not hasattr(other, "_property_of_inst") and not isinstance(other, Object):
            raise AssertionError("Both LHS and RHS are classes. Do not know what to instantiate.")
        elif type(self._property_of) is BaseObjectMeta and not hasattr(self, "_property_of_inst"):
            log.debug("OPERATOR: Decided to return SELF.property_of()")
            obj=self._property_of() # contains who am I the property of.. (meta)
            who_instantiating = "self"
        # Else, if the thing we are comparing ourself to (subj) is class and not instance
        #    vvv---always-true--------------vvv         vvv----check-if-subj-is-instance--vvv
        elif type(subjObjectClass) is BaseObjectMeta and not isinstance(subjObjectClass, Object) and not hasattr(other, "_property_of_inst"):
            log.debug("OPERATOR: Decided to return subj() objecs")
            who_instantiating = "other" 
            # The following is the fix for scenario Select(Class.prop1 in inst.prop2)
            #    in this scenario, without this fix return value and class name are wrong
            if hasattr(other, "_value") and subjObjectClass == other._value:
                obj = other._property_of() # TODO HERE - think what should happen next...
                who_instantiating_fix = True # Fix for bug with instantiating Class.prop in inst.prop2
            else:
                obj = subjObjectClass()
                who_instantiating_fix = False # Fix for bug with instantiating Class.prop in inst.prop2
        else:
            if _compilation: # actually means "running selector" and would be better renamed as `_selector_mode`
                # PART 3.1.
                # in compilation mode, we can return anything we want as result is not being used in later computations
                log.debug("OPERATOR IN COMPILATION/SELECTOR MODE")
                # obj = self._value()
                if dir_hint == "reverse": # for ABC.RSelect support
                    obj = other._property_of_inst
                else:
                    obj = self._property_of_inst
                who_instantiating = None
            else:
                raise ValueError("No class to select is present in selector expression. Both LHS and RHS are instances.")
            
        if isinstance(subjObjectClass, Object):
            other_class_name = type(subjObjectClass).__name__
            other_class = type(subjObjectClass)
        else:
            other_class_name = subjObjectClass.__name__
            other_class = subjObjectClass
        
        # Part 5. Get history of generated variables
        # Variants:
        # 1. we are property of instance, thus self._property_of_inst._parse_history
        # 2. the other is instance, thus other._parse_history
        # 3. the other is property of instance, thus other._property_of_inst._parse_history
        #    TODO XXX NOTE: need to look for toplevel object always, as we may be property-of-property
        _parse_history = []
        if has_poi and hasattr(self._property_of_inst, "_parse_history"):
            #print("OPERATOR HIST:", "1. we are property of instance")
            if not _compilation: assert _parse_history == []
            _parse_history += self._property_of_inst._parse_history
        if isinstance(other, Object) and hasattr(other, "_parse_history"):
            #print("OPERATOR HIST:", "2. the other is instance")
            if not _compilation: assert _parse_history == []
            _parse_history += other._parse_history
        if isinstance(other, Property) and hasattr(other, "_property_of_inst") and hasattr(other._property_of_inst, "_parse_history"):
            #print("OPERATOR HIST:", "3. the other is property of instance")
            if not _compilation: assert _parse_history == []
            _parse_history += other._property_of_inst._parse_history
        #print("OPERATOR-HIST-1", _parse_history)
        other_genvar = None
        myclass_genvar = None
        
        # no need to generate other_genvar if other is an instance and already has a variable
        if who_instantiating != "other": # means that other is already an instance, both in regular and compilatioin mode
            # it is either an instance itself or is a property of instance
            if hasattr(other, "_property_of_inst") and other_class_name == other._property_of_inst.__class__.__name__: # weird check to figure out if this is applicable scenario...
                if other._property_of_inst._class_variable:
                    log.debug("OPERATOR: Found other porperty variable {0} {1} {2}".format(other._property_of_inst._class_variable, other_class_name, other._property_of_inst))
                    other_genvar = other._property_of_inst._class_variable
            elif not hasattr(other, "_property_of_inst"):
                if hasattr(other, "_class_variable") and other._class_variable:
                    log.debug("OPERATOR: Found other instance variable {0} {1}".format(other._class_variable, other_class_name))
                    other_genvar = other._class_variable
            else:
                log.debug("OPERATOR Skipping getting variable from instances")
                pass
                
        if has_poi and self._property_of_inst._class_variable:
            myclass_genvar = self._property_of_inst._class_variable
        # WARNING@!!!! finding variables in history is obsolete and UNSAFE!!!
        if _parse_history:
            if not other_genvar:
                for ph in reversed(_parse_history):
                    if other_class_name in ph["variables"] and who_instantiating != "other": # only generate new var if we are instantiating it here
                        other_genvar = ph["variables"][other_class_name]
                        log.debug("WARNING! Variable found in history - resulted PDDL may be wrong")
                        break
            for ph in reversed(_parse_history):
                if has_poi and self._property_of_inst._class_variable:
                    myclass_genvar = self._property_of_inst._class_variable
                else:
                    if my_class_name in ph["variables"] and who_instantiating != "self":
                        myclass_genvar = ph["variables"][my_class_name]
                        break
                    
        if myclass_genvar is None: 
            if issubclass(my_class, Imaginary):
                myclass_genvar = gen_var_imaginary(my_class_name)
                my_class_name = HASHNUM_CLASS_NAME
            else:
                myclass_genvar = gen_var(my_class_name)
        if other_genvar is None: 
            if issubclass(other_class, Imaginary):
                other_genvar = gen_var_imaginary(other_class_name)
                other_class_name = HASHNUM_CLASS_NAME
            else:
                other_genvar = gen_var(other_class_name)
            log.debug("OPERATOR: generating new var for other! {0}".format(other_genvar))
        
        collected_parameters = {other_genvar: class_or_hash(other_genvar, other_class_name), myclass_genvar: class_or_hash(myclass_genvar, my_class_name)}
        
        if property_property_comparison:
            other_property_class_name = get_property_class_name(other)
            other_property_class = other.get_parent_class()
            other_property_genvar = None
            if _parse_history:
                for ph in reversed(_parse_history):
                    if other_property_class_name in ph["variables"] and who_instantiating != "other": # only generate new var if we are instantiating it here
                        other_property_genvar = ph["variables"][other_property_class_name]
                        break
            if other_property_genvar is None: 
                if issubclass(other_property_class, Imaginary):
                    other_property_genvar = gen_var_imaginary(other_property_class_name)
                    other_property_class_name = HASHNUM_CLASS_NAME
                else:
                    other_property_genvar = gen_var(other_property_class_name)
            collected_parameters[other_property_genvar] = class_or_hash(other_property_genvar, other_property_class_name)
            text_predicate = gen_text_predicate_push_globals(my_class_name, self._property_name, myclass_genvar, my_class_name, other_genvar, other_class_name)
            text_predicate_2 = gen_text_predicate_push_globals(other_property_class_name, other._property_name, other_property_genvar, other_property_class_name, other_genvar, other_class_name)
            log.debug("OPERATOR-PRECOND-PDDL1: {0}".format(text_predicate))
            log.debug("OPERATOR-PRECOND-PDDL2: {0}".format(text_predicate_2))
        else:
            text_predicate = gen_text_predicate_push_globals(my_class_name, self._property_name, myclass_genvar, my_class_name, other_genvar, other_class_name)
            text_predicate_2 = None
            log.debug("OPERATOR-PRECOND-PDDL: {0}".format(text_predicate))
        
        # print("OPERATOR-PARAM-PDDL:", collected_parameters)
        
        if not hasattr(obj, "_parse_history"):
            obj._parse_history = _parse_history
        else:
            obj._parse_history += _parse_history
        
        # TODO: what if we have two same classes?
        
        # TODO: a new method for variable storage!
        #       store the variable in object returned - and use it first whenever needed

        # store variable that we created for the returning object
        if who_instantiating == "self": # returning object is our class, and we just invented a new variable name for us
            log.debug("OPERATOR setting class variable myclass genvar to {0} {1}".format(myclass_genvar, my_class_name))
            obj._class_variable = myclass_genvar
        if who_instantiating == "other": # returning object is who we are being compared to, and we invented variable for that
            log.debug("OPERATOR setting class variable ohter genvar to {0} {1}".format(other_genvar, other_class_name))
            if who_instantiating_fix: # Fix for bug with instantiating Class.prop in inst.prop2
                obj._class_variable = other_property_genvar
            else:
                obj._class_variable = other_genvar
            
        # also store variable for the instantiated object that we are comparing with, if not created before
        if has_poi: # is exactly equivalent to who_instantiating == other, means that we(who we property of) are not a class
            if not self._property_of_inst._class_variable is None:
                log.warning("WARNING! _class_variable is  {0} but we are generating {1}".format(self._property_of_inst._class_variable, myclass_genvar))
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
                    log.warning("WARNING! Not setting other variable to {0} as it already has {1}".format(other_genvar, other._class_variable))

        
        obj._parse_history.append({
            "operator": operator, 
            "self": self, 
            "other": subjObjectClass, 
            "self-prop": self._value, 
            #"variables": { other_class_name: other_genvar , my_class_name: myclass_genvar }, # TODO: what if we have two same classes?
            "variables": {my_class_name: myclass_genvar, other_class_name: other_genvar }, # TODO: what if we have two same classes?
            "class_variables": { my_class_name: myclass_genvar },
            "text_predicates": [text_predicate, text_predicate_2],
            "parameters": collected_parameters
        })
        #print("OPERATOR-HIST-2", _parse_history)

        # this is required for the variables to become available at selector compilation
        # if has_poi and _compilation and not hasattr(self._property_of_inst, "_parse_history"): self._property_of_inst._parse_history = _parse_history
        if has_poi and not hasattr(self._property_of_inst, "_parse_history"): self._property_of_inst._parse_history = _parse_history
        if has_poi and hasattr(self._property_of_inst, "_parse_history"): self._property_of_inst._parse_history += _parse_history
        
        if _compilation:
            # because in compilation mode our _parse_history now contains merged history ->>>
            for ph in obj._parse_history + _parse_history: # WARNING! why do we need to add ph here??
                _collected_predicates += ph["text_predicates"]
                _collected_parameters.update(ph["parameters"])
        return obj
        
    def equals(self, other):
        return self.operator(other, "equals")

    def __eq__(self, other):
        global _selector_out
        if hasattr(self, "_property_of_inst") and isinstance(other, Property) and not hasattr(other, "_property_of_inst"):
            log.warning("!!!!!! ALT BEH 1 - me is {0} {1} other is {2} ".format(self, self._property_of_inst, other))
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
        for ph in self._property_of_inst._parse_history:
            _collected_predicates += ph["text_predicates"]
            _collected_parameters.update(ph["parameters"])
        if valueObjectObject:
            for ph in valueObjectObject._parse_history:
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
            log.warning("WARNING! Using experimental support for what=None")
            _collected_effects.append("(not ("+self.gen_predicate_name()+" "+self.find_class_variable()+" "+self.find_parameter_variable+"))")
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
                    log.debug("%s is returning copy of val %s %s which is %s" % (self, attr, ob, self._value))
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
        for ph in self._property_of_inst._parse_history:
            _collected_predicates += ph["text_predicates"]
            _collected_parameters.update(ph["parameters"])
        
    def set(self):
        global _collected_effects
        global _collected_facts
        global _problem_compilation
        # print("EFFECT-PDDL: TODO", self._property_of_inst.__class__.__name__)
        # print("EFFECT-PDDL: TODO", self._property_of_inst._parse_history)
        # now find in our instance's _parse_history our instance's class name variable
        
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
            log.debug("GOP returning {0} {1}".format(what, self._type_of_property))
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
            log.warning("!!!!!! ALT BEH 2")
            return other.__eq__(self)
        else:
            return super().__eq__(other)
        

class Object(metaclass=BaseObjectMeta):
    def __init__(self, value=None): # WARNING! name is too dangerous to put here!
        self._parse_history = [] # Experimentally setting to fix #78
        global _effect_compilation
        global _problem_compilation
        if not hasattr(self, "__imaginary__"): self.__imaginary__ = False
        if _effect_compilation and not self.__imaginary__:
            raise AssertionError("Object instantiation is prohibited in effect. Use Imaginary instead.")
        self.__unlock_setter = True
        name = None
        self._class_variable = gen_var(self.__class__.__name__, prefix="default-")
        self.value = value
        self.name = ""
        if _problem_compilation:
            if name is None: # WARNING name must always be none
                frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
                name = "%s-%s-%s-L%s" % (self.__class__.__name__, str(new_id()), os.path.basename(frameinfo.filename), frameinfo.lineno)
            self.name = self.gen_name(name) # object name when instantiating..
        global _collected_objects
        global _collected_object_classes
        if _problem_compilation:
            self._parse_history = []
            self._class_variable = self.name
            if not self.__imaginary__:
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
        #my_class_name = self.__class__.__name__
        #myclass_genvar = None
        #for ph in reversed(self._parse_history):
        #    if my_class_name in ph["variables"]:
        #        myclass_genvar = ph["variables"][my_class_name]
        #        break
        #return myclass_genvar
    
    @classmethod
    def Select(cls, **kwargs):
        "ret = Class.Select(prop1=inst1,prop2=inst2,...) is equivalent to \
        v1=Select(Class.prop1 in/== inst1) and ret = Select(v1.prop2 in/== inst2)"
        global _compilation
        ret = cls
        _compilation = True
        for k,v in kwargs.items(): 
            ret = getattr(ret,k).operator(v)
        _compilation = False
        return ret
     
    @classmethod
    def RSelect(cls, **kwargs):
        "ret = Class.RSelect(prop1=inst1,prop2=inst2,...) is equivalent to \
        v1=Select(inst1 in/== Class.prop1) and ret = Select(inst2 in/== v1.prop2)"
        global _compilation
        # ret1 = list(kwargs.items())[0][1].operator(getattr(cls,list(kwargs.items())[0][0]))
        # ret = ret1
        ret = cls
        _compilation = True
        # for k,v in list(kwargs.items())[1:]: 
        for k,v in kwargs.items(): 
            ret = v.operator(getattr(ret,k),dir_hint="reverse")
        _compilation = False
        return ret
        
    def __eq__(self, other):
        if isinstance(other, Property):
            return other.__eq__(self)
        else:
            return super().__eq__(other)
    
    def __setattr__(self, name, value):
        global _problem_compilation
        global _compilation
       
        # if _problem_compilation and isinstance(value, Object):
        #     print("EXEC PC TRYING TO SET ---------------------------------------", name, value)
            
        if (_compilation or _problem_compilation) and isinstance(value, Object) and hasattr(self, name) and isinstance(getattr(self, name), Property):
            # print("EXEC SET ---------------------------------------", name, value)
            getattr(self, name).set(value)
        elif _problem_compilation and isinstance(value, bool) and hasattr(self, name) and isinstance(getattr(self, name), Property):
            if value == True:
                getattr(self, name).set()
            else:
                raise NotImplementedError("Boolean False is not supported")
        else:
            # WARNING! please check the proper usage of __unlock_setter
            # setter must probably unlock only for non-existent class attributes or only for existing properties
            if ( _problem_compilation or _compilation) and hasattr(self, name) and not self.__unlock_setter and isinstance(getattr(self, name), Property):
                raise AssertionError("No support for setting of type %s to property %s (in compilation mode)" % (str(type(value)), name))
            if _compilation and name[0] != "_" and not hasattr(self, name) and not "__unlock_setter" in name and not self.__unlock_setter: # all system properties must start with _
            #if _compilation and not hasattr(self, name) and not "__unlock_setter" in name:
                raise AssertionError("New properties setting is not allowed in compilation mode, please define %s as Property of %s" % (name, self.__class__))
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
    
    def gen_name(self, name):
        global _problem_compilation
        if _problem_compilation:
            hns = gen_hashnums(HASHNUM_DEPTH_DEFAULT)
            return ' '.join([v.name for v in hns])
        else:
            return super().gen_name(name)
    
    def __init__(self):
        self.__imaginary__ = True
        super().__init__()
        self._class_variable = gen_var_imaginary(self.__class__.__name__, prefix="im-default-")
        global _effect_compilation
        global _collected_predicates
        global _collected_effects
        global _collected_parameters
        if _effect_compilation:
            self._parse_history = []
            self._class_variable = gen_var_imaginary(self.__class__.__name__)
            exists_predicate = gen_one_predicate(self.__class__.__name__+HASHNUM_EXISTS_PFX, self._class_variable, self.__class__.__name__)
            for v in self._class_variable.split():
                _collected_predicates.append("("+HASHNUM_ID_PREDICATE + " " + v + ")")
            _collected_predicates.append("(not %s)" % exists_predicate)
            _collected_predicate_templates.append("("+HASHNUM_ID_PREDICATE+" ?var - "+HASHNUM_CLASS_NAME+")")
            _collected_predicate_templates.append("({pred} ?var - {cls})".format(pred=HASHNUM_ID_PREDICATE, cls=HASHNUM_CLASS_NAME))
            _collected_effects.append(exists_predicate)
            _collected_parameters[self._class_variable] = HASHNUM_CLASS_NAME



class Digit(Object):
    pass

class PoodleHashnum(Object):
    "hashnum is used in imaginary object identification"
    pass # unsorted, unopimized

#########################################################################
##
##  Domain Definition
##


#class PlannedAction(metaclass=ActionMeta):
class PlannedAction():
    cost = 1
    argumentList = []
    parameterList = []
    problem = None
    template = None

    def __init__(self, argumentList):
        self.argumentList = argumentList
#        print("argument list ",self.argumentList  )
    
    def __str__(self):
        ret = "{0}".format(self.__class__.__name__)
        for arg in self.argumentList:
            ret +=" {0}({1})".format(arg.name, arg.value)
        return ret

    def templateMe(self):
        return self.__str__()

    @classmethod
    def compile(cls, problem):
        # TODO: acquire lock for multithreaded!!!
        global _compilation
        global _collected_predicates
        global _collected_parameters
        global _collected_effects
        global _selector_out
        global _effect_compilation
        assert _selector_out is None, "Selector operators used outside of Select() decorator while compiling %s in %s" % (cls, problem)
        _collected_predicates = []
        _collected_parameters = {}
        _collected_effects = []
        _compilation = True
        cls.problem = problem
        log.info("{0}".format(cls.selector(cls))) # this fills globals above
        _effect_compilation = True
        log.info("{0}".format(cls.effect(cls)))
        _effect_compilation = False
        _compilation = False
        
        # _collected_predicates = filter(None, list(set(_collected_predicates)))
        _collected_predicates = list(filter(None, list(OrderedDict.fromkeys(_collected_predicates))))
        collected_parameters = ""
        assert len(_collected_effects) > 0, "Action %s has no effect" % cls.__name__
        assert len(_collected_predicates) > 0, "Action %s has nothing to select" % cls.__name__
        for ob in _collected_parameters:
            if " " in ob:
                # WARNING! this is because of how imaginary variables are implemented
                collected_parameters += "%s - %s " % (ob.split()[0], _collected_parameters[ob])
                collected_parameters += "%s - %s " % (ob.split()[1], _collected_parameters[ob])
            else:
                collected_parameters += "%s - %s " % (ob, _collected_parameters[ob])
        
        return """
    (:action {action_name}
        :parameters ({parameters})
        :precondition (and
            {precondition}
        )
        :effect (and
            {effect}
            {cost}
        )
    )
        """.format(action_name = cls.__name__, 
            parameters=collected_parameters.strip(), 
            precondition='\n            '.join(_collected_predicates),
            effect='\n            '.join(_collected_effects),
            cost='(increase (total-cost) {0})'.format(cls.cost)
        )
    
    def selector(self):
        raise NotImplementedError
        
    def effect(self):
        raise NotImplementedError
    

class PlannedActionJinja2(PlannedAction):
    template = "./template/default.j2"

    def templateMe(self, template=None):
        fileIn = ""
        with open(self.template, "r") as fd:
            fileIn = fd.read()
        template = Template(fileIn)
        param = []
        for arg in self.argumentList:
            args = []
            args.append(arg.name)
            args.append(arg.value)
            param.append(args)
        return template.render(action=self.__class__.__name__, parameters=param)

    def getTemplate(self):
        if self.template == None:
            return "./template/{0}.j2".format(self.__class__.__name__)
        return selt.template

# problem definition
class Problem:
    HASHNUM_COUNT = HASHNUM_COUNT_DEFAULT # amount of hashnums generated for imaginary object
    HASHNUM_DEPTH = HASHNUM_DEPTH_DEFAULT # only 2 is currently supported, waring! set globally only!
    folder_name = None
    objectList = []
    def __init__(self):
        self._has_imaginary = False
    def getFolderName(self):
        return self.folder_name
    
    def addObject(self, obj):
        self.objectList.append(obj)
        return obj
    
    def getObjectList(self):
        return self.objectList

    def actions(self):
        raise NotImplementedError("Please implement .actions() method to return list of planned action classes")

    def getActionByName(self):
        strList = []
        for action in self.action():
            strList.append(action.__class__.__name__)
        return strList

    def goal(self):
        raise NotImplementedError("Please implement .goal() method to return goal in XXX format") 

    def run(self):
        global _collected_parameters
        print(_collected_parameters)
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
        self.folder_name = "./out/{0:05d}_{1}_{2}".format(counter, self.__class__.__name__, str(datetime.date.today()),rnd)
        os.makedirs(self.folder_name, exist_ok=True)
        with open("{0}/problem.pddl".format(self.folder_name), "w+") as fd:
            fd.write(self.compile_problem())
        with open("{0}/domain.pddl".format(self.folder_name), "w+") as fd:
            fd.write(self.compile_domain())
        max_time = 10000
        # TODO: create "debug" mode to run in os command and show output in real time
        runscript = 'pypy ../downward/fast-downward.py --plan-file "{folder}/out.plan" --sas-file {folder}/output.sas {folder}/domain.pddl {folder}/problem.pddl --evaluator "hff=ff()" --evaluator "hlm=cg(transform=no_transform())" --search "lazy_wastar(list(hff, hlm), preferred = list(hff, hlm), w = 5, max_time={maxtime})"'.format(folder=self.folder_name, maxtime=max_time)
        std = subprocess.Popen(runscript, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True).stdout
        retcode = "-1"
        for line in std:
            if line.find('search exit code:') != -1:
                retcode = line.rstrip("\n").split()[3]
            log.info(line.rstrip("\n"))
        if retcode == "0" :
            if self.getFolderName() != None:
                actionClassLoader = ActionClassLoader(self.actions(), self)
                actionClassLoader.loadFromFile("{0}/out.plan".format(self.getFolderName()))
        return retcode

        
    def compile_actions(self):
        # TODO: collect all predicates while generating
        self.actions_text = ""
        for act in self.actions():
            act.problem = self
            self.actions_text += act.compile(self)
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
        if HASHNUM_ID_PREDICATE in predicates:
            self._has_imaginary = True # TODO REMOVE as this does not work due to order of compilation
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
    (:functions
        (total-cost)
    )

    {actions}
)""".format(types=types, predicates=predicates, actions=actions)

    def has_imaginary(self):
        #return self._has_imaginary # this does not work as order of compilation prevents
        return True # TODO: find a way to detect if imaginary objects are present
        # one option

    def gen_hashnums(self, amount=0):
        if amount == 0: amount = self.HASHNUM_COUNT 
        for hn in gen_hashnums(amount):  self.addObject(hn)


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
        if self.has_imaginary(): self.gen_hashnums()
        self.collected_objects = _collected_objects
        self.collected_object_classes = _collected_object_classes
        self.collected_facts = _collected_facts
        _compilation = True # required to compile the goal
        _collected_effects = []
        self.goal()
        global _selector_out
        _selector_out = None # cleaner goal
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
    (:metric minimize (total-cost))
)
""".format(objects=txt_objects, facts='\n        '.join(self.collected_facts), goal='\n            '.join(self.collected_goal))

class ActionClassLoader:
    actionList = [] #list of the ActionPlanned type
    planList = [] #list instances of the ActionPlanned type
    problem = None
    # put as argument for constructor list of the ActionPlanned type which got from Problem.actions()
    def __init__(self, actionList):
        self.actionList = actionList

    def __init__(self, actionList, problem):
        self.actionList = actionList
        self.problem = problem

    # put here action step string line from out.plan without "()"
    # please load action sequentially
    def load(self, planString):
        actionString = str(planString).split()[0]
        for action in self.actionList:
            if action.__name__.lower() == actionString.lower():
                argumentList = []
                for argStr in str(planString).split()[1:]:
                    for obj in self.problem.getObjectList():
#                        print("test",obj)
                        if isinstance(obj, Object):
#                            print("test again",obj," ", obj.name )
                            if argStr.lower() == obj.name.lower():
                                argumentList.append(obj)
                             #   log.debug("got {0}".format(obj.name))
                plannedAction = action(argumentList)
                self.planList.append(plannedAction)
              #  log.info(plannedAction)
                log.info(plannedAction.templateMe())

    def loadFromFile(self, outPlanFile):
        log.debug("load action from file {0}".format(outPlanFile))
        with open(outPlanFile, "r") as fd:
            for planLine in fd:
                self.load(planLine.replace("(", "").replace(")", ""))
