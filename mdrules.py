'''
Classes for the rules.
- Rule. This is a container to hold the attributes of a rule.
- Rules. This contains a list of the rules.
'''

class Rule():
    '''Contains the attributes of a rule.'''

    def __init__(self):
        self.type = ""
        self.name = ""
        self.id = 0
        self.query = ""
        self.flag = ""
        self.operation = ""
        self.value = ""
        self.level = ""
        self.mitigation = ""


class Rules():
    '''Contains a list of rules.'''

    def __init__(self):
        self.list_of_rules = []
        self.rules = {}

    def load_object(self, type, indict):
        '''With a dictionary of key values, load a Rule object, and add to the
        list_of_rules.'''
        rule = Rule()
        rule.type = type
        rule.name = indict["name"]
        rule.id = indict["id"]
        rule.query = indict["query"]
        rule.flag = indict["flag"]
        rule.operation = indict["operation"]
        rule.value = indict["value"]
        rule.level = indict["level"]
        rule.mitigation = indict["mitigation"]
        self.list_of_rules.append(indict["id"])
        self.rules[indict["id"]] = rule
        return 

    def load_rules(self, inputjson):
        '''With a json object, load the rules list.'''
        for a in inputjson["rules"]["header"]:
            if a["id"] not in self.list_of_rules:
                self.load_object("header", a)
        for a in inputjson["rules"]["body"]:
            if a["id"] not in self.list_of_rules:
                self.load_object("body", a)

class Validation():
    '''A container class for validation responses.'''

    def __init__(self):
        self.id = 0
        self.state = ""
        self.value = ""
        self.mitigation = ""
        self.path = ""
        

class Checks():
    '''Contains a list of validation checks.'''

    def __init__(self):
        self.list_of_checks = []
        self.checks = {}


    def file_check(self, check):
        self.list_of_checks.append(check)
        index = len(self.list_of_checks)
        self.check[check.id] = index


    def get_check(self, index):
        return self.list_of_checks(self.checks[index])


    def load_check(self, indict):
        '''With a dictionary of key values, load a check object, and add to the
        list_of_checks.'''
        check = Validation()
        check.id = indict["id"]
        check.state = indict["state"]
        check.value = indict["value"]
        check.mitigation = indict["mitigation"]
        check.path = indict["path"]
        self.list_of_checks.append(check)
        self.file_check(check)


