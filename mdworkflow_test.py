'''
Unit tests using pytest for mdworkflow.py.
'''

import json
import mdhandler as HA
import mdrunner as RUN
import mdrules as RU
import mdworkflow as WOR

import mdworkflow as WOR


def validate_with_rules(rule_json_file, markdown_file):
    '''With a json rule set and a markdown file produce validation results.'''
    with open(rule_json_file, 'r') as json_file:
        data = json.load(json_file)
    rules = RU.Rules()
    rules.validate_rules(data, markdown_file)
    return rules


def validate_with_workflows(rules, rule_json_file, workflow):
    '''With a json rule set and a markdown file produce validation results.'''
    with open(rule_json_file, 'r') as json_file:
        data = json.load(json_file)
    for i in data["workflows"]:
        workflow.run_workflow(rules, i["steps"])
    
    return workflow

rule_json_file = r"C:\git\mb\markdown-validator\testdata\checkworkflow.json"
markdown_file = r"C:\git\mb\markdown-validator\testdata\azure-stack-overview.md"
check_rules = validate_with_rules(rule_json_file, markdown_file)
check_workflows = WOR.Workflows()
check_workflows.load_flows(check_rules, rule_json_file)
check_workflows.validate_all_workflows()
# check_workflows.get_validation()

print(check_workflows.results[0])