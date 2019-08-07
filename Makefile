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
	-git clone https://github.com/grandrew/poodle-release.git
	cd poodle-release && git pull && git checkout v2pip37
	cat ./dist/poodle.py  | sed s/pytransform/poodle.pytransform/g > ./poodle-release/poodle/poodle.py
	cd poodle-release && git add poodle/poodle.py && git commit -m "fix" && git push
	
	
	
all: net test

