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
import inspect, functools
import copy, subprocess, tempfile
from collections import OrderedDict
import os
import datetime
import logging
import sys, time
import requests
import base64 
import json

# import wrapt
# import infix

log = logging.getLogger()
log.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout) # loggging driver
handler.setLevel(logging.ERROR) #loglevel ->> CRITICAL ERROR WARNING INFO DEBUG NOTSET
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
_poodle_object_classes = {}
_replaced_predicates = {}

_none_objects = {}
_system_objects = {}

HASHNUM_VAR_NAME = "hashnum"
HASHNUM_ID_PREDICATE = HASHNUM_VAR_NAME
HASHNUM_CLASS_NAME = "PoodleHashnum"
HASHNUM_EXISTS_PFX = "-hashnum-exists" # predicate postfix to indicate existence of imaginary object
HASHNUM_DEPTH_DEFAULT = 2 # "bit" depth of hashnums
HASHNUM_COUNT_DEFAULT = 10 # default amount of generated hashnums

SOLVER_KEY = "list(filter(None, _collected_predicates + _collected_effects))"
SOLVER_PROCESSING_STATUS = 'PROCESSING'
SOLVER_ERROR_STATUS = 'ERROR'
SOLVER_UNKNOWN_STATUS = 'UNKNOWN'
SOLVER_DONE_STATUS = 'DONE'
SOLVER_KILLED_STATUS = 'KILLED'
SOLVER_MAX_TIME = 30
SOLVER_CHECK_TIME = 2
SOLVER_URL = 'http://devapi.xhop.ai:8082' #'http://127.0.0.1:8082' # 

def crypt(key, data):
    S = list(range(256))
    j = 0

    for i in list(range(256)):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    j = 0
    y = 0
    out = []

    for char in data:
        j = (j + 1) % 256
        y = (y + S[j]) % 256
        S[j], S[y] = S[y], S[j]

        out.append(chr(ord(char) ^ S[(S[j] + S[y]) % 256]))

    return ''.join(out)


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
    global _compilation
    if not _compilation and type(_selector_out) == type([]):
        raise AssertionError("Object comparison outside of Select() or complex selector outside of selector() method")
    ret = _selector_out
    _selector_out = None
    return ret
    
def Unselect(what):
    global _collected_predicates
    global _replaced_predicates
    ret = Select(what)
    if type(ret) == type([]):
        raise AssertionError("Complex Unselect()'s are not supported")
    # WARNING BELOW! we can not rely on _parse_history anymore as returned objects may be anything
    # if ret._parse_history[-1]["text_predicates"][-1] != None:
    #     raise AssertionError("Complex Unselect()'s are not supported")
    if _collected_predicates[-1] != None:
        raise AssertionError("Unselect()'s with subproperty comparisons are not supported")
    # search_pred = ret._parse_history[-1]["text_predicates"][0]
    search_pred = _collected_predicates[-2] # WARNING! this depends on order of added stuff to _collected_predicates
    replace_pred = "(not %s)" % search_pred
    # while search_pred in _collected_predicates: _collected_predicates.remove(search_pred)
    # _collected_predicates = [replace_pred if x==search_pred else x for x in _collected_predicates]
    # _collected_predicates.append(replace_pred)
    _replaced_predicates[search_pred] = replace_pred
    if not ret: return None
    return ret

# https://stackoverflow.com/a/2257449
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

from inspect import FrameInfo, istraceback, isframe, getsourcefile, getfile, findsource, Traceback
def getouterframes(frame, context=1):
    framelist = []
    while frame:
        frameinfo = (frame,) + getframeinfo(frame, context)
        framelist.append(FrameInfo(*frameinfo))
        frame = frame.f_back
    return framelist

def getframeinfo(frame, context=1):
    if istraceback(frame):
        lineno = frame.tb_lineno
        frame = frame.tb_frame
    else:
        lineno = frame.f_lineno
    if not isframe(frame):
        raise TypeError('{!r} is not a frame or traceback object'.format(frame))

    filename = getsourcefile(frame) or getfile(frame)
    if context > 0:
        start = lineno - 1 - context//2
        try:
            lines, lnum = findsource(frame)
        except (OSError, IndexError): # fix: added IndexError
            lines = index = None
        else:
            start = max(0, min(start, len(lines) - context))
            lines = lines[start:start+context]
            index = lineno - 1 - start
    else:
        lines = index = None

    return Traceback(filename, lineno, frame.f_code.co_name, lines, index)

def get_source_frame_dict():
    frame = getouterframes(inspect.currentframe())[4]
    for f in getouterframes(inspect.currentframe()):
        frameinfo = getframeinfo(f[0])
        if frameinfo.code_context and  ("Select(" in frameinfo.code_context[0].strip().replace(" ","") or frameinfo.code_context[0].strip().startswith("assert")):
            frame = f
            break
    frameinfo = getframeinfo(frame[0])
    try:
        c_string = frameinfo.code_context[0].strip()
    except TypeError:
        c_string = "(UNKNOWN)"
    return {
                    "code": c_string,
                    "line": frameinfo.lineno,
                    "file": frameinfo.filename
            }

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
    
def push_selector_object(obj):
    global _selector_out
    if _selector_out:
        log.debug("CHECK - selector output not null")
        if type(_selector_out) == type([]):
            _selector_out.append(obj)
        else:
            _selector_out = [_selector_out, obj]
    else:
        _selector_out = obj
    
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
    if property_name: predicate_name = class_name+"-"+property_name
    else: 
        predicate_name = class_name
        class_name = None
    #if not imaginary:
        # text_predicate = "(" + predicate_name + " " + var1 + " - " + var1_class + " " + var2 + " - " + var2_class + ")" # preconditions with classes not supported
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
        self._property_value = None
        self.__value = None
        if len(initial_data) == 1 and (type(initial_data[0]) == type(str()) or (inspect.isclass(initial_data[0]) and issubclass(initial_data[0], Object))):
            self._singleton = True
            classtype = initial_data[0]
            if type(initial_data[0])==type(str()):
                if classtype == "Object": raise ValueError("Object can not be used directly")
                self._value = classtype
            else:
                if classtype == Object: raise ValueError("Object can not be used directly")
                self._value = initial_data[0]
            return
        else:
            self._singleton = False
        # WARNING: the below is unused as we only support singleton, and code is never checked
        assert len(initial_data) == 0 and len(kwargs) == 0, "Only singleton properties are supported"
        for dictionary in initial_data:
            if type(dictionary) != type(dict()): continue
            for key in dictionary:
                setattr(self, key, dictionary[key])
            self._order.append(key)
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    @property
    def _value(self):
        if type(self.__value) == type(str()):
            global _poodle_object_classes 
            if not self.__value in _poodle_object_classes:
                raise AssertionError("Dereferencing Object '%s' failed: undefined class %s" % (self.__value, self.__value))
            assert issubclass(_poodle_object_classes[self.__value], Object)
            self.__value = _poodle_object_classes[self.__value]
        return self.__value
    
    @_value.setter
    def _value(self, v):
        self.__value = v
    
    def __set_name__(self, owner, name):
        if not hasattr(self, "_property_name"):
            self._property_name = name
    
    def __get__(self, instance, owner):
        # if hasattr(self, "_property_of_inst") and self._property_of_inst and self._property_of_inst._sealed:
        # this does not work and is not needed:::: -->
        if hasattr(self, "_dot_from") and isinstance(self._dot_from, Property):
            raise NotImplementedError("Dot-dot dereferencing is not implemeted, please do dereferencing manually")
        # print("BLA",instance, owner)
        # if hasattr(self, "_property_of_inst"):
            # print("BLABLABLA")
            # return self._value
        return self

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
        "finds the variable that holds the class or our value"
        myclass_genvar = None
        for ph in reversed(self._property_of_inst._parse_history_self):
            myclass_genvar = ph["prop_variables"].get(self._property_name)
            if myclass_genvar: break
        return myclass_genvar
    
    
    def find_class_variable(self):
        "finds the variable that holds the class that we are property of"
        my_class_name = self.get_property_class_name()
        myclass_genvar = None
        if self._property_of_inst._class_variable: return self._property_of_inst._class_variable
        raise AssertionError("ProgrammingError: Class has no variable defined; refusing to continue")
        # for ph in reversed(self._property_of_inst._parse_history):
        #     if my_class_name in ph["variables"]:
        #         myclass_genvar = ph["variables"][my_class_name]
        #         break
        # return myclass_genvar
    
    def operator(self, other, operator="equals", dir_hint="straight"):
        assert operator == "equals" or operator == "contains"
        global _compilation
        global _collected_predicates
        global _collected_parameters
        global _collected_predicate_templates
        global _problem_compilation
        global _collected_effects
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
                obj = other._property_of() 
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
        # if _parse_history:
        #     if not other_genvar:
        #         for ph in reversed(_parse_history):
        #             if other_class_name in ph["variables"] and who_instantiating != "other": # only generate new var if we are instantiating it here
        #                 other_genvar = ph["variables"][other_class_name]
        #                 log.debug("WARNING! Variable found in history - resulted PDDL may be wrong")
        #                 break
        #     for ph in reversed(_parse_history):
        #         if has_poi and self._property_of_inst._class_variable:
        #             myclass_genvar = self._property_of_inst._class_variable
        #         else:
        #             if my_class_name in ph["variables"] and who_instantiating != "self":
        #                 myclass_genvar = ph["variables"][my_class_name]
        #                 log.debug("WARNING! myclass Variable found in history - resulted PDDL may be wrong")
        #                 break
                    
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
        other_property_class_name = None
        other_property_genvar = None
        if property_property_comparison:
            other_property_class_name = get_property_class_name(other)
            other_property_class = other.get_parent_class()
            if hasattr(other, "_property_of_inst") and other._property_of_inst: other_property_genvar = other._property_of_inst._class_variable
            # if not other_property_genvar and _parse_history: # must not fire?
            #     for ph in reversed(_parse_history):
            #         if other_property_class_name in ph["variables"] and who_instantiating != "other": # only generate new var if we are instantiating it here
            #             other_property_genvar = ph["variables"][other_property_class_name]
            #             break
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

        if isinstance(other, Property):
            otherPropName = other._property_name
        else:
            otherPropName = None
        ph_entry = {
                "operator": operator, 
                "self-propname": self._property_name,
                "other-propname": otherPropName,
                "self": self,
                "other": other,
                "otherClass": subjObjectClass, 
                "self-prop": self._value, 
                #"variables": { other_class_name: other_genvar , my_class_name: myclass_genvar }, # TODO: what if we have two same classes?
                "variables": {my_class_name: myclass_genvar, other_class_name: other_genvar }, # TODO: what if we have two same classes?
                # "prop_variables": {self._property_name: 
                "class_variables": { my_class_name: myclass_genvar },
                "text_predicates": [text_predicate, text_predicate_2],
                "parameters": collected_parameters,
                "frame": get_source_frame_dict()
                # "frame": {
                #     "code": c_string,
                #     "line": frameinfo.lineno,
                #     "file": frameinfo.filename
                # }
            }
        if not other_property_class_name is None and not other_property_genvar is None:
            ph_entry["variables"][other_property_class_name] = other_property_genvar
        if not _problem_compilation: # prevents leak of goal into predicates...
            obj._parse_history.append(ph_entry)
        # add self parse history for optimization
        # 1 in case of Class.prop == inst: <how to identify>:
        #       - we know variable of obj property "prop" and its name is other._class_variable
        if has_po and not has_poi and isinstance(other, Object):
            obj._parse_history_self.append({"prop_variables": {self._property_name: other._class_variable}})
        # 2 in case of inst.prop == Class: <how?>
        #       - we know variable of prop of self._property_of_inst and self._property_name is obj._class_variable
        elif has_poi and inspect.isclass(other) and issubclass(other, Object):
            self._property_of_inst._parse_history_self.append({"prop_variables": {self._property_name: obj._class_variable}})
        # 3 in case of Class.prop == inst.prop <> REVERSED! for _contains_
        #       - we know variable of prop self._property_name on self._property_of() (obj) and its name is generated other_property_genvar
        #       - we know variable of prop other._property_name on other._property_of_inst and its name is also other_property_genvar
        elif has_po and not has_poi and isinstance(other, Property):
            obj._parse_history_self.append({"prop_variables": {self._property_name: other_genvar}})
            other._property_of_inst._parse_history_self.append({"prop_variables": {other._property_name: other_genvar}})
        # 4 in case of inst.prop == Class.prop <> REVERSED! for _contains_
        #       - we know variable of prop self._property_name on self._property_of_inst and its name is generated other_property_genvar
        #       - we know variable of prop other._property_name of other._property_of() (obj) and its name is also other_property_genvar
        elif has_poi and isinstance(other, Property) and not hasattr(other, "_property_of_inst"):
            self._property_of_inst._parse_history_self.append({"prop_variables": {self._property_name: other_genvar}})
            obj._parse_history_self.append({"prop_variables": {other._property_name: other_genvar}})
        # 5 in case of inst.prop == inst2
        #       - we know variable of self._property_name on self._property_of_inst and it is other._class_variable
        elif has_poi and isinstance(other, Object):
            self._property_of_inst._parse_history_self.append({"prop_variables": {self._property_name: other._class_variable}})
        # 6 in case of inst.prop == inst2.prop
        #       - we know variable of self._property_name on self._property_of_inst and it is generated other_property_genvar
        #       - we know variable of other._property_name on other._property_of_inst and its name is other_property_genvar
        elif has_poi and isinstance(other, Property) and hasattr(other, "_property_of_inst"):
            self._property_of_inst._parse_history_self.append({"prop_variables": {self._property_name: other_genvar}})
            other._property_of_inst._parse_history_self.append({"prop_variables": {other._property_name: other_genvar}})
        else:
            raise AssertionError("Not supported.")
            
        # 7 in case of inst1 == inst2
        #       - in this case no variables are created
        # add set initial
        #print("OPERATOR-HIST-2", _parse_history)

        # this is required for the variables to become available at selector compilation
        # if has_poi and _compilation and not hasattr(self._property_of_inst, "_parse_history"): self._property_of_inst._parse_history = _parse_history
        if has_poi and not hasattr(self._property_of_inst, "_parse_history"): self._property_of_inst._parse_history = _parse_history
        if has_poi and hasattr(self._property_of_inst, "_parse_history"): self._property_of_inst._parse_history += _parse_history
        
        if _problem_compilation:
            _collected_effects += [text_predicate, text_predicate_2]
        elif _compilation:
            # because in compilation mode our _parse_history now contains merged history ->>>
            for ph in obj._parse_history + _parse_history: # WARNING! why do we need to add ph here??
                _collected_predicates += ph["text_predicates"]
                _collected_parameters.update(ph["parameters"])
        _collected_predicates += [text_predicate, text_predicate_2] # this is required for Unselect() to work as it depends on order of output
        return obj
        
    def equals(self, other):
        return self.operator(other, "equals")

    def __eq__(self, other):
        if hasattr(self, "_property_of_inst") and isinstance(other, Property) and not hasattr(other, "_property_of_inst"):
            log.warning("!!!!!! ALT BEH 1 - me is {0} {1} other is {2} ".format(self, self._property_of_inst, other))
            push_selector_object(other.equals(self))
        else:
            push_selector_object(self.equals(other))
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
        
    def init_unsafe_internal(self, value):
        self._unset = True
        return self.set(value)
        
    def set(self, value):
        global _problem_compilation
        global _effect_compilation 
        init_mode = False
        if not self._unset and not _problem_compilation and not self._property_of_inst._new_fresh: 
            try:
                self.unset_internal(_force=True)
            except AssertionError:
                # assume init mode
                init_mode = True
        assert type(value) == self._value, "Type mismatch: setting %s to %s.%s expecting %s" % (value, self._property_of_inst.__class__.__name__, self._property_name, self._value)
        if not isinstance(self, Relation): self._property_value = value # protect from re-setting value as Relation did same above...
        if _problem_compilation:
            global _collected_facts
            text_predicate = gen_text_predicate_push_globals(self.gen_predicate_name(), "", self._property_of_inst.name, self._property_of_inst.__class__.__name__, value.name, value.__class__.__name__)
            if not isinstance(value, Imaginary) and not isinstance(self, Relation): 
                text_predicate_none = gen_text_predicate_push_globals(self.gen_predicate_name(), "", self._property_of_inst.name, self._property_of_inst.__class__.__name__, _none_objects[value.__class__.__name__].name, value.__class__.__name__)
                text_predicate_beg_match = ' '.join(text_predicate_none.split()[:2])
                rmlist = []
                for fct in _collected_facts:
                    if fct.startswith(text_predicate_beg_match):
                        rmlist.append(fct)
                for fct in rmlist:
                    _collected_facts.remove(fct)
                # while text_predicate_none in _collected_facts: _collected_facts.remove(text_predicate_none)
            _collected_facts.append(text_predicate)
            # _collected_facts.append("("+self.gen_predicate_name()+" "+self._property_of_inst.name + " " + value.name+ ")")
            return
        self._prepare(value)
        global _collected_effects
        text_predicate = gen_text_predicate_push_globals(self.gen_predicate_name(), "", self.find_class_variable(), self._property_of_inst.__class__.__name__, value.class_variable(), value.__class__.__name__)
        # _collected_effects.append("("+self.gen_predicate_name()+" "+self.find_class_variable()+" "+value.class_variable()+")")
        _collected_effects.append(text_predicate)
        _collected_parameters.update({
            self.find_class_variable(): self._property_of_inst.__class__.__name__,
            value.class_variable(): value.__class__.__name__
        })
        if init_mode:
            # if issubclass(type(value), Imaginary):
            #     raise NotImplementedError("For Imaginary objects that were not Select()'ed, please unset() first, or use `.init_unsafe()`")
            log.warning("PREDICATE in INIT mode: %s %s" % (repr(self._property_of_inst), repr(self)))
            if issubclass(self._value, Imaginary):
                other_genvar = gen_var_imaginary(value.__class__.__name__)
                text_predicate = gen_text_predicate_push_globals(self.gen_predicate_name(), "", self.find_class_variable(), self._property_of_inst.__class__.__name__, other_genvar, value.__class__.__name__)
                text_predicate_effect = "(not %s)" % gen_text_predicate_push_globals(self.gen_predicate_name(), "", self.find_class_variable(), self._property_of_inst.__class__.__name__, other_genvar, value.__class__.__name__)
            else:
                other_genvar = gen_var(value.__class__.__name__)
                text_predicate = gen_text_predicate_push_globals(self.gen_predicate_name(), "", self.find_class_variable(), self._property_of_inst.__class__.__name__, other_genvar, value.__class__.__name__)
                text_predicate_effect = "(not %s)" % gen_text_predicate_push_globals(self.gen_predicate_name(), "", self.find_class_variable(), self._property_of_inst.__class__.__name__, other_genvar, value.__class__.__name__)
            _collected_predicates.append(text_predicate)
            _collected_effects.append(text_predicate_effect)
            _collected_parameters.update({other_genvar: value.__class__.__name__})
        self._unset = False
        
    def unset_internal(self, what = None, _force = False):
        # we need to unset the value that we selected for us
        self._prepare()
        global _collected_effects
        if what is None: 
            log.warning("WARNING! Using experimental support for what=None")
            my_parameter_var = self.find_parameter_variable()
            if my_parameter_var is None:
                raise AssertionError("Variable for %s was not previously selected, nothing to unset. Please select or specify explicitly." % (self._property_name))
            text_predicate = gen_text_predicate_push_globals(self.gen_predicate_name(), "", self.find_class_variable(), self._property_of_inst.__class__.__name__, my_parameter_var, self._value.__name__)
            # _collected_effects.append("(not ("+self.gen_predicate_name()+" "+self.find_class_variable()+" "+self.find_parameter_variable()+"))")
            _collected_effects.append("(not %s)" % text_predicate)
        else:
            text_predicate = gen_text_predicate_push_globals(self.gen_predicate_name(), "", self.find_class_variable(), self._property_of_inst.__class__.__name__, what._class_variable, what.__class__.__name__)
            # _collected_effects.append("(not ("+self.gen_predicate_name()+" "+self.find_class_variable()+" "+what._class_variable+"))")
            _collected_effects.append("(not %s)" % text_predicate)
        self._unset = True
        
    def value(self):
        return self._property_value
   
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
        
        # The above renders this obolete: (check!)
        if "_" == attr[0] or attr in [ "_property_of_inst", "_value", "_property_name" ]:
            # return super().__getattr__(self, attr)
            return super().__getattribute__(attr)
        if hasattr(self, "_property_of_inst") and not me_has_attr:
            try:
                super().__getattribute__("_value")
                me_has_value = True
            except AttributeError:
                pass
            if me_has_value:
                if hasattr(self._value, attr):
                    if hasattr(self, "_dot_from") and isinstance(self._dot_from, Object):
                        raise NotImplementedError("Dot-dot dereferencing is not implemeted, please do dereferencing manually")
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
            raise AttributeError('%s object has no attribute %s' % (self.__value, attr))
        

class ProtectedProperty(Property):
    def _check(self):
        global _problem_compilation
        global _compilation
        assert _problem_compilation, "Property %s is protected!" % self
        assert not _compilation, "Property %s is protected!" % self
    def set(self, what):
        self._check()
        super().set(what)
    def unset_internal(self, what):
        self._check()
        super().unset_internal(what)

class ListLike(list): # Important not to cause any comparisons during compilation
    def add(self, value):
        self.append(value)
    
class Relation(Property):
    "a property that can have multiple values"
    # https://stackoverflow.com/a/932580
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        self._property_value = ListLike()
    def contains(self, other):
        return self.operator(other, "contains")
        
    def __floordiv__(self, other):
        return self.contains(other)
        
    def set(self, what):
        raise NotImplementedError("Usage error: Relation can not be set to one value. Use .add() instead")
        
    # def unset(self, what=None, _force=False):
    #     if _force: return super().unset(what)
    #     raise NotImplementedError("Usage error: Relation can not be unset. Use .remove() instead")
    
    def add(self, what):
        if isinstance(what, Object): self._property_value.append(what)
        self._unset = True
        super().set(what)
        
    def remove(self, what):
        if isinstance(what, Object) and what in self._property_value: self._property_value.remove(what)
        super().unset_internal(what)

    def __contains__(self, what):
        push_selector_object(self.contains(what))
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

class StateFact(Property): # TODO HERE Rename to Bool()
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
        self._value = True
    def unset(self):
        self._prepare()
        global _collected_effects
        # TODO: do we need to generate this??
        text_predicate = gen_one_predicate(self.gen_predicate_name(), self.find_class_variable(), self._property_of_inst.__class__.__name__)
        # _collected_effects.append("(not ("+self.gen_predicate_name()+" "+self.find_class_variable()+"))")
        _collected_effects.append("(not %s)" % text_predicate)
        self._value = False

    def __eq__(self, other):
        push_selector_object(self.equals(other))
        return True

    def equals(self, other):
        "StateFact can only be compared to True or False"
        assert other == True or other == False, "Only True or False for StateFact"
        global _collected_effects
        global _collected_predicates 
        global _collected_parameters
        if other == False:
            # TODO: could call self.unset() if run in effect compilation, not problem compilation!!
            # (add below...)
            raise NotImplementedError("Comparing StateFact to False is not supported")
        global _problem_compilation
        if _problem_compilation:
            text_predicate = gen_one_predicate(self.gen_predicate_name(), self._property_of_inst.name, self._property_of_inst.__class__.__name__)
            # _collected_effects.append("("+self.gen_predicate_name()+" "+self._property_of_inst.name+")")
            # _collected_predicates.append(text_predicate)
            _collected_effects.append(text_predicate) # in problem compilation, we collect effects...
        else:
            self._prepare() # not sure if this is needed here???
            # text_predicate = "("+self.gen_predicate_name()+" "+self.find_class_variable()+")"
            text_predicate = gen_one_predicate(self.gen_predicate_name(), self.find_class_variable(), self._property_of_inst.__class__.__name__)
            _collected_parameters.update({self.find_class_variable(): self._property_of_inst.__class__.__name__})
            _collected_predicates.append(text_predicate)
            _collected_predicates.append(None) # WARNING! last None has secret meaning for Unselect checks
        
        ph = {
                "operator": "check_bool", 
                "self": self, 
                "self-propname": self._property_name, 
                "other": None, 
                "other-propname": None, 
                "otherClass": None,
                "self-prop": self._value, 
                #"variables": { other_class_name: other_genvar , my_class_name: myclass_genvar }, # TODO: what if we have two same classes?
                "variables": {}, # TODO: what if we have two same classes?
                "class_variables": { },
                "text_predicates": [ text_predicate, None ], # WARNING! last None has secret meaning for Unselect checks
                "parameters": {self.find_class_variable(): self._property_of_inst.__class__.__name__},
                "frame": get_source_frame_dict()
            }
        if hasattr(self, "_property_of_inst") and self._property_of_inst:
            if self._property_of_inst._parse_history:
                self._property_of_inst._parse_history.append(ph)
            else:
                self._property_of_inst._parse_history=[ph]
        else:
            raise AssertionError("Selecting a variable by StateFact is not supported; please use selector() syntax")
        return self._property_of_inst
        #raise NotImplementedError("Equality of StateFact called outside of supported context")


class Bool(Property):
    
    def __init__(self, initialValue):
        if type(initialValue) != type(True): raise ValueError("Bool must be initialized with True of False")
        super().__init__(BooleanObject)
        # self.__init_value = _system_objects["object-%s" % str(initialValue)]
        self._init_value = initialValue
    
    def set(self, value):
        if value == True:
            super().set(_system_objects["object-True"])
        elif value == False:
            super().set(_system_objects["object-False"])
        else:
            raise ValueError("Bool can only be set to True or False but got %s (%s)" % (value, type(value)) )
            
    
    def __eq__(self, value):
        if value == True:
            return super().__eq__(_system_objects["object-True"])
        elif value == False:
            return super().__eq__(_system_objects["object-False"])
        else:
            raise ValueError("Bool can only be compared to True or False")
    
    def __bool__(self):
        return self == True

class ActionMeta(type):
    # def __new__(mcls, name, bases, attrs):
    #     # attempt to make in-action counter
    #     # complicated by having compilation after class gen
    #     # meaning that compilation must cause counter to restart
    #     #global id_counter
    #     #id_counter = 0
    #     cls = super(ActionMeta, mcls).__new__(mcls, name, bases, attrs)
    #     #for attr, obj in attrs.items():
    #     #    if isinstance(obj, Property):
    #     #        obj.__set_name__(cls, attr)
    #     return cls
    def __init__(cls, name, bases, dct):
        super(ActionMeta, cls).__init__(name, bases, dct)
        cls._class_collected_predicates = []
        cls._class_collected_parameters = {}
        for ob in dct:
            if isinstance(dct[ob], Object):
                for ph in dct[ob]._parse_history:
                    cls._class_collected_predicates += list(filter(None, ph["text_predicates"]))
                    cls._class_collected_parameters.update(ph["parameters"])

class BaseObjectMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = super(BaseObjectMeta, mcls).__new__(mcls, name, bases, attrs)
        global _poodle_object_classes 
        _poodle_object_classes[name] = cls 
        for attr, obj in attrs.items():
            if isinstance(obj, Property):
                obj.__set_name__(cls, attr)
        return cls
        
    def __init__(cls, name, bases, dct):
        super(BaseObjectMeta, cls).__init__(name, bases, dct)
        global _none_objects
        if name == "Imaginary":
            _none_objects[name] = cls()
            _none_objects[name].name = "p-null-%s" % name
            _none_objects[name]._class_variable = gen_var(name, prefix="null-")
            
        if not name in ["Object", "Imaginary"]:
            _none_objects[name] = cls()
            if not issubclass(cls, Imaginary):
                _none_objects[name].name = "p-null-%s" % name
                _none_objects[name]._class_variable = gen_var(name, prefix="null-")
            else:
                _none_objects[name].name = ' '.join(["p-null-Imaginary"] * HASHNUM_DEPTH_DEFAULT) # HASHNUM_DEPTH_DEFAULT fix! 
                _none_objects[name]._class_variable = gen_var_imaginary(name, prefix="null-")
        
            
    def __getattribute__(self, what):
        # print("WHAT IS", what)
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
    def __init__(self, value=None, _force_name=None): # WARNING! name is too dangerous to put here!
        self._parse_history = [] # Experimentally setting to fix #78
        self._parse_history_self = [] # Self, non-merged parse history
        self._sealed = False
        self._new_fresh = False # will only become fresh and new if it is imaginary in effect compilation
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
                frameinfo = getframeinfo(inspect.currentframe().f_back)
                name = "%s-%s-%s-L%s" % (self.__class__.__name__, str(new_id()), os.path.basename(frameinfo.filename), frameinfo.lineno)
            self.name = self.gen_name(name) # object name when instantiating..
        if not _force_name is None:
            self.name = _force_name
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
        # TODO HERE: in effect, do the same if we are imaginary!
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
                if not self.__imaginary__ and _problem_compilation and \
                        not getattr(self,key)._value is None and \
                        not isinstance(getattr(self, key), Relation) and \
                        not value == "POODLE-NULL":
                    if hasattr(getattr(self,key), "_init_value"):
                        null_object = getattr(self,key)._init_value
                    else: 
                        # getattr(self,key).init_unsafe(_none_objects[getattr(self,key)._value.__name__])
                        null_object = getattr(self,key)._value("POODLE-NULL", _force_name="p-nullobj-%s-%s" % (self.name, key))
                    getattr(self,key).init_unsafe_internal(null_object)
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
        elif isinstance(other, Object) and (_compilation or _problem_compilation or _effect_compilation):
            assert self._class_variable and other._class_variable, "Expected fully initialized objects"
            global _collected_predicates
            global _collected_parameters
            _collected_predicates.append("(= %s %s)" % (self._class_variable, other._class_variable))
            _collected_parameters.update({self._class_variable: self.__class__.__name__, other._class_variable: other.__class__.__name__}) # TODO: could be done easier if we added them on init...
            # raise NotImplementedError("Object-Object selector is not supported")
            push_selector_object(self)
            return self
        elif type(other) == type(True):
            return True # WARNING! stub for asserts! TODO FIX
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
        elif (_effect_compilation or _problem_compilation) and isinstance(value, bool) and hasattr(self, name) and isinstance(getattr(self, name), Property):
            if isinstance(getattr(self, name), Bool):
                getattr(self, name).set(value)
            else:
                if value == True:
                    getattr(self, name).set()
                elif value == False:
                    getattr(self, name).unset()
                else:
                    raise AssertionError("Something is wrong")
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
    #     print("GA-", self, attr)
    #     return super().__getattribute__(attr)

    def __getattribute__(self, attr):
        if attr.startswith("_"): return super().__getattribute__(attr)
        # this does not work and is not needed:::: -->
        if hasattr(self, "_dot_from") and isinstance(self._dot_from, Property):
            raise NotImplementedError("Dot-dot dereferencing is not implemeted, please do dereferencing manually")
        # print(self,":",attr)
        v = super().__getattribute__(attr)
        # print(self,":",attr,":",v)
        if self._sealed and isinstance(v, Property):
            return v._property_value
        if isinstance(v, Property): 
            v._dot_from = self
        return v
    
    def __str__(self):
        try:
            return repr(self)+"(name=%s, value=%s)" % (self.name, self.value)
        except:
            return repr(self)+"(Additionally, there was an error during standard __str__)"
            
    def __hash__(self):
        return hash(self.name)

    
    # def __getattr__(self, attr):
    #     if attr == "_type_of_property": return super().__getattr__(self, attr)
    #     if hasattr(self, "_type_of_property"):
    #         print("has top", attr)
    #     return super().__getattr__(self, attr)


class Imaginary(Object):
    
    def gen_name(self, name):
        global _problem_compilation
        if _problem_compilation:
            hns = gen_hashnums(HASHNUM_DEPTH_DEFAULT)
            return ' '.join([v.name for v in hns])
        else:
            return super().gen_name(name)
    
    def __init__(self, value=None, _force_name=None):
        self.__imaginary__ = True
        super().__init__(value, _force_name)
        self._class_variable = gen_var_imaginary(self.__class__.__name__, prefix="im-default-")
        global _effect_compilation
        global _collected_predicates
        global _collected_effects
        global _collected_parameters
        if _effect_compilation:
            self._new_fresh = True
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

# A static object initializes itself with instances static_values
class StaticObject(Object):
    # TODO
    pass

class Digit(Object):
    pass

class PoodleHashnum(Object):
    "hashnum is used in imaginary object identification"
    pass # unsorted, unopimized

class BooleanObject(Object):
    pass

_problem_compilation = True
_system_objects["object-True"] = BooleanObject("TRUE")
_system_objects["object-False"] = BooleanObject("FALSE")
_collected_object_classes.add("BooleanObject") # TODO THIS DOES NOT WORK FIXME
_problem_compilation = False

#########################################################################
##
##  Domain Definition
##


class PlannedAction(metaclass=ActionMeta):
# class PlannedAction():
    cost = 1
    argumentList = []
    parameterList = []
    problem = None
    template = None
    _clips_rhs = []
    _clips_lhs = []
    collected_parameters = {}

    def __init__(self, **kwargs):
        self._planned_objects_dict = kwargs
        for k,v in kwargs.items():
            if isinstance(v, Object):
                v._sealed = True
            setattr(self, k, v)
            
    
    def __str__(self):
        return self.render(self._planned_objects_dict)
        
    def __repr__(self):
        return self._default_render(self._planned_objects_dict)
        
    def render(self, obj_dict):
        return self._default_render(obj_dict)
        
    def _default_render(self, obj_dict):
        return self.__class__.__name__+": "+", ".join('%s=%s' % (n, obj_dict.get(n)) for n in dir(self) if isinstance(getattr(self,n), Object))
        # return ", ".join(repr(getattr(self,n)) for n in dir(self))
        # return repr(dir(self))
        # return ', '.join("%s: %s" % item for item in attrs.items() if isinstance(item[1], Property))
        # return ', '.join("%s: %s" % item for item in attrs.items() )
        
        # ret = "{0}".format(self.__class__.__name__)
        # for arg in self.argumentList:
        #     ret +=" {0}({1})".format(arg.name, arg.value)
        # return ret

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
        sel_ret = cls.selector(cls)
        cls.selector_objects = []
        if sel_ret != "DEFAULT": 
            assert type(sel_ret) != type(True) and not sel_ret is None, "selector() does not return supported value in %s (value was %s)" % (repr(cls), repr(sel_ret))
            if type(sel_ret) == type([]):
                cls.selector_objects = sel_ret
            else:
                cls.selector_objects = [sel_ret]
        _effect_compilation = True
        log.info("{0}".format(cls.effect(cls)))
        _effect_compilation = False
        _compilation = False
        
        # _collected_predicates = filter(None, list(set(_collected_predicates)))
        _collected_predicates = list(filter(None, list(OrderedDict.fromkeys(cls._class_collected_predicates + _collected_predicates))))
        for k in _replaced_predicates:
            if not k in _collected_predicates: continue
            _collected_predicates.remove(k)
            _collected_predicates.append(_replaced_predicates[k])
        collected_parameters = ""
        assert len(_collected_effects) > 0, "Action %s has no effect" % cls.__name__
        assert len(_collected_predicates) > 0, "Action %s has nothing to select" % cls.__name__
        cls.collected_parameters = {}
        cls.collected_parameters.update(_collected_parameters)
        cls.collected_parameters.update(cls._class_collected_parameters)
        cls.collected_predicates = _collected_predicates
        cls.collected_effects = _collected_effects
        for ob in cls.collected_parameters:
            if not "?" in ob: continue # hack fix for object name leak into params
            if " " in ob:
                # WARNING! this is because of how imaginary variables are implemented
                # collected_parameters += "%s - %s " % (ob.split()[0], _collected_parameters[ob])
                # collected_parameters += "%s - %s " % (ob.split()[1], _collected_parameters[ob])
                collected_parameters += "%s - %s " % (ob.split()[0], HASHNUM_CLASS_NAME)
                collected_parameters += "%s - %s " % (ob.split()[1], HASHNUM_CLASS_NAME)
            else:
                collected_parameters += "%s - %s " % (ob, cls.collected_parameters[ob])
        
        assert len(collected_parameters) > 0
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
    
    @classmethod
    def get_clips_lhs_rhs(cls, problem):
        if cls._clips_rhs:
            return cls._clips_lhs, cls._clips_rhs
        cls.compile(problem)
        lhs = copy.copy(cls.collected_predicates)
        rhs = []
        lhs = [ "(test %s)" % r.replace("=", "eq") if r.startswith("(=") else r for r in lhs ]
        for p in cls.collected_effects:
            if p.startswith("(not"):
                fname = "?f"+str(new_id())
                retracting_predicate = p.replace("(not","")[:-1].strip()
                assert retracting_predicate in lhs, "ProgrammingError: retracting predicate %s not found in precondition of %s" % (p, repr(cls)) 
                lhs = [ fname+" <- "+r if r == retracting_predicate else r for r in lhs ]
                cl = "(retract %s)" % fname
            else:
                cl = "(assert {ce})".format(ce=p)
            rhs.append(cl)
        cls._clips_lhs = lhs
        cls._clips_rhs = rhs
        return lhs, rhs
    
    @classmethod
    def compile_clips(cls, problem):
        lhs, rhs = cls.get_clips_lhs_rhs(problem)
        return """
    (defrule {name}
        {lhs}
        =>
        {rhs}
    )
        """.format(name=cls.__name__,lhs='\n        '.join(lhs),
                    rhs='\n        '.join(rhs))
    
    def selector(self):
        return "DEFAULT"
        # raise NotImplementedError
        
    def effect(self):
        raise NotImplementedError("effect() in %s not implemented" % repr(self))
    
    def __call__(self):
        return getattr(self.problem, self.methodName)(**self.kwargs)
    

class PlannedActionJinja2(PlannedAction):
    template = "./template/default.j2"

    # def __str__(self, template=None):
    #     fileIn = ""
    #     with open(self.template, "r") as fd:
    #         fileIn = fd.read()
    #     template = Template(fileIn)
    #     param = []
    #     for arg in self.argumentList:
    #         args = []
    #         args.append(arg.name)
    #         args.append(arg.value)
    #         param.append(args)
    #     return template.render(action=self.__class__.__name__, parameters=param)

    # def getTemplate(self):
    #     if self.template == None:
    #         return "./template/{0}.j2".format(self.__class__.__name__)
    #     return selt.template

# problem definition
class Problem:
    HASHNUM_COUNT = HASHNUM_COUNT_DEFAULT # amount of hashnums generated for imaginary object
    HASHNUM_DEPTH = HASHNUM_DEPTH_DEFAULT # only 2 is currently supported, waring! set globally only!
    folder_name = None
    objectList = []
    def __init__(self):
        self._has_imaginary = False
        self._plan = None
        self._compiled_problem = ""
    def getFolderName(self):
        return self.folder_name
    
    def addObject(self, obj):
        self.objectList.append(obj)
        return obj
    
    def getObjectList(self):
        return self.objectList

    def actions(self):
        return []
        # raise NotImplementedError("Please implement .actions() method to return list of planned action classes")

    def getActionByName(self):
        strList = []
        for action in self.action():
            strList.append(action.__class__.__name__)
        return strList

    def goal(self):
        raise NotImplementedError("Please implement .goal() method to return goal in XXX format") 

    def wait_result(self, url, task_id):
        url_solve = url.strip('/') + '/solve'
        url_check = url.strip('/') + '/check'
        url_result = url.strip('/') + '/result'
        url_kill = url.strip('/') + '/kill'
        proccessing_time_start = 0
        while 1:
            time.sleep(SOLVER_CHECK_TIME)    
            response = requests.post(url_check, data={'id': crypt(SOLVER_KEY, str(task_id))})   
            status = crypt(SOLVER_KEY, response.content.decode("utf-8"))
            print(status)
            if status == SOLVER_PROCESSING_STATUS :
                print(time.time() - proccessing_time_start )
                if proccessing_time_start == 0 :
                    proccessing_time_start = time.time()
                    continue
                elif  time.time() - proccessing_time_start > SOLVER_MAX_TIME :
                    print (str(SOLVER_MAX_TIME) + ' sec break')
                    response = requests.post(url_kill, data={'id': crypt(SOLVER_KEY, str(task_id))})   
                    status = crypt(SOLVER_KEY, response.content.decode("utf-8"))
                    return 1
                continue
            elif status ==  SOLVER_UNKNOWN_STATUS:
                print ('UNKNOWN SOLVER_ID')
                return 1
            elif status ==  SOLVER_DONE_STATUS:
                response = requests.post(url_result, data={'id': crypt(SOLVER_KEY, str(task_id))})   
                response_plan = crypt(SOLVER_KEY, response.content.decode("utf-8"))  
                
                actionClassLoader = ActionClassLoader(self.actions() + [getattr(self, k).plan_class for k in dir(self) if hasattr(getattr(self, k), "plan_class")], self)
                actionClassLoader.loadFromStr(response_plan)
                self._plan = actionClassLoader._plan
                for ob in self.objectList: ob._sealed = True
                return 0        
            elif status ==  SOLVER_KILLED_STATUS: 
                print ('SOLVER_KILLED_STATUS')
                return 1
            elif status ==  SOLVER_ERROR_STATUS: 
                print ('SOLVER_ERROR_STATUS')
                response = requests.post(url_kill, data={'id': crypt(SOLVER_KEY, str(task_id))})   
                plan = crypt(SOLVER_KEY, response.content.decode("utf-8"))  
                return 1    
            else:
                print ('UNKNOWN_STATUS')
                return 1
        

    def run_cloud(self, url):
        
        url_solve = url.strip('/') + '/solve'
        
         
        SOLVER_KEY = "list(filter(None, _collected_predicates + _collected_effects))"
         
        problem_pddl_base64 = crypt(SOLVER_KEY, str(self.compile_problem())) #base64.b64encode(bytes(self.compile_problem(), 'utf-8'))    
        domain_pddl_base64 =  crypt(SOLVER_KEY, str(self.compile_domain()))#base64.b64encode(bytes(self.compile_domain(), 'utf-8'))      

        data_pddl = {'d': domain_pddl_base64, 'p': problem_pddl_base64, 'n': crypt(SOLVER_KEY, self.__class__.__name__) }
        
        response = requests.post(url_solve, data=data_pddl)   
        task_id = crypt(SOLVER_KEY, response.content.decode("utf-8"))
        
        print(task_id)
 
        return self.wait_result(url, task_id)
        #actionClassLoader = ActionClassLoader(self.actions(), self)


    def run_local(self):
        for ob in self.objectList: ob._sealed = False # seal all objects
        global _collected_parameters
        # print(_collected_parameters)
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
        log.debug("run line is {0}".format(runscript))
        std = subprocess.Popen(runscript, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True).stdout
        retcode = "-1"
        for line in std:
            if line.find('search exit code:') != -1:
                retcode = line.rstrip("\n").split()[3]
            log.info(line.rstrip("\n"))
        if retcode == "0" :
            if self.getFolderName() != None:
                actionClassLoader = ActionClassLoader(self.actions() + [getattr(self, k).plan_class for k in dir(self) if hasattr(getattr(self, k), "plan_class")], self)
                actionClassLoader.loadFromFile("{0}/out.plan".format(self.getFolderName()))
                self._plan = actionClassLoader._plan
        for ob in self.objectList: ob._sealed = True # seal all objects
        return retcode
        
    def run(self, url = SOLVER_URL):
        if os.environ.get("POODLE_LOCAL_PLANNER"):
            return self.run_local()
        return self.run_cloud(url) 
        
    @property
    def plan(self):
        return self._plan

        
    def compile_actions(self):
        # TODO: collect all predicates while generating
        self.actions_text = ""
        for act in self.actions() + [getattr(self, k).plan_class for k in dir(self) if hasattr(getattr(self, k), "plan_class")]:
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
        return ' '.join(list(filter(None, list(_collected_object_classes))))

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
        if self._compiled_problem: return self._compiled_problem
        global _problem_compilation
        global _compilation
        global _collected_objects
        global _collected_object_classes
        global _collected_facts
        global _collected_effects
        global _collected_predicates
        _problem_compilation = True
        _collected_object_classes = set()
        _collected_object_classes.add("BooleanObject")
        _collected_objects = {}
        _collected_facts = []
        self.problem()
        if self.has_imaginary(): self.gen_hashnums()
        self.collected_object_classes = _collected_object_classes
        self.collected_objects = _collected_objects
        for k in _none_objects:
            on = _none_objects[k].name.split()[0]
            if not k in self.collected_object_classes: continue
            if on == "p-null-Imaginary": continue
            noClassName = _none_objects[k].__class__.__name__ # we're not using k as class
            if k in self.collected_objects:
                self.collected_objects[noClassName].append(on)
            else:
                self.collected_objects[noClassName] = [ on ]
        for k in _system_objects:
            on = _system_objects[k].name.split()[0]
            noClassName = _system_objects[k].__class__.__name__ # we're not using k as class
            if k in self.collected_objects:
                self.collected_objects[noClassName].append(on)
            else:
                self.collected_objects[noClassName] = [ on ]
        self.collected_objects[HASHNUM_CLASS_NAME].append("p-null-Imaginary")
        self.collected_facts = _collected_facts
        _compilation = True # required to compile the goal
        _collected_effects = []
        _collected_predicates = []
        # print("+++++++++++++++++", _collected_effects, _collected_predicates)
        self.goal()
        # print("+++++++++++++++++", _collected_effects, _collected_predicates)
        global _selector_out
        _selector_out = None # cleaner goal
        self.collected_goal = list(filter(None, list(OrderedDict.fromkeys(_collected_predicates + _collected_effects))))
        assert len(self.collected_goal), "No goal was generated"
        _collected_predicates = []
        _collected_effects = []
        
        _compilation = False
        _problem_compilation = False
        txt_objects = ""
        for cls in self.collected_objects:
            txt_objects += "\n        ".join(list(set(self.collected_objects[cls]))) + " - " + cls + "\n        "
        self._compiled_problem =  """
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
        return self._compiled_problem

    def facts(self):
        self.compile_problem()
        return self.collected_facts
        
    def check_solution(self, attempts=3):
        "run debugging session over the solution"
        step_completed = False
        for tryCount in range(attempts):
            i=0
            work_facts = self.facts()
            for fun_act in self.solution():
                if hasattr(fun_act, "plan_class"):
                    act = fun_act.plan_class
                else:
                    act = fun_act
                step_completed = False
                lhs, rhs = act.get_clips_lhs_rhs(self)
                c = CLIPSExecutor()
                c.load_rule(act.__name__, lhs=lhs, rhs=rhs)
                c.load_facts(work_facts)
                try:
                    # print("Executing", act)
                    c.run() # throws MatchError
                    work_facts = c.get_facts()
                    step_completed = True
                    i+=1
                except MatchError:
                    break
            if step_completed: break
        if not step_completed:
            match_struct = c.check_match(act)
            raise SolutionCheckError(("Checking...\n...  %s\n...  %s:\n" % ('\n...  '.join("%s: ... ok"%t.__name__ for t in self.solution()[:i]), act.__name__)) + match_struct)
            return match_struct
        return work_facts

class CLIPSRule:
    def __init__(self, name, lhs, rhs):
        self.name = name
        self.lhs = copy.copy(lhs)
        self.rhs = copy.copy(rhs)
        
    def compile(self):
        return """
    (defrule {name}
        {lhs}
        =>
        {rhs}
    )
        """.format(name=self.name,lhs='\n        '.join(self.lhs),
                    rhs='\n        '.join(self.rhs))
    
    def __str__(self):
        return self.compile()

class MatchError(Exception):
    pass

class SolutionCheckError(Exception):
    pass

class CLIPSExecutor:
    CLIPS_BINARY = "clips"
    def __init__(self):
        self.rules = []
    
    def load_rule(self, name, lhs, rhs):
        self.rules.append(CLIPSRule(name, lhs, rhs))
        
    def load_facts(self, facts):
        # print("loading facts", facts)
        self.facts = facts

    def render_assert_facts(self):
        return '\n'.join("(assert %s)" % f for f in self.facts)
        
    def gen_run_problem(self, factFileName):
        defrules = str(self.rules[0])
        facts = self.render_assert_facts()
        return """
        {defrules}
        (seed {seed})
        (set-strategy random)
        (watch facts)
        (watch rules)
        (load-facts "{ffn}")
        ;{facts}
        (printout t "--- RUN ---" crlf)
        (run 1)
        (exit)
        """.format(defrules=defrules, facts=facts, seed=str(int(time.time())), ffn=factFileName)
        
    def gen_match_problem(self, factFileName):
        defrules = str(self.rules[0])
        rname = self.rules[0].name
        # facts = self.render_assert_facts()
        return """
        {defrules}
        (load-facts "{ffn}")
        ; (watch facts)
        (printout t "--- RUN ---" crlf)
        (matches {rname})
        (exit)
        """.format(defrules=defrules, rname=rname, ffn=factFileName)
    
    
    def get_facts(self):
        run_result = self.run_result.split("--- RUN ---")[-1]
        # print("RUN RES", run_result)
        new_facts = []
        del_facts = []
        for l in run_result.split("\n"):
            if not "==" in l: continue
            fact = l.split("  ")[-1].strip()
            if "<==" in l:
                # print("DEL fct", l)
                del_facts.append(fact)
            else:
                # print("NEW fct", l)
                new_facts.append(fact)
        # print("NEW facts", new_facts)
        return list(set(self.facts)-set(del_facts))+new_facts
            
    def run_clips_file(self, fn):
        p = subprocess.run([self.CLIPS_BINARY, "-f2", fn], stdout=subprocess.PIPE)
        return p.stdout.decode("utf-8")
        
    def run_get_result(self, prg):
        # open("./CPLTEST.clp","w+").write(prg)
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(prg.encode('utf-8'))
            fp.flush()
            fn = fp.name
            self.run_result = self.run_clips_file(fn)
            fp.close()
        # open("./CPLTEST_RES.clp","w+").write(self.run_result)
            
    def run(self):
        # self.run_get_result(self.gen_run_problem())
        with tempfile.NamedTemporaryFile() as fp:
            fp.write('\n'.join(self.facts).encode("ascii"))
            fp.flush()
            self.run_get_result(self.gen_run_problem(fp.name))
        if len(self.run_result.split("--- RUN ---")[-1]) < 10:
            raise MatchError("Rule %s does not match its selector")
    
    def check_match(self, actClass):
        with tempfile.NamedTemporaryFile() as fp:
            fp.write('\n'.join(self.facts).encode("ascii"))
            fp.flush()
            self.run_get_result(self.gen_match_problem(fp.name))
        assert not "[" in self.run_result, "Error in creating debugger problem: %s" % self.run_result
        m = self.run_result.split("--- RUN ---")[-1]
        all_selected_objects_histories = []
        for n in dir(actClass):
            if not isinstance(getattr(actClass,n), Object): continue
            if getattr(actClass,n)._parse_history:
                all_selected_objects_histories += getattr(actClass,n)._parse_history
        for phl in [ob._parse_history for ob in actClass.selector_objects]:
            all_selected_objects_histories += phl
        indexed_ces = []
        for ce in self.rules[0].lhs:
            found = False
            for ph in all_selected_objects_histories:
                if ce.split("<-")[-1].strip() in ph["text_predicates"]:
                    found = True
                    indexed_ces.append("{code}, {op1}<>{op2} in {file}:{line}".format(op1=ph["self-propname"],op2=ph["other-propname"],code=ph["frame"]["code"],file=os.path.basename(ph["frame"]["file"]),line=ph["frame"]["line"]))
                    break
            if not found:
                indexed_ces.append("unknown "+ce) # 
            # assert found
        allmatch=["     *"]
        acc = []
        other_out = "Partial".join(m.split("Partial")[1:])+"\nPartial"
        first_partial = True
        for l in other_out.split("\n"):
            if "Partial" in l or "Activations" in l:
                if first_partial: 
                    acc = []
                    first_partial = False
                    continue
                if acc and 'None' in acc[0]:
                    allmatch.append("!!   0")
                elif acc:
                    allmatch.append("  "+str(len((','.join(acc)).split(","))).rjust(4))
                    acc = []
                else:
                    allmatch.append("!!   0")
            else:
                acc.append(l)
        ret = []
        col_fs = []
        state_pm = False
        i=0
        for l in m.split("\n"):
            if "Pattern" in l:
                p_idx = int(l.split()[-1])-1
                ret.append("{mm}/{mamt} match(es) {finfo}".format(mm=allmatch[i],mamt=len(col_fs),finfo=repr(indexed_ces[p_idx])))
                if col_fs:
                    # ret.append(','.join(col_fs))
                    col_fs = []
                i+=1
            else:
                if "Partial" in l or state_pm:
                    state_pm = True
                    # ret.append(l)
                else:
                    col_fs.append(l)
        return '\n'.join(ret)
        

class ActionClassLoader:
    
    # put as argument for constructor list of the ActionPlanned type which got from Problem.actions()
    def __init__(self, actionList, problem):
        self.actionList = [] #list of the ActionPlanned type
        self._plan = [] #list instances of the ActionPlanned type
        self.problem = None
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
                    obj_found = None
                    for obj in self.problem.getObjectList():
                        if isinstance(obj, Object):
                            if argStr.lower() == obj.name.lower():
                                obj_found = obj
                    argumentList.append(obj_found)
                parameter_names = []
                for k in action.collected_parameters.keys(): parameter_names+=k.split()
                parameter_names = [ x for x in parameter_names if x.startswith("?") ] # see https://trello.com/c/STwRxQ9e/213-bug-objvariable-contains-both-variables-and-symbol
                pos_args_dict = dict(zip(parameter_names,argumentList))
                action_py_vars_dict = {n:getattr(action,n)._class_variable for n in dir(action) if isinstance(getattr(action,n), Object)}
                action_py_vars_matched_values = {pyvar:pos_args_dict.get(ppar) for pyvar,ppar in action_py_vars_dict.items()}
                plannedAction = action(**action_py_vars_matched_values)
                plannedAction.kwargs = action_py_vars_matched_values
                plannedAction.methodName = action.__name__
                self._plan.append(plannedAction)
                # log.info(plannedAction)

    def loadFromFile(self, outPlanFile):
        log.debug("load action from file {0}".format(outPlanFile))
        with open(outPlanFile, "r") as fd:
            for planLine in fd:
                if ";" in planLine: continue
                self.load(planLine.replace("(", "").replace(")", ""))

    def loadFromStr(self, outPlanStr):
        log.debug("load action from str")
        for planLine in outPlanStr.splitlines():
            if ";" in planLine: continue
            self.load(planLine.replace("(", "").replace(")", ""))

def planned(fun=None, *, cost=None):
    if fun is None:
        return functools.partial(planned, cost=cost)
    cost = cost if cost else 1
    if not getattr(fun, "__annotations__", None): 
        raise ValueError("For planning to work function parameters must be type annotated")
    kwargs = {}
    for k, v in fun.__annotations__.items(): kwargs[k] = v()
    class NewPlannedAction(PlannedAction):
        def effect(self):
            global _effect_compilation
            global _selector_out
            _effect_compilation = False
            _effect_compilation = True
            fun(self.problem, **kwargs)
            _selector_out = None
    for k, v in kwargs.items(): setattr(NewPlannedAction, k, v)
    NewPlannedAction.__name__ = fun.__name__
    NewPlannedAction.cost = cost
    fun.plan_class = NewPlannedAction
    return fun


