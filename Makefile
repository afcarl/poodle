net:
	python3 -m problem.pydlNetProblem
test:
	python3 -m unittest tests.testFromTrello
all: net test
