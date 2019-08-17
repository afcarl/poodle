from poodle import *
import collections.abc
from .poodle_main import Select, _collected_predicates, _collected_effects, _none_objects, _system_objects, HASHNUM_CLASS_NAME, _selector_out, _reset_state

class SchedulingError(Exception):
    pass

def planned2(fun=None, *, cost=None):
    global _selector_out
    _selector_out = None
    if fun is None:
        return functools.partial(planned, cost=cost)
    cost = cost if cost else 1
    if not getattr(fun, "__annotations__", None):
        raise ValueError("For planning to work function parameters must be type annotated with at least one parameter")
    kwargs = {}
    for k, v in fun.__annotations__.items(): 
        if isinstance(v, str):
            raise ValueError("Forward references are not suported in methods yet")
        else:
            kwargs[k] = v(_variable_mode=True)
    class NewPlannedAction(PlannedAction):
        def effect(self):
            global _selector_out
            fun(**kwargs)
            _selector_out = None
    for k, v in kwargs.items(): setattr(NewPlannedAction, k, v)
    NewPlannedAction.__name__ = fun.__name__
    NewPlannedAction.cost = cost
    NewPlannedAction.wrappedMethod = [fun]
    fun.plan_class = NewPlannedAction
    return fun

def _create_problem(methods, space, exit=None, goal=None):
    """schedule methods within variables space space with exit method exit or goal goal"""
    # 1. for every variable in space, 
    #    - create a full :predicates description of the object 
    #    - create init objects
    # 2. for every method, add them to planning problem
    assert isinstance(space, collections.abc.Mapping)
    global _selector_out
    _selector_out = None

    class XSProblem(Problem):
        pass
    
    p = XSProblem()
    p.objectList = [x for x in list(space.values()) if isinstance(x, Object)]
    
    l_collected_predicates = set()
    l_collected_objects = collections.defaultdict(list)
    l_collected_classes = set()
    l_collected_facts = set()
    p.gen_hashnums()
    # TODO: scan objects recursively
    for ob in p.objectList + list(_system_objects.values()):
        l_collected_predicates |= set(ob._get_all_predicates())
        l_collected_objects[ob.__class__.__name__].append(ob.name.split()[0])
        if not ob.__class__._none_object in l_collected_objects[ob.__class__.__name__]:
            l_collected_objects[ob.__class__.__name__].append(ob.__class__._none_object.name.split()[0])
        l_collected_classes.add(ob.__class__.__name__)
        l_collected_facts |= set(ob._get_all_facts())
        
    # 3. extract the created goal from global stack
    # global _collected_predicates
    global _collected_effects
    # l_collected_goal = list(filter(None, list(collections.OrderedDict.fromkeys(_collected_predicates + _collected_effects))))
    l_collected_goal = []
    if goal:
        for ph in goal._parse_history:
            l_collected_goal += ph["text_predicates"]
    _collected_predicates = []
    _collected_effects = []
    _selector_out = None

    l_collected_objects[HASHNUM_CLASS_NAME].append("p-null-Imaginary")
    
    # TODO: collected_classes should derive from collected_ojbects
    p.collected_objects = l_collected_objects
    p.collected_classes = list(l_collected_classes)
    p.collected_facts = list(l_collected_facts)
    p.collected_goal = list(filter(None, l_collected_goal))
    p.get_types = lambda: ' '.join(list(filter(None, list(l_collected_classes))))
    p.get_predicates = lambda: "\n        ".join(list(set(l_collected_predicates)))
    
    
    mcount = 0
    actions = [] 
    
    for m in methods:
        if not callable(m): continue
        if not hasattr(m, "plan_class"): continue
        pm = planned2(m, cost=m.plan_class.cost)
        actions.append(pm.plan_class)
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

def debug_plan(methods, space, exit=None, goal=None, plan=[], iterations=50):
    p = _create_problem(methods, space, exit, goal)
    p.solution = lambda: plan
    r = p.check_solution(iterations)
    # clean up after debugging
    _reset_state()
    return r
    

def schedule(methods, space, exit=None, goal=None):
    p = _create_problem(methods, space, exit, goal)
    p.run()
    if p.plan is None: raise SchedulingError("Unable to solve")
    _reset_state()
    for o,v in space.items(): 
        if isinstance(v, Object): v._sealed = False
    return p.plan
    
    

def xschedule(methods, space, exit=None, goal=None):
    """schedule methods within variables space space with exit method exit or goal goal
    this function returns a composable method that has the resulting algorithm built in"""
    return [x() for x in schedule(methods, space, exit, goal)][-1]
    
