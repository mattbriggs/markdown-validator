'''
Classes for the runner.
- Box. This is a container to hold state and value for each action.
- Runner. This is the interacts wtih the workflow process to handle the filing
    retrieval of boxes.
'''

import json
import mdrunner as RUN
import mdrules as RUL

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
            exit()


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

        workflow_states = []
        decision = None
        dec_flag = False
        merge = False
        counter = 0

        for step in workflow:
            counter += 1

            source = self.make_proper(step[0])
            target = self.make_proper(step[1])

            if self.is_number(source) and target == "d":
                decision = rules.checks[str(source)].state
                dec_flag = True
            elif source == "t" and dec_flag == True:
                if decision == True:
                    decision = rules.checks[str(target)].state
                    dec_flag = False
            elif source == "f" and dec_flag == True:
                if decision == False:
                    decision = rules.checks[str(target)].state
                    dec_flag = False
            elif self.is_number(source) and target == "m":
                if merge == False:
                    workflow_states.append(decision)
                    decision = None
                    merge = True
                else:
                    merge = False
            elif self.is_number(source) and target != "m":
                workflow_states.append(rules.checks[str(source)].state)

        workflow_state = self.check_truth(workflow_states)
        runner.state = workflow_state
        return runner

class Workflows():
    '''Class to process workflows'''

    def __init__(self):
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


    def validate_all_workflows(self):
        '''With loaded rules and worklows, add result validation objects.'''
        for i in self.list_of_workflows:
            work = Workflow()
            work.run_workflow(self.rules, self.flows[i])
        print(self.results)
        return(self.results)


    def get_validation(self):
        '''Retrieve the validation status.'''
        output = {}
        for inx, i in enumerate(self.list_of_workflows):
            record = {}
            record["result"] = self.results[i]
            record["fix"] = self.fix[i]
            output[inx] = record
        return output
