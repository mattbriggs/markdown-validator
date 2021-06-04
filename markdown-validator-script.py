'''
First version to run with complex workflows.

5/7/2021
'''

import json
import mdhandler as HA
import mdrunner as RUN
import mdrules as RU




# get_workflows()

print("Test rule 2021.6.4\n")
#file_to_check = r"C:\git\ms\azure-stack-docs-pr\azure-stack\aks-hci\deploy-linux-application.md"
#file_to_check = input('File to check > ')

# load rules
with open(r"C:\git\mb\markdown-validator\rules\conceptv4.json", 'r') as json_file:
  data = json.load(json_file)

rules = RU.Rules()
rules.load_rules(data)
print("Inventory of rules:  ")
print(rules.list_of_rules)

for i in data["workflows"]:
    print(i["name"])
    run = run_workflow(i["steps"])
    print(" State: {},  Value: {}, \n    Run history: {}\n\n".format(run.state, run.value, run.history))