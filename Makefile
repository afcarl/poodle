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
	cat ./poodle_lib/poodle_main.py | sed s/127.0.0.1:8082/devapi.xhop.ai:8082/g > ./poodle_lib/poodle_main_temp.py
	pyarmor obfuscate ./poodle_lib/poodle_main_temp.py
	-git clone https://github.com/xhop-ai/poodle-release.git
	cd poodle-release && git pull && git checkout v2pip37
	cat ./dist/poodle_main_temp.py | sed s/pytransform/poodle.pytransform/g > ./poodle-release/poodle_lib/poodle.py  
	cd poodle-release && git add poodle_lib/poodle.py && git commit -m "fix" && git push
	
all: net test

