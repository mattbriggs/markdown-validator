'''
Simplist check of a validation.

4/16/2021

'''


import json
import sys
sys.path.insert(0, 'tools-development\common')
import mod_utilities as MU
import mdxpathv1 as MDX

rules = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\rules\conceptv1.json"
rules_raw = MU.get_textfromMD(rules)
my_check=json.loads(rules_raw)
file_to_check = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\validtemplates\concept.md"

print("=======Checking File=======\n")

for i in my_check:
    check_rule = MDX.eval_query(file_to_check, i["Rule"], i["Operation"], i["Value"])
    if check_rule:
        print("Rule: {} Passed: {}".format(i["ID"], check_rule))
    else:
        print("Rule: {} Passed: {}\n-->Fix: {}".format(i["ID"], check_rule, i["Mitigation"]))
print("=======End=======")