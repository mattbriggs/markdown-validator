'''
Module contains the classes for the rules.

- Rule class. This is a container to hold the attributes of a rule.

- Rules class. This contains a list of the rules.

'''

import markdownvalidator.mdhandler as HA
import markdownvalidator.mdparser as PA

class Rule():
    """Contains the attributes of a rule.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """

    def __init__(self):
        self.type = ""
        self.name = ""
        self.id = 0
        self.query = ""
        self.flag = ""
        self.operation = ""
        self.value = ""

class Validation():
    """A container class for validation responses.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """

    def __init__(self):
        self.id = 0
        self.name = ""
        self.state = ""
        self.value = ""
        self.path = ""

class Rules():
    """Contains a list of rules.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """

    def __init__(self):
        self.list_of_rules = []
        self.rules = {}
        self.checks = {}
        self.path = ""
        self.page = PA.MDPage()
        self.handler = HA.MDHandler()


    def load_object(self, type, indict):
        """With a dictionary of key values, load a Rule object, and add to the
        list_of_rules.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        rule = Rule()
        rule.type = type
        rule.name = indict["name"]
        rule.id = indict["id"]
        rule.query = indict["query"]
        rule.flag = indict["flag"]
        rule.operation = indict["operation"]
        rule.value = indict["value"]
        self.list_of_rules.append(indict["id"])
        self.rules[indict["id"]] = rule
        return 


    def load_rules(self, inputjson):
        """With a json object, load the rules list.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        for a in inputjson["rules"]["header"]:
            if a["id"] not in self.list_of_rules:
                self.load_object("header", a)
        for a in inputjson["rules"]["body"]:
            if a["id"] not in self.list_of_rules:
                self.load_object("body", a)


    def load_page(self, file_to_check):
        """With a filepath to a markdown page, load the page.

        :param file_to_check: File path to the a markdown file.
        :type file_to_check: String
        ...
        :raises General: Error getting file. Captures the exception.
        ...
        :return: Rule.path. File path to the a markdown file.
        :rtype: String
        :return: Rule.page. 
        :rtype: Page object
        """
        try:
            self.path = file_to_check
            self.page = self.handler.get_page(file_to_check)
        except Exception as e:
            print("Error getting file. {}".format(e))


    def process_rule(self, id):
        """With a rule object loaded with rules, a path to a markdown file, and 
        the rule id, run the rules and return a validaton object.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """

        if self.rules[id].type == "header":
            check_rule = self.handler.eval_ask(self.page.metadata, self.rules[id].query, self.rules[id].flag,
            self.rules[id].operation, self.rules[id].value)
        else:
            check_rule = self.handler.eval_list(self.page.html, self.rules[id].query, 
            self.rules[id].flag, self.rules[id].operation, self.rules[id].value)
        validation = Validation()
        validation.id = id
        validation.name = self.rules[id].name
        validation.state = check_rule
        validation.value = self.rules[id].value
        validation.path = self.path
        return validation


    def validate_rules(self, json_rules, file_to_check):
        """With rules and a file to check run all of the rules. Add the checks
        to the `checks` property of the `Rules` object.

        :param json_rules: A json object that contains valid rules.
        :type file_to_check: File path to the a markdown file.
        ...
        :raises ValueError: Duplicate rule ID in the JSON file.
        ...
        :return: None
        :rtype: None
        """
        self.load_rules(json_rules)
        self.load_page(file_to_check)
        for i in self.list_of_rules:
            validation = self.process_rule(i)
            try:
                self.checks[i] = validation
            except ValueError:
                print("Duplicate rule ID.")
                exit()
