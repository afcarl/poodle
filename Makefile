net:
	python3 -m problem.pydlNetProblem
test:
	python3 -m unittest tests.testFromTrello
kube:
	python3 -m problem.py-kube
all: net test

