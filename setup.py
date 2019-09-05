#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    python_requires='>=3.7',
    name='poodle',
    version="0.1",
    url='https://github.com/criticalhop/poodle',
    description=(
        "Python AI Planning and automated programming extension"),
    long_description=open('README.md').read(),
    keywords="Poodle, PDDL, AI Planning, Constraint programming, CriticalHop, automatic programming",
    # license=open('LICENSE').read(), # breaks tox
    platforms=['linux'],
    packages=['poodle'],
    package_dir = {'poodle': 'poodle_lib'},
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],

)