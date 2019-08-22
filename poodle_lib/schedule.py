import sys
from poodle import *
import collections.abc
from .poodle_main import ListLike, Select, Problem, _collected_predicates, \
    _collected_effects, _none_objects, _system_objects, _compilation_enable, \
        HASHNUM_CLASS_NAME, _selector_out, _reset_state, _planned_internal

class SchedulingError(Exception):
    pass

class EmptyPlanError(Exception):
    pass

def _space_to_list(sp):
    if isinstance(sp, collections.abc.Mapping):
        r = list(set([o for o in sp.values() if isinstance(o, Object)]))
    else: r = list(set([o for o in sp if isinstance(o, Object)]))
    rec = []
    for o in r:
        rec += _get_recursive_objects(o)
    return list(set(rec))

# TODO: unfinished method
def _objwalk(obj, path=(), memo=None, recursion=0):
    if memo is None:
        memo = set()
    if isinstance(obj, Object):
        if id(obj) not in memo and recursion < 4:
            memo.add(id(obj)) 
            for k in dir(obj):
                val = getattr(obj, k)
                if isinstance(val, Property):
                    for child in _objwalk(val, path + (k,), memo, recursion+1):
                        yield child
                    if val._property_value:
                        for child in _objwalk(val._property_value, path + (k,), memo, recursion+1):
                            yield child
                    else:
                        # has no value, return default value
                        pass
    elif isinstance(obj, ListLike):
        if id(obj) not in memo and recursion < 4:
            memo.add(id(obj)) 
            for index, value in enumerate(obj):
                for child in _objwalk(value, path + (index,), memo, recursion+1):
                    yield child
    else:
        yield path, obj

def _get_recursive_objects(obj, leveldeep=0):
    if leveldeep > 10: return set([obj])
    ret = set()
    for p in _objwalk(obj, recursion=leveldeep+1):
        v = p[1]._property_value
        if isinstance(v, ListLike):
            for o in v:
                ret |= _get_recursive_objects(o, leveldeep+1)
        else:
            if v: ret.add(v)
            else: ret.add(p[1]._value._none_object)
    return ret | set([obj])



def _create_problem(methods, space, exit=None, goal=None, sessionName=None):
    """schedule methods within variables space space with exit method exit or goal goal"""
    # 1. for every variable in space, 
    #    - create a full :predicates description of the object 
    #    - create init objects
    # 2. for every method, add them to planning problem
    assert isinstance(space, list)
    global _selector_out
    _selector_out = None

    class XSProblem(Problem):
        pass
    
    if sessionName: XSProblem.__name__ = sessionName
    p = XSProblem()
    p.objectList = [x for x in space if isinstance(x, Object)]
    
    l_collected_predicates = set()
    l_collected_objects = collections.defaultdict(list)
    l_collected_classes = set()
    l_collected_facts = set()
    p.gen_hashnums()
    l_collected_goal = []
    if goal:
        _reset_state()
        _compilation_enable()
        try:
            goal = Select(goal())
        except Exception as e:
            et, ei, tb = sys.exc_info()
            _compilation_enable(False)
            raise ei.with_traceback(tb)
        if not type(goal) == list:
            goal = [goal]
        for g in goal:
            for ph in g._parse_history:
                l_collected_goal += ph["text_predicates"]
        _compilation_enable(False)
    # TODO: scan objects recursively: expand space with recursive scan
    l_collected_objects[HASHNUM_CLASS_NAME].append("p-null-Imaginary")
    for ob in p.objectList + list(_system_objects.values()):
        ob._parse_history = []
        l_collected_predicates |= set(ob._get_all_predicates())
        l_collected_objects[ob.__class__.__name__].append(ob.name.split()[0])
        for no in ob._get_all_none_objects():
            l_collected_objects[no.__class__.__name__].append(no.name.split()[0])
        if not ob.__class__._none_object in l_collected_objects[ob.__class__.__name__]:
            l_collected_objects[ob.__class__.__name__].append(ob.__class__._none_object.name.split()[0])
        l_collected_classes.add(ob.__class__.__name__)
        l_collected_facts |= set(ob._get_all_facts())

    #################################
    # TEST OBJECT SPACE TODO REMOVE THIS
    l_all_objects_defs = set()
    for o in l_collected_objects.values():
        l_all_objects_defs |= set(o)
    for f in l_collected_facts:
        for fct in f.replace("(", "").replace(")", "").split()[1:]:
            if not fct in l_all_objects_defs:
                raise AssertionError("Fact %s is not in classes space" % (fct))
    #################################


    # 3. extract the created goal from global stack
    # global _collected_predicates
    global _collected_effects
    # l_collected_goal = list(filter(None, list(collections.OrderedDict.fromkeys(_collected_predicates + _collected_effects))))
    _collected_predicates = []
    _collected_effects = []
    _selector_out = None

    
    # TODO: collected_classes should derive from collected_ojbects
    l_collected_classes |= set(l_collected_objects.keys())
    p.collected_objects = l_collected_objects
    p.collected_classes = list(l_collected_classes)
    p.collected_facts = list(l_collected_facts)
    p.collected_goal = list(filter(None, l_collected_goal))
    p.get_types = lambda: ' '.join(list(filter(None, list(l_collected_classes))))
    p.get_predicates = lambda: "\n        ".join(list(set(l_collected_predicates)))
    
    assert p.collected_goal
    
    mcount = 0
    actions = [] 
    
    for m in methods:
        if not callable(m): continue
        # if not hasattr(m, "plan_class"): continue
        if not hasattr(m, "_planned"): continue
        pm = _planned_internal(m, cost=m._cost)
        actions.append(pm.plan_class)
        # actions.append(m.plan_class)
        # def methodWrapper(self, *args, **kwargs):
        #     return pm(*args, **kwargs)
        # methodWrapper.__name__ = m.__name__
        # methodWrapper.plan_class = m.plan_class
        # setattr(p, m.__name__, methodWrapper)
        mcount+=1
    p.actions = lambda: actions
    if not mcount: raise ValueError("No methods can be scheduled")
    
    p.format_problem()
    return p

def debug_plan(methods, space, exit=None, goal=None, plan=[], iterations=10):
    space = _space_to_list(space)
    assert methods
    assert space
    assert plan
    p = _create_problem(methods, space, exit, goal)
    p.solution = lambda: [_planned_internal(a, cost=a._cost) for a in plan ]
    r = p.check_solution(iterations)
    # clean up after debugging
    _reset_state()
    return r
    

def schedule(methods, space, exit=None, goal=None, sessionName=None):
    space = _space_to_list(space)
    p = _create_problem(methods, space, exit, goal, sessionName)
    p.run()
    _reset_state()
    for v in space: 
        if isinstance(v, Object): v._sealed = False
    if p.plan is None: raise SchedulingError("Unable to solve")
    if not p.plan: raise EmptyPlanError("Empty plan")
    return p.plan
    
    

def xschedule(methods, space, exit=None, goal=None, sessionName=None):
    """schedule methods within variables space space with exit method exit or goal goal
    this function returns a composable method that has the resulting algorithm built in"""
    return [x() for x in schedule(methods, space, exit, goal, sessionName)][-1]
    
