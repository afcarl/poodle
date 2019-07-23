#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='poodle',
    version=1,
    url='https://github.com/grandrew/poodle',
    description=(
        "Poodle development"
        "Depends sudo apt install python3.7 python3-jinja2 python3-jinja2-time cookiecutter"),
    long_description=open('README.md').read(),
    keywords="Poodle, Pddl, CriticalHop",
    license=open('LICENSE').read(),
    platforms=['linux'],
    packages=find_packages(),
    include_package_data=True,
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Other/Nonlisted Topic'],
)