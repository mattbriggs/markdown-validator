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

def validate_with_rules(rule_json_file, markdown_file):
    '''With a json rule set and a markdown file produce validation results.'''
    with open(rule_json_file, 'r') as json_file:
        data = json.load(json_file)
    rules = RU.Rules()
    rules.validate_rules(data, markdown_file)
    return rules


def validate_with_workflows(rules, rule_json_file):
    '''With a json rule set and a markdown file produce validation results.'''
    with open(rule_json_file, 'r') as json_file:
        data = json.load(json_file)
          
    for i in data["workflows"]:
        work = WOR.Workflow()
        run = work.run_workflow(rules, i["steps"])

        print(i["name"])
        print(run.state)
        print(i["level"])
        if run.state == False:
            print(i["fix"])
        print("=============\n")

# run validation

rule_json_file = r"C:\git\mb\markdown-validator\rules\conceptv4.json"
markdown_file = r"C:\git\ms\azure-docs-pr\articles\governance\policy\tutorials\create-and-manage.md"

# check rules and load the results

check = validate_with_rules(rule_json_file, markdown_file)

# print('''
# =============
# check rules
# =============
# ''')
# for i in check.list_of_rules:
#     print(check.checks[i].id)
#     print(check.checks[i].name)
#     print(check.checks[i].state)
#     print(check.checks[i].value)
#     print(check.checks[i].mitigation)
#     print("=============\n")

# run workflow

print('''
=============
check workflows
=============
''')

validate_with_workflows(check, rule_json_file)
