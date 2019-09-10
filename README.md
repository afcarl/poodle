# Poodle - AI Planning in Python

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![PyPI version](https://badge.fury.io/py/poodle.svg)](https://badge.fury.io/py/poodle) [![Build Status](https://travis-ci.org/criticalhop/poodle.svg?branch=master)](https://travis-ci.org/criticalhop/poodle)

Poodle is the Python 3 framework for AI Planning and automated programming

# Overview

## The Dream



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

This program would immediately print "Hello, World!" to the console, which looks obvious at the beginning. What actually happened is that Poodle compiled your Python method into planning problem and found that the final state is achievable by simply executing the only method, and all `assert`s are satisfied with object `w`.

It is important to note that the more precise you describe your task the easier it is for the AI planner to figure out the algorithm. That is why Poodle enforces fully statically typed interface for all objects and methods in search space as a minimum selectivity requirement. This also saves from a lot of bugs in bigger projects.

Let's now jump to a more sophisticated example:

TODO

# Installation

```shell
pip install poodle
```

Poodle requires Python 3.7+

## Running local solver

If you don't specify, Poodle will use a hosted solver environment from [CriticalHop](https://criticalhop.com), which has some limitations in its free-to-use version. To try with your local server the environment variable `POODLE_SOLVER_URL` must be set:

```shell
export POODLE_LOCAL_URL=http://localhost:8082
```

To run a local solver you must first install [fast-downward](http://www.fast-downward.org/). After you have fast-downward running - issue `poodleserver` from fast-downard folder:

```shell
cd fast-downward
poodleserver
```

will serve requests on port 8082 on localhost

# Contacts

Poodle is supported by [CriticalHop](https://criticalhop.com). If you have any questions, feel free to open a [github issue](https://github.com/criticalhop/poodle/issues) and chat with the team at `##poodle` on [freenode](https://freenode.net/).

If you would like to support the project or plan to use enterprise edition please write at info@criticalhop.com or chat directly to `@grandrew` on freenode IRC.