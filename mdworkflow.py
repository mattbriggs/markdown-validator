'''
Classes for the runner.
- Box. This is a container to hold state and value for each action.
- Runner. This is the interacts wtih the workflow process to handle the filing
    retrieval of boxes.
'''

import sys
import json
import mdrunner as RUN

class Workflow():
    """Class to process a workflow object.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """

    def __init__(self):
        self.state = "Created"

    def is_number(self, input):
        """[Summary]

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        try:
            int(input)
            return True
        except:
            return False


    def check_truth(self, in_list):
        """[Summary]

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        if False in in_list:
            return False
        else:
            return True


    def parse_steps(self, insteps):
        """Take a raw set of steps and return as list of tuples.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        if insteps.count("-") % 2 == 0:
            steps = insteps.split(",")
            workflow = []
            for i in steps:
                tup = tuple(i.split("-"))
                workflow.append(tup)

            return workflow
        else:
            print("Malformed workflow: {}".format(insteps))
            sys.exit()


    def make_proper(self, in_string):
        """Take a string and return the right type of item.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        try:
            out_value = int(in_string)

        except ValueError:
            out_value = in_string.lower()

        return out_value


    def run_workflow(self, rules, in_steps):
        """Process a rules and workflow steps. rules are a Rule object.
        A workflow is a list of tuples. Returns a runner
        object.

        :param rules: Processed rules.
        :type rules: Rules object.
        :param in_steps: A list of tuples referencing rules.
        :type in_steps: List
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """

        workflow = self.parse_steps(in_steps)

        runner = RUN.Runner()
        runner.shelf_boxes(workflow)

        state_workflow = None
        state_decision = None
        state_merge = None
        counter = 0

        for step in workflow:
            counter += 1

            source = self.make_proper(step[0])
            target = self.make_proper(step[1])

            # 1
            if source == "s" and self.is_number(target):
                state_workflow = rules.checks[str(target)].state

            # 2
            elif self.is_number(source) and target == "d":
                state_decision = rules.checks[str(source)].state
                state_merge = True

            # 3
            elif source == "m" and target == "d":
                state_workflow = state_decision
                state_merge = True
                state_decision = None

            # 4
            elif source == "t" and self.is_number(target) and state_decision == True:
                state_workflow = rules.checks[str(target)].state
                state_decision = None

            # 5
            elif source == "f" and self.is_number(target) and state_decision == False:
                state_workflow = rules.checks[str(target)].state
                state_decision = None

            # 6
            elif source == "t" and target == "r" and state_decision == True:
                state_decision = False

            # 7
            elif source == "f" and target == "r" and state_decision == False:
                state_decision = True

            # 8
            elif self.is_number(source) and target == "m" and state_merge == True:
                state_workflow = state_decision
                state_merge = None
                state_decision = None

            # 9
            elif source == "m" and self.is_number(target) and state_merge == None:
                state_workflow = state_decision
                state_merge = None
                state_decision = None

            # 10
            elif source == "m" and target == "e":
                state_workflow = state_decision
                state_merge = None
                state_decision = None
                # end

            # 11
            elif self.is_number(source) and target == "e":
                state_workflow = rules.checks[str(source)].state
                # end

            # 12
            elif self.is_number(source) and self.is_number(target):
                if rules.checks[str(source)].state == False:
                    state_workflow = False
                if rules.checks[str(target)].state == False:
                    state_workflow = False

        runner.state = state_workflow
        return runner

class Workflows():
    '''Class to process workflows'''

    def __init__(self):
        self.state = None
        self.summary = None
        self.list_of_workflows = []
        self.results = {}
        self.flows = {}
        self.fix = {}
        self.rules = None


    def load_flows(self, rules, rule_json_file):
        '''With rules and a rule_json_file extract the workflows.'''
        self.rules = rules
        with open(rule_json_file, 'r') as json_file:
            data = json.load(json_file)
        for ix, i in enumerate(data["workflows"]):
            self.list_of_workflows.append(ix)
            self.flows[ix] = i["steps"]
            self.fix[ix] = i["fix"]
        self.state = "Load"


    def validate_all_workflows(self):
        '''With loaded rules and worklows, add result validation objects.'''
        if self.state == "Load":
            self.summary = True
            for i in self.list_of_workflows:
                print(i)
                work = Workflow()
                result = work.run_workflow(self.rules, self.flows[i]).state
                print(result)
                self.results[i] = result
                if result == False:
                    self.summary = False
        else:
            return "Error. Must load flows."


    def get_validation(self):
        '''Retrieve the validation status.'''
        output = {}
        for inx, i in enumerate(self.list_of_workflows):
            record = {}
            record["result"] = self.results[i]
            record["fix"] = self.fix[i]
            output[inx] = record
        return output
