'''
Classes for the runner.
- Box. This is a container to hold state and value for each action.
- Runner. This is the interacts wtih the workflow process to handle the filing
    retrieval of boxes.
'''

import mdhandler as HA
import mdrunner as RUN
import mdrules as RU

class Workflow():
    '''Class to process a workflow object.'''

    def __init__(self):
        self.actions = {
            "s" : s,
            "d" : d,
            "m" : m,
            "e" : e,
            "t" : t,
            "f" : f }

    def parse_steps(self, insteps):
        '''Take a raw set of steps and return as list of tuples.'''
        steps = insteps.split(",")
        workflow = []
        for i in steps:
            tup = tuple(i.split("->"))
            workflow.append(tup)

        return workflow


    def process_rule(self, rules, file_to_check, id):
        '''With a rule object loaded with rules, a path to a markdown file, and 
        the rule id, run the rules and return a validaton object.'''
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


    def run_workflow(self, workflow):
        '''Process a workflow. A workflow is a list of tuples. Returns a runner
        object.'''

        runner = RUN.Runner()
        runner.shelf_boxes(workflow)

        COUNT = 0

        for i in workflow:
            COUNT += 1
            a = None
            MESSAGE = ""

            source = self.make_proper(i[0])
            target =  self.make_proper(i[1])

            print("In-loop: {} | {} {} {}".format(COUNT, source, target, runner.d.state))

            if source == 't' and runner.d.state == True:
                runner.boxes[target] = self.actions[str(target)](runner.d)
                runner.d = runner.boxes[target]
                MESSAGE = runner.boxes[target].value
                print("T-TERM: {} | {} {} {}".format(COUNT, source, target, runner.d.state))
                continue

            elif source == 'f' and runner.d.state == False:
                runner.boxes[target] = self.actions[str(target)](runner.d)
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
                        runner.boxes[int(target)] = self.actions[str(target)](a)
                        MESSAGE = runner.boxes[int(target)].value
                    else:
                        runner.boxes[target] = self.actions[str(target)]()
                        MESSAGE = runner.boxes[int(target)].value

                except ValueError:
                    if target == 'd':
                        runner.d = self.actions[str(source)]()
                        MESSAGE = "Decision"

                    elif target == 'm':
                        runner.m.append(runner.boxes[source])
                        MESSAGE = "Merge"

                    elif target == 'e':
                        MESSAGE = "End"
            
            print("LOOP-TERM: {} | {} {} {}\n".format(COUNT, source, target, runner.d.state))

            runner.history += "Loop: {} | {} \n".format(COUNT, MESSAGE)
        
        return runner


    def create_rules(self, in_json):
        rules = {}
        for i in in_json["rules"]["header"]:
            rules[i["id"]] = i
        for i in in_json["rules"]["body"]:
            rules[i["id"]] = i
        return rules


    def run_rule_header(self, rule_json, file_to_check, runstate):
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


    def run_rule_body(self, rule_json, file_to_check, runstate):
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

    def make_proper(self, in_string):
        '''Take a string and return the right type of item.'''
        try:
            out_value = int(in_string)

        except ValueError:
            out_value = in_string.lower()

        return out_value

    def action(self, inbox=RUN.Box()):
        ''' '''
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Action 1. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def s(self, inbox=RUN.Box()):
        '''Start function.'''
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def d(self, inbox=RUN.Box()):
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def m(self, inbox=RUN.Box()):
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Merge. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def e(self, inbox=RUN.Box()):
        outbox = RUN.Box()
        outbox.state = False
        outbox.value = "End. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def t(self, inbox=RUN.Box()):
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "True. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def f(self, inbox=RUN.Box()):
        outbox = RUN.Box()
        outbox.state = False
        outbox.value = "False. Input: {}".format((inbox.state, inbox.value))
        return outbox