tox:
	tox
net:
	python3.7 -m problem.pydlNetProblem

test: tox

kube:
	python3.7 -m problem.pydlKubeProblem
sqldemo: 
	python3.7 -m action.sqlDemo

release: 
	pyarmor obfuscate ./poodle_lib/poodle.py
	-git clone https://github.com/grandrew/poodle-release.git
	cd poodle-release && git pull && git checkout v2pip37
	cat ./dist/poodle.py  | sed s/pytransform/poodle.pytransform/g > ./poodle-release/poodle_lib/poodle.py
	cd poodle-release && git add poodle_lib/poodle.py && git commit -m "fix" && git push
	
all: net test

