net:
	python3.7 -m problem.pydlNetProblem
test:
	python3.7 -m unittest tests.testFromTrello
	python3.7 -m problem.py-kube
all: net test

