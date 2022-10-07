'''
The scanner returns a score 

6/5/2021
'''

import json
import mdhandler as HA
import mdrunner as RUN
import mdrules as RU
import mdworkflow as WOR


# develop functions

class MDScanner():
    ''' '''
    def __init__(self):
        self.state = "new"

    def validate_with_rules(self, rule_json_file, markdown_file):
        '''With a json rule set and a markdown file produce validation results.'''
        validation = {}
        validation["file"] = markdown_file
        validation["score"] = 0
        validation["checks"] = {}
        with open(rule_json_file, 'r') as json_file:
            rules_json = json.load(json_file)
        rull = RU.Rules()
        rull.validate_rules(rules_json, markdown_file)
        for i in rull.list_of_rules:
            if rull.checks[i].state == True:
                validation["score"] += 1
        for i in rull.list_of_rules:
            check = {}
            check["id"] = rull.checks[i].id
            check["name"] = rull.checks[i].name
            check["state"] = rull.checks[i].state
            check["value"] = rull.checks[i].value
            validation["checks"][check["id"]] = check
        return validation
