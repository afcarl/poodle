# coding: utf-8
# from flask import Flask, render_template
from flask import Flask, flash, request, redirect, url_for, Response, make_response
import os
import subprocess
import time
import re
import sys
import base64 
import string
import logging
import random
import datetime


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


@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'POST':
        print("ok")
        domain = request.form.get("domain")#base64.b64decode()
        problem = request.form.get("problem")#base64.b64decode()
        
 
        counter = 0
        try:
            with open("./.counter", "r") as fd:
                counter = int(fd.read())
        except:
            counter = 0
 
        counter += 1
        with open("./.counter", "w") as fd:
            fd.write(str(counter))
        

        rnd = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        folder_name = "./out/{0:05d}_{1}_{2}".format(counter, str(datetime.date.today()),rnd)
        os.makedirs(folder_name)
        
        with open("{0}/problem.pddl".format(folder_name), "w+") as fd:
            fd.write(str(problem))
        with open("{0}/domain.pddl".format(folder_name), "w+") as fd:
            fd.write(str(domain))
            
       
            
        max_time = 10000
        # TODO: create "debug" mode to run in os command and show output in real time
        runscript = 'pypy ../../downward/fast-downward.py --plan-file "{folder}/out.plan" --sas-file {folder}/output.sas {folder}/domain.pddl {folder}/problem.pddl --evaluator "hff=ff()" --evaluator "hlm=cg(transform=no_transform())" --search "lazy_wastar(list(hff, hlm), preferred = list(hff, hlm), w = 5, max_time={maxtime})"'.format(folder=folder_name, maxtime=max_time)
        std = subprocess.Popen(runscript, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True).stdout
        retcode = "-1"
        response = ''
        response_text = "ERROR"
        for line in std:
            response_text += line
            if line.find('search exit code:') != -1:
                retcode = line.rstrip("\n").split()[3]
            log.info(line.rstrip("\n"))
            
        if retcode == "0" :
            if folder_name != None:
                f = open("{0}/out.plan".format(folder_name),'r')
                response_text = f.read()
                f.close()
            #    actionClassLoader = ActionClassLoader(self.actions(), self)
            #    actionClassLoader.loadFromFile("{0}/out.plan".format(folder_name))
            #    self._plan = actionClassLoader._plan
        response = make_response(response_text)    
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)