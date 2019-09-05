# Poodle - AI Planning in Python

Poodle is the Python 3 framework for AI Planning and automated programming

## Installation

`python3.7 -m pip install git+https://github.com/criticalhop/poodle`

## Introduction

Poodle enables construction of complex planning and constraint satisfaction problems using familiar python paradigms in production environments. It is still in early stage of development but is already powering our tool to prevent Kubernetes configuraion errors.

It introduces a new python method `xschedule` and a new base object `Object`:

```python
xschedule(
    methods=[methodToPlan1, methodToPlan1, ...],
    space=[object1, object1, ...],
    goal=lambda:"""condition for object state"""
)
```

where `methods` is the list of methods that the planner should use to try to reach the goal state; `space` contains the list of `Object` objects that the planner will try to use as parameters for the methods, and `goal` is a simple end state condition expresed as Python logical expression, usually a `lambda` function.

`Object` is a special object type that knows how to translate itself to PDDL.

To understand how to construct a first real problem let's start with a simple method:

```python
from poodle import Object, xschedule

class World(Object):
    said: bool

def hello(world: World):
    assert world.said == False
    print("Hello, World!")
    world.said = True

w = World()
w.said = False

xschedule(methods=[hello], space=[w], goal=lambda:w.said==True)
```

This program would immediately print "Hello, World!" to the console, which looks obvious at the beginning. What actually happened is that Poodle compiled your Python method into planning problem and found that the final state is achievable by simply executing the only method.

It essentially searches for such a set of inputs that satisfies `assert` expressions present in the python function, and combines as many such functions as needed to reach a goal state.

It is important to note that the more precise you describe your task the easier it is for the AI planner to figure out the algorithm. That is why Poodle enforces fully statically typed interface for all objects and methods in search space as a minimum selectivity requirement. This also saves from a lot of bugs in bigger projects.

Let's now jump to a more sophisticated example:

TODO