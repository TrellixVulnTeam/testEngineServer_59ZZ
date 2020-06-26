
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from flask import send_from_directory
from flask import send_file
from IPython.display import HTML
import ast
import operator
from collections import OrderedDict
import jsbeautifier
import subprocess
import shlex
import os
import fnmatch
import shutil
from json2html import *
from ppadb.client import Client as AdbClient
import re


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def create_download_link(title, filename):  
    html = '<a href=http://localhost:5001/jsonFile/{filename}>{title}</a>'
    html = html.format(title=title,filename=filename)
    return HTML(html)

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z    

@app.route('/createJson', methods=['GET', 'POST'])
def createjson():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data1 = request.get_json()
        post_data = ast.literal_eval(json.dumps(post_data1))
        print(post_data)
        filename = "filename"
        scenarios = "scenarios"
        sc_count = "scenario_count"
        steps = "steps"
        step_count = "stepcount"
        scenario1 = {}
        scenarioName = []
        stepArray = {}
        scenarioArray = {}
        print (post_data)
        if filename in post_data.keys() :
            jsonName = str(post_data[filename])
        post_data.pop('filename')
        print('kkkkk')
        if scenarios in post_data.keys() :
            scenario1 = post_data[scenarios]
            print('ccccc')
            for scname in scenario1 :
                scenario2 = scenario1[scname]
            print(scenario2)
            scenarioCount = scenario2[sc_count]
            print(scenarioCount)
            scenario2.pop(sc_count)
            print(scenario2)
            skeys = sorted(scenario2.keys(), key=lambda s: int(s))
            print(skeys)
            sorted_scenario_dict = dict((k, scenario2[k]) for k in skeys)
            print(sorted_scenario_dict)
            sorted_scenario_dict[sc_count] = scenarioCount
            print(sorted_scenario_dict)
            for scName in skeys :
                scenarioName.append(scenario2[scName]['name'])
            print(scenarioName)
        scenarioArray[scname] = sorted_scenario_dict
        print(scenarioArray)

        if steps in post_data.keys() :
            steps1 = post_data[steps]
            for scNames in scenarioName :
                scenarioSteps = steps1[scNames]
               # print(scenarioSteps)
                stepCount = scenarioSteps[step_count]
                print(stepCount)
                scenarioSteps.pop(step_count)
                print(scenarioSteps)
                stepkeys = sorted(scenarioSteps.keys(), key=lambda s: int(s))
                print(stepkeys)
                sorted_steps_dict = dict((k, scenarioSteps[k]) for k in stepkeys)
                print(sorted_steps_dict)
                sorted_steps_dict[step_count] = stepCount
                print(sorted_steps_dict)
                stepArray[scNames] = sorted_steps_dict
        print(stepArray)
        completeArray = merge_two_dicts(scenarioArray, stepArray)
        print(completeArray)
        with open("files/"+jsonName+".json", 'w') as file1:
            json.dump(completeArray, file1, indent=2)
            response_object = create_download_link("Download JSON file",jsonName+".json")
      #  with open("files/"+jsonName+".json", 'w') as file1:    
       #     opts = jsbeautifier.default_options()
       #     opts.indent_size = 2
       #     file1.write(jsbeautifier.beautify(json.dumps(completeArray), opts))
       #     response_object = create_download_link("Download JSON file",jsonName+".json")
    return jsonify(response_object)


@app.route('/jsonFile/<path:filename>', methods=['GET', 'POST'])
def download(filename): 
    directoryname = 'files'  
    return send_from_directory(directory=directoryname, filename=filename, as_attachment=True)

@app.route('/application', methods=['GET', 'POST'])
def application():
    response_object = {'status': 'success'}
    with open('Application.json', 'r') as json_file :
        appList = json.load(json_file)
        print(appList)
        return jsonify(appList)

@app.route('/listscenarios/', methods=['GET'])
def scenariolist():
    #response_object = {'status': 'success'}
    app = request.args.get('app')
    os = request.args.get('os')
    if request.method == 'GET':
        with open("listscenarios.json", 'r') as json_file :
            data = json.load(json_file)
            print(data)
            if app in data.keys() :
                print("Present")
                selectApp = data[app]
                print (selectApp)
                if os in selectApp.keys() :
                    print("present")
                    selectOS = selectApp[os]
                    print(selectOS)
                    scenarios = selectOS['scenarios']
                    print(scenarios)
           # print(scenarios)
   # jsonFiles = [f for f in os.listdir("files") if fnmatch.fnmatch(f, '*.json')]
   # print(jsonFiles)
   # listFiles = [os.path.splitext(x)[0] for x in jsonFiles]
   # print(lst)
    return jsonify(scenarios)

@app.route('/viewscenarios/', methods=['GET', 'POST'])
def scenarioview():
    response_object = {'status': 'success'}
    with open('listscenarios.json', 'r') as json_file :
        scenarios = json.load(json_file)
        print(scenarios)
        return jsonify(scenarios)

@app.route('/screenNames/<app>', methods=['GET', 'POST'])
def screen_names(app):
    response_object = {'status': 'success'}
    print('bbb')
    if request.method == 'GET':
        with open(app+".json", 'r') as json_file :
          appdata = json.load(json_file)
          response_object = appdata   
    return jsonify(response_object)        

@app.route('/editValue/<app_name>', methods=['GET', 'POST'])
def edit_value(app_name):
    response_object = {'status': 'success'}
    print('bbb')
    if request.method == 'GET':
        with open(app_name+".json", 'r') as json_file :
          appdata = json.load(json_file)
          print (appdata)
          print(appdata.keys())
          maindata = appdata[app_name]
          print (maindata)
          value = "value"
          if value in maindata.keys():
              print("Present")
              response_object = maindata[value]
              print(response_object)
          else:
              response_object = "Operand not present"    
    return jsonify(response_object)

@app.route('/updateValue', methods=['GET', 'POST'])
def update_Value():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        app_name = post_data.get('application')
        filename = app_name+".json"
        print(filename)
    with open(filename, 'r') as json_file : 
        exdata = json.load(json_file)
        exdataApp = exdata[app_name]
        print(exdata)
        value = "value"
        if value in exdataApp.keys(): 
            print("Present, ") 
            exdataApp.pop(value)
            print(exdata)
            exdataApp['value'] = post_data.get('value')
            print(exdata) 
        else: 
            print("Not present")
        #newdata.update(exdata)
        with open(filename, 'w') as f:
            json.dump(exdata, f, indent=2, sort_keys=False)
            #print(dbdata)
        #response_object = calculatedynamic()
        return jsonify(response_object)

@app.route('/editAction/<app_name>', methods=['GET', 'POST'])
def edit_action(app_name):
    response_object = {'status': 'success'}
    print('bbb')
    if request.method == 'GET':
        with open(app_name+".json", 'r') as json_file :
          appdata = json.load(json_file)
          print (appdata)
          print(appdata.keys())
          maindata = appdata[app_name]
          print (maindata)
          Action = "Action"
          if Action in maindata.keys():
              print("Present")
              response_object = maindata[Action]
              print(response_object)
          else:
              response_object = "Operand not present"    
    return jsonify(response_object)        

@app.route('/updateAction', methods=['GET', 'POST'])
def update_Action():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        app_name = post_data.get('application')
        filename = app_name+".json"
        print(filename)
    with open(filename, 'r') as json_file : 
        exdata = json.load(json_file)
        exdataApp = exdata[app_name]
        print(exdata)
        Action = "Action"
        if Action in exdataApp.keys(): 
            print("Present, ") 
            exdataApp.pop(Action)
            print(exdata)
            exdataApp['Action'] = post_data.get('action')
            print(exdata) 
        else: 
            print("Not present")
        #newdata.update(exdata)
        with open(filename, 'w') as f:
            json.dump(exdata, f, indent=2, sort_keys=False)
            #print(dbdata)
        #response_object = calculatedynamic()
        return jsonify(response_object)


@app.route('/execFlow/<param>', methods=['GET', 'POST'])
def exec_action(param):
    print('bbb')
    print(param)
    paramlist = param.split(",")
    print(paramlist)
    response_object = {'status': 'success'}
    exdata = {}
    for scenarios in paramlist :
        print(scenarios)
        stringtoExecute = './test.sh ' + scenarios
        print(stringtoExecute)
        subprocess.call(shlex.split(stringtoExecute))
        shutil.copy2('/Users/snithinnarayanan/tile_automation_android-dev/logs/tile_automation_android_logs.html', 'logs/')
        shutil.copy2('/Users/snithinnarayanan/tile_automation_android-dev/logs/tile_automation_android_logs.json', 'logs/')
        report_file = open('logs/tile_automation_android_logs.html')
        with open('logs/tile_automation_android_logs.json', 'r') as json_file1 :
            newdata = json.load(json_file1)
            exdata.update(newdata)
        html = report_file.read()
    print(exdata)
    with open('logs/report.json', 'w') as f:
        json.dump(exdata, f, indent=2, sort_keys=False)
    response_object = json2html.convert(json = exdata)
    print(response_object)
    firstpart = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<title>Automation test result</title>\n    <style>\n            table {\nborder-collapse: collapse;\npadding:0.5rem;\nwidth: 100%;\n }\n\ntd {\nborder: 1px solid #999;\npadding: 0.0rem;\ntext-align: left;\n\n}\n\nth\n\n {\nborder: 1px solid #999;\npadding: 0.5rem;\ntext-align: left;\n\n }\n\n</style>\n</head>\n<body>\n\n\n<div><h4>Android Automation  Testing Report <script> document.write(new Date().toLocaleDateString()); </script> </h4></div>"
    lastpart = "</body>\n</html>"
    response_object = firstpart + response_object + lastpart
    print(response_object)
    payload = {
        "html_response": response_object
        }
    return jsonify(payload)

@app.route('/report', methods=['GET', 'POST'])
def downloadReport(): 
    directoryname = 'logs'
    filename = 'tile_automation_android_logs.html'
    print(filename,directoryname)   
    return send_from_directory(directory=directoryname, filename=filename, as_attachment=True)                                                                     

if __name__ == '__main__':
    app.run(host="localhost",port=5001) 
