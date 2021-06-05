'''
First version to run with complex workflows.

6/5/2021
'''

import json
import mdhandler as HA
import mdrunner as RUN
import mdrules as RU
import mdworkflow as WOR


# develop functions

def check_the_file(rule_json_file, markdown_file):
    '''With a json rule set and a markdown file produce validation results.'''
    with open(rule_json_file, 'r') as json_file:
        data = json.load(json_file)
    rules = RU.Rules()
    rules.validate_file(data, markdown_file)
    return rules

    # for i in data["workflows"]:
    #   work = WOR.Workflow()
    #   run = work.run_workflow( rules, i["steps"])
    #   print(" State: {},  Value: {}, \n    Run history: {}\n\n".format(run.state, run.value, run.history))

# run validation

rule_json_file = r"C:\git\mb\markdown-validator\rules\conceptv4.json"
markdown_file = r"C:\git\ms\azure-stack-docs-pr\azure-stack\aks-hci\deploy-linux-application.md"

# check rules

check = check_the_file(rule_json_file, markdown_file)

for i in check.list_of_rules:
    print(check.checks[i].id)
    print(check.checks[i].name)
    print(check.checks[i].state)
    print(check.checks[i].value)
    print(check.checks[i].mitigation)
    print("=============\n")

# run workflow