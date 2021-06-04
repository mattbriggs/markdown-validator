'''
First version to run with complex workflows.

5/7/2021
'''

import json
import sys
sys.path.insert(0, 'tools-development\common')
import mod_utilities as MU
import mdhandler as HA
import mdrunner as RUN
import mdrules as RU


def x_run_rules():
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
        check_rule = handler.eval_query(md_page.html, i['query'],  i['flag'], i['operation'], i['value'])
        if check_rule:
            print("Rule: {} Passed: {}".format(i["id"], check_rule))
        else:
            print("Rule: {} Passed: {}\n-->Fix: {}".format(i["id"], check_rule, i["mitigation"]))

    print("=======End=======")


def x_run_workflows(in_json, rule_json, file_to_check):
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


def parse_steps(insteps):
    '''Take a raw set of steps and return as list of tuples.'''
    steps = insteps.split(",")
    workflow = []
    for i in steps:
        tup = tuple(i.split("->"))
        workflow.append(tup)

    return workflow


def process_rule(rules, file_to_check, id):
    '''With a rule object loaded with rules, a path to a markdown file, and 
    the a rule id, run the rules and return a validaton object.'''
    handler = HA.MDHandler()
    md_page = handler.get_page(file_to_check)
    if rules.rules[id].type == "header":
        check_rule = handler.eval_ask(md_page.metadata, rules.rules[id].query, rules.rules[id].flag,
        rules.rules[id].operation,  rules.rules[id].value)
    else:
        check_rule = handler.eval_query(md_page.html, rules.rules[id].query, 
        rules.rules[id].flag, rules.rules[id].operation, rules.rules[id].value)
    validation = RU.Validation()
    validation.id = id
    validation.state = check_rule
    validation.value = rules.rules[id].value
    validation.mitigation = rules.rules[id].mitigation
    validation.path = file_to_check
    return validation


def run_workflow(workflow):
    '''Process a workflow. A workflow is a list of tuples. Returns a runner
    object.'''

    runner = RUN.Runner()
    runner.shelf_boxes(workflow)

    COUNT = 0

    for i in workflow:
        COUNT += 1
        a = None
        MESSAGE = ""

        source = make_proper(i[0])
        target =  make_proper(i[1])

        print("In-loop: {} | {} {} {}".format(COUNT, source, target, runner.d.state))

        if source == 't' and runner.d.state == True:
            runner.boxes[target] = actions[str(target)](runner.d)
            runner.d = runner.boxes[target]
            MESSAGE = runner.boxes[target].value
            print("T-TERM: {} | {} {} {}".format(COUNT, source, target, runner.d.state))
            continue

        elif source == 'f' and runner.d.state == False:
            runner.boxes[target] = actions[str(target)](runner.d)
            runner.d = runner.boxes[target]
            MESSAGE = runner.boxes[target].value
            print("f-TERM: {} | {} {} {}".format(COUNT, source, target, runner.d.state))
            continue

        elif target == None:
            pass

        else:
            print("Action: {} {}".format(target, runner.d.value ))
            try:
                a = runner.boxes[int(source)]
                MESSAGE = a.value

            except ValueError:
                if source == "s":
                    MESSAGE = "Start"

                elif source == "m":
                    runner.state = runner.reconcile()
                    MESSAGE = "Merge"
            try:
                if a:
                    runner.boxes[int(target)] = actions[str(target)](a)
                    MESSAGE = runner.boxes[int(target)].value
                else:
                    runner.boxes[target] = actions[str(target)]()
                    MESSAGE = runner.boxes[int(target)].value

            except ValueError:
                if target == 'd':
                    runner.d = actions[str(source)]()
                    MESSAGE = "Decision"

                elif target == 'm':
                    runner.m.append(runner.boxes[source])
                    MESSAGE = "Merge"

                elif target == 'e':
                    MESSAGE = "End"
        
        print("LOOP-TERM: {} | {} {} {}\n".format(COUNT, source, target, runner.d.state))

        runner.history += "Loop: {} | {} \n".format(COUNT, MESSAGE)
    
    return runner


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

def make_proper(in_string):
    '''Take a string and return the right type of item.'''
    try:
        out_value = int(in_string)

    except ValueError:
        out_value = in_string.lower()

    return out_value

def action(inbox=RUN.Box()):
    ''' '''
    outbox = RUN.Box()
    outbox.state = True
    outbox.value = "Action 1. Input: {}".format((inbox.state, inbox.value))
    return outbox

def s(inbox=RUN.Box()):
    '''Start function.'''
    outbox = RUN.Box()
    outbox.state = True
    outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
    return outbox

def d(inbox=RUN.Box()):
    outbox = RUN.Box()
    outbox.state = True
    outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
    return outbox

def m(inbox=RUN.Box()):
    outbox = RUN.Box()
    outbox.state = True
    outbox.value = "Merge. Input: {}".format((inbox.state, inbox.value))
    return outbox

def e(inbox=RUN.Box()):
    outbox = RUN.Box()
    outbox.state = False
    outbox.value = "End. Input: {}".format((inbox.state, inbox.value))
    return outbox

def t(inbox=RUN.Box()):
    outbox = RUN.Box()
    outbox.state = True
    outbox.value = "True. Input: {}".format((inbox.state, inbox.value))
    return outbox

def f(inbox=RUN.Box()):
    outbox = RUN.Box()
    outbox.state = False
    outbox.value = "False. Input: {}".format((inbox.state, inbox.value))
    return outbox

actions = { "s" : s,
            "d" : d,
            "m" : m,
            "e" : e,
            "t" : t,
            "f" : f
        }

# get_workflows()

file_to_check = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\testdata\azure-stack-overview.md"
therules = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\rules\conceptv3.json"
rules = RU.Rules()
rules.load_rules(therules)
print(rules.list_of_rules)

for i in rules.list_of_rules:
    check_this = process_rule(rules, file_to_check, str(i))
    print(check_this.state)