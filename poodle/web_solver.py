# coding: utf-8
# from flask import Flask, render_template
from flask import Flask, request, redirect, url_for, Response, make_response
import os, signal
import os.path
import subprocess
import time
import re
import sys
import base64 
import string
import logging
import random
import datetime
import time
from threading import Thread
from poodle import pddlSplitter


log = logging.getLogger()
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout) # loggging driver
handler.setLevel(logging.DEBUG) #loglevel ->> CRITICAL ERROR WARNING INFO DEBUG NOTSET
log.addHandler(handler)

app = Flask(__name__, template_folder='.')
app.secret_key = "super secret key2"

def allowed_file(fn):
    return True
def secure_filename(fn):
    return fn

def crypt(key, data):
    return data
    S = list(range(256))
    j = 0

    for i in list(range(256)):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    j = 0
    y = 0
    out = []

    for char in data:
        j = (j + 1) % 256
        y = (y + S[j]) % 256
        S[j], S[y] = S[y], S[j]

        out.append(chr(ord(char) ^ S[(S[j] + S[y]) % 256]))

    return ''.join(out)

storage = {}
SOLVER_KEY = "list(filter(None, _collected_predicates + _collected_effects))"
SOLVER_PROCESSING_STATUS = 'PROCESSING'
SOLVER_ERROR_STATUS = 'ERROR'
SOLVER_UNKNOWN_STATUS = 'UNKNOWN'
SOLVER_DONE_STATUS = 'DONE'
SOLVER_KILLED_STATUS = 'KILLED'
SOLVER_MAX_TIME = 60

def kill_task_by_id(id):
    # print("kill? ...")
    if id in storage:
        print("KILLING PROCESS !!!!!")
        proc = storage[id]['proc'] 
        pid = proc.pid
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        # os.kill(pid, signal.SIGTERM)
        # time.sleep(0.5)
        proc.terminate()
        os.remove("{0}/output.sas".format(storage[id]['folder']))
        del storage[id]
        return SOLVER_KILLED_STATUS
    return SOLVER_UNKNOWN_STATUS  

def killing_threat(id):
    while 1:
        time.sleep(2)
        if not id in storage:
            return 1
        elif int(time.time() - storage[id]['check_time']) > SOLVER_MAX_TIME :
            kill_task_by_id(id)
            return 0
            
          

def working_threat(id):
    if id in storage:
        std_out = []
        retcode = "-1"
        folder_name = storage[id]["folder"]
        fd = open(folder_name+"/stdout.log","w+")
        for line in storage[id]['proc'].stdout:
            print(line)
            fd.write(line)
            fd.flush()
            std_out.append(line) 
            if line.find('search exit code:') != -1:
                retcode = line.rstrip("\n").split()[3]
            log.info(line.rstrip("\n"))
        # fd = open(folder_name+"/stdout.log","w+")
        # fd.write("".join(std_out))
        # fd.flush()
        fd.close()
                
        if retcode == "0" :
            storage[id]['status'] = SOLVER_DONE_STATUS
        else: 
            storage[id]['status'] = SOLVER_ERROR_STATUS   


@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'POST':
        #print(request.form.get("d"))
        domain = crypt(SOLVER_KEY, request.form.get("d"))#base64.b64decode()
        problem = crypt(SOLVER_KEY, request.form.get("p"))#base64.b64decode()
        pddl_name = crypt(SOLVER_KEY, request.form.get("n"))
        
        counter = 0
        try:
            with open("./.counter", "r") as fd:
                counter = int(fd.read())
        except:
            counter = 0
 
        counter += 1
        with open("./.counter", "w") as fd:
            fd.write(str(counter))
        

        rnd = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
        while rnd in storage : 
            rnd = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
            
        folder_name = "./out/{0:05d}_{1}_{2}_{3}".format(counter, pddl_name, str(datetime.date.today()),rnd)
        os.makedirs(folder_name)

        asplitter = pddlSplitter.ActionSplitter(str(domain))
        domain_new = asplitter.split()
        if asplitter.splitted_actions:
            problem_new = asplitter.fix_problem(problem)
            with open("{0}/problem_orig.pddl".format(folder_name), "w+") as fd:
                fd.write(str(problem))
            problem = problem_new
        with open("{0}/problem.pddl".format(folder_name), "w+") as fd:
            fd.write(str(problem))
        with open("{0}/domain.pddl".format(folder_name), "w+") as fd:
            fd.write(str(domain_new))
        with open("{0}/domain_orig.pddl".format(folder_name), "w+") as fd:
            fd.write(str(domain))
            
       
            
        max_time = 90000
        runscript = os.getenv("PYTHON", "python")+' ./fast-downward.py --plan-file "{folder}/out.plan" --sas-file {folder}/output.sas {folder}/domain.pddl {folder}/problem.pddl --evaluator "hff=ff()" --evaluator "hlm=lmcount(lm_rhw(reasonable_orders=true))" --search "lazy_wastar(list(hff, hlm), preferred = list(hff, hlm), w = 5, max_time={maxtime})"'.format(folder=folder_name, maxtime=max_time)        
        proc = subprocess.Popen(runscript, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, preexec_fn=os.setsid)
        storage[rnd] = {'proc': proc, 'folder': folder_name, 'status': SOLVER_PROCESSING_STATUS, 'check_time': time.time(), "splitter": asplitter}
        
        thread = Thread(target = working_threat, args = [rnd])
        thread.start()
        
        thread = Thread(target = killing_threat, args = [rnd])
        thread.start()

        response_text = rnd
            
        response = make_response(crypt(SOLVER_KEY, response_text))    
        response.set_cookie('CH_SESS', 'NULL')
        response.headers.set('Content-Type', 'text/plain')
        return response
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=xml>
      <input type=submit value=Upload>
    </form>
    '''

def check_status_by_id(id):
    if id in storage:
        storage[id]['check_time'] = time.time() 
        return storage[id]['status'] 
    return SOLVER_UNKNOWN_STATUS

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        pddl_task_id = crypt(SOLVER_KEY, request.form.get("id"))
        
        result = check_status_by_id(pddl_task_id)
        
        response = make_response(crypt(SOLVER_KEY, result))    
        response.headers.set('Content-Type', 'text/plain')
        return response
    return ''

@app.route('/kill', methods=['GET', 'POST'])
def kill():
    if request.method == 'POST':
        pddl_task_id = crypt(SOLVER_KEY, request.form.get("id"))
        
        result = kill_task_by_id(pddl_task_id)
        
        response = make_response(crypt(SOLVER_KEY, result))    
        response.headers.set('Content-Type', 'text/plain')
        return response
    return SOLVER_UNKNOWN_STATUS

def get_result_by_id(id):
    if id in storage:
        if storage[id]['folder'] != None :
            f = open("{0}/out.plan".format(storage[id]['folder']),'r')
            response_text = f.read()
            f.close()
            os.remove("{0}/output.sas".format(storage[id]['folder']))
            print("Unsplitting plan", response_text)
            response_text = storage[id]["splitter"].unsplit_plan(response_text)
            print("UnsplittED plan", response_text)
            open("{folder}/out_unsplit.plan".format(folder=storage[id]["folder"]),"w+").write(response_text)
            return response_text
    return SOLVER_ERROR_STATUS


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        pddl_task_id = crypt(SOLVER_KEY, request.form.get("id"))
        
        result = get_result_by_id(pddl_task_id)
        
        response = make_response(crypt(SOLVER_KEY, result))    
        response.headers.set('Content-Type', 'text/plain')
        return response
    return SOLVER_UNKNOWN_STATUS

def serve():
    assert os.path.isfile("./fast-downward.py"), \
        """Fast-downward installation not found in current 
    directory. Please `cd` into fast-downward installation folder
    and make sure fast-downward.py is present"""
    debug = True
    app.debug = debug
    app.run(host='127.0.0.1', port=16009, debug=True, use_reloader=False)
    server.serve_forever()