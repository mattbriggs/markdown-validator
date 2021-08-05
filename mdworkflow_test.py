'''
Unit tests using pytest for mdworkflow.py.
'''

import json
import mdhandler as HA
import mdrunner as RUN
import mdrules as RU
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
test_workflow = WOR.Workflow()

print(check_workflows.results)

def test_workflow_is_number():
    assert True == test_workflow.is_number("1")

def test_workflow_check_truth():
    check_value = [True, True, True, False]
    assert False == test_workflow.check_truth(check_value)

def test_workflow_make_proper_string():
    assert "f" == test_workflow.make_proper("F")

def test_workflow_make_proper_int():
    assert 1 == test_workflow.make_proper("1")

def test_workflow_run_workflow():
    pass

def test_workflows_load_flows():
    workflows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    assert workflows == check_workflows.list_of_workflows


# def test_workflows_validate_all_workflows():
#     output = check_workflows.validate_all_workflows()
#     print(output)
#     evaluate = True
#     checkall = []
#     for i in check_workflows.list_of_workflows:
#         checkall.append(output[i])
#     if False in checkall:
#         evaluate = False
#     assert evaluate == True


def test_workflows_get_validation():
    output = check_workflows.get_validation()
    assert output[0]["result"] == True
