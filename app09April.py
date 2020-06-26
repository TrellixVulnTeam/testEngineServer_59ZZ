
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from flask import send_from_directory
from flask import send_file
from IPython.display import HTML
import ast
import operator
from collections import OrderedDict 


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

@app.route('/createJson', methods=['GET', 'POST'])
def createjson():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
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
        if scenarios in post_data.keys() :
            scenario1 = post_data[scenarios]
            for scname in scenario1 : 
                scenario2 = scenario1[scname]
            print(scenario2)
            scenarioCount = scenario2[sc_count]
            print(scenarioCount)
            scenario2.pop(sc_count)
            print(scenario2)
           # d = {'24': {'name': 'fghfg', 'enabled': 'TRUE', 'desc': 'dfg', 'testcase_id': 'dfg'}, '11': {'name': 'kkkk', 'enabled': 'FALSE', 'desc': 'sss', 'testcase_id': 'ddd'}, '17': {'name': 'jjjjjj', 'enabled': 'TRUE', 'desc': 'jjjj', 'testcase_id': 'jjjjj'}, '9': {'name': 'mmmmm', 'enabled': 'TRUE', 'desc': 'mmmm', 'testcase_id': 'mmmmm'}}
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
        test = {'fghfg': {
        '1': {'screen_name': 'pj_admin_reports', 'name': 'XPATH_ADMIN_ENTRY_STATISTICS_REPORT', 'action': 'switch_frame', 'value': 'time_filter', 'cond_exec': 'enabled'}, 'stepcount': 1},
        'jjjjjj': {
        '1': {'screen_name': 'pj_revenue_report', 'name': 'XPATH_SWITCH_IFRAME1', 'action': 'new_tab', 'value': 'time_filter2', 'cond_exec': 'enabled', 'skipflag': 'enabled'}, 
        '2': {'screen_name': 'pj_admin_page', 'name': 'XPATH_ADMIN_SESSION_DROPDOWN', 'action': 'close_tab', 'value': 'report_type'}, 
        '3': {'screen_name': 'pj_admin_reports', 'name': 'XPATH_ADMIN_PAYMENT_METHOD_REPORT', 'action': 'click', 'value': 'username_sign', 'skipflag': 'enabled'}, 
        '4': {'screen_name': 'pj_revenue_report', 'name': 'XPATH_OPERATOR_CLICK_SEARCH', 'action': 'new_tab', 'value': 'time_filter', 'cond_exec': 'enabled', 'skipflag': 'enabled'}, 'stepcount': 4},
        'kkkk': {
        '1': {'screen_name': 'pj_rate_paid_breakdown', 'name': 'XPATH_SRP_MONDAY', 'action': 'new_tab', 'value': 'time_filter1', 'cond_exec': 'enabled'}, 
        '2': {'screen_name': 'pj_admin_page', 'name': 'XPATH_ADMIN_SESSION_ENTRY', 'action': 'switch_frame', 'value': 'operator', 'skipflag': 'enabled'}, 
        '3': {'screen_name': 'pj_admin_page', 'name': 'XPATH_ADMIN_SESSION_ENTRY', 'action': 'new_tab', 'value': 'operator1', 'cond_exec': 'enabled'}, 'stepcount': 3}, 
        'mmmmm': {
        '1': {'screen_name': 'pj_landingpage', 'name': 'XPATH_ADMIN_SESSION_SAVE', 'action': 'switch_back', 'value': 'operator_1550', 'cond_exec': 'enabled', 'skipflag': 'enabled'}, 
        '3': {'screen_name': 'pj_rate_paid_breakdown', 'name': 'XPATH_SRP_TUESDAY', 'action': 'switch_frame', 'value': 'password_sign'}, 
        '2': {'screen_name': 'pj_admin_page', 'name': 'XPATH_ADMIN_SESSION_SAVE', 'action': 'switch_frame', 'value': 'username_sign', 'cond_exec': 'enabled'},
        '5': {'screen_name': 'pj_landingpage', 'name': 'XPATH_ADMIN_PROMO_AMOUNT', 'action': 'dropdown', 'value': 'admin_username', 'cond_exec': 'enabled', 'skipflag': 'enabled'},
        '4': {'screen_name': 'pj_admin_reports', 'name': 'XPATH_ADMIN_Frequency_Analysis_REPORT', 'action': 'switch_back', 'value': 'option', 'skipflag': 'enabled'}, 'stepcount': 5}}
        
        if steps in post_data.keys() :
           # steps1 = post_data[steps]
            steps1 = test
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
               # print(sorted_steps_dict)
                sorted_steps_dict[step_count] = stepCount
                print(sorted_steps_dict)
                stepArray[scNames] = sorted_steps_dict
        print('bbbbbbb')        
        print(stepArray)
        completeArray = {**scenarioArray, **stepArray}
        print(completeArray)


    #    pdata = str(post_data)
     #   print(pdata)
     #   kdata = pdata.replace("\'", "\"")
       # json_data = ast.literal_eval(json_data)
     #   print(kdata)
        
        with open("files/"+jsonName+".json", 'w') as file:
         #   mydata = json.loads(kdata)
         #   print(mydata)
            json.dump(post_data, file, indent=2)
            response_object = create_download_link("Download JSON file",jsonName+".json")
    return jsonify(response_object2)


@app.route('/jsonFile/<path:filename>', methods=['GET', 'POST'])
def download(filename): 
    directoryname = 'files'  
    return send_from_directory(directory=directoryname, filename=filename, as_attachment=True)

    stringtoExecute = './ios.sh '
    print(stringtoExecute)
 #   c = str(subprocess.call(shlex.split(stringtoExecute)))
  #  print(type(c))
    process = subprocess.Popen(shlex.split(stringtoExecute), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
           # print (output.strip())
            c = str(output.strip(), 'utf-8')
            print (c)
            print(type(c))
        # print(c)
            my_list = c.split(',')
            print(my_list)
            i=0
            while (i < len(my_list)) :
               # print (my_list[i])
                i=i+1
                txt = my_list[i]
              #  x = re.search("^iPhone.*\(", txt)
                start = ""
                end = "("
                # r = re.findall("start(.+?)end",html_page,re.MULTILINE)  # Old version
                r = re.match(re.escape(start) + "(.+?)" + re.escape(end), txt, re.DOTALL)  # New version
                print(r)
               # print (x)
    rc = process.poll()
   # return rc
    
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    print(client.version())
    print(devices)                                                   

if __name__ == '__main__':
    app.run(host="localhost",port=5001) 
