net:
	python3.7 -m problem.pydlNetProblem
test:
	python3.7 -m unittest tests.testFromTrello
kube:
	python3.7 -m problem.py-kube
all: net test

