'''
Run rules with a simple workflow.

5/1/2021
'''

import json
import sys
sys.path.insert(0, 'tools-development\common')
import mod_utilities as MU
import mdhandler as HA


def run_rules():
    '''procedure to run the rules'''

    print("=======Checking File=======\n")

    for i in my_check["rules"]["header"]:
        handler = HA.MDHandler()
        md_page = handler.get_page(file_to_check)
        check_rule = handler.eval_ask(md_page.metadata, i['query'], i['operation'], i['value'])
        if check_rule:
            print("Rule: {} Passed: {}".format(i["id"], check_rule))
        else:
            print("Rule: {} Passed: {}\n-->Fix: {}".format(i["id"], check_rule, i["mitigation"]))

    for i in my_check["rules"]["body"]:
        handler = HA.MDHandler()
        md_page = handler.get_page(file_to_check)
        check_rule = handler.eval_query(md_page .html, i['query'],  i['flag'], i['operation'], i['value'])
        if check_rule:
            print("Rule: {} Passed: {}".format(i["id"], check_rule))
        else:
            print("Rule: {} Passed: {}\n-->Fix: {}".format(i["id"], check_rule, i["mitigation"]))

    print("=======End=======")

def run_workflows(in_json, rule_json, file_to_check):
    '''procedure to run the workflows'''
    runstate = {"state" : "new", "pass" : False }
    for i in in_json["workflows"]:
        steps = i["steps"].split(";")
        for step in steps:
            if step:
                print("Workflow: {} Step: {}".format(i["name"],step))
                a_rule = rule_json[step]
                if i["type"] == "body":
                    runstate = run_rule_body(a_rule, file_to_check, runstate)
                elif i["type"] == "header":
                    runstate = run_rule_header(a_rule, file_to_check, runstate)
                else:
                    print("Need to specify rule.")
    runstate["state"] = "complete"
    return runstate

def create_rules(in_json):
    rules = {}
    for i in in_json["rules"]["header"]:
        rules[i["id"]] = i
    for i in in_json["rules"]["body"]:
        rules[i["id"]] = i
    return rules


def run_rule_header(rule_json, file_to_check, runstate):
    handler = HA.MDHandler()
    md_page = handler.get_page(file_to_check)
    check_rule = handler.eval_ask(md_page .html, rule_json['query'], rule_json['operation'], rule_json['value'])
    if check_rule:
        print("Rule: {} Passed: {}".format(rule_json["id"], check_rule))
        runstate["state"] = "running"
        runstate["pass"] = check_rule
    else:
        print("Rule: {} Passed: {}\n-->Fix: {}".format(rule_json["id"], check_rule, rule_json["mitigation"]))
        runstate["state"] = "running"
        runstate["pass"] = check_rule
        return runstate


def run_rule_body(rule_json, file_to_check, runstate):
    handler = HA.MDHandler()
    md_page = handler.get_page(file_to_check)
    check_rule = handler.eval_query(md_page .html, rule_json['query'],  rule_json['flag'], rule_json['operation'], rule_json['value'])
    if check_rule:
        print("Rule: {} Passed: {}".format(rule_json["id"], check_rule))
        runstate["state"] = "running"
        runstate["pass"] = check_rule
        return runstate
    else:
        print("Rule: {} Passed: {}\n-->Fix: {}".format(rule_json["id"], check_rule, rule_json["mitigation"]))
        runstate["state"] = "running"
        runstate["pass"] = check_rule
        return runstate

# variables

load_rules = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\rules\conceptv2.json"
rules_raw = MU.get_textfromfile(load_rules)
my_check=json.loads(rules_raw)
file_to_check = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\testdata\azure-stack-overview.md"

# execute

therules = create_rules(my_check)
job = run_workflows(my_check, therules, file_to_check)
print(job)
