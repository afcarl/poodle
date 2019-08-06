net:
	python3.7 -m problem.pydlNetProblem
test:
	python3.7 -m unittest tests.testFromTrello
kube:
	python3.7 -m problem.pydlKubeProblem
sqldemo: 
	python3.7 -m action.sqlDemo
obfuscate: 
	pyarmor obfuscate ./poodle/poodle.py
	cat ./dist/poodle.py  | sed s/pytransform/poodle.pytransform/g > ../poodle-release/poodle/poodle.py

all: net test

