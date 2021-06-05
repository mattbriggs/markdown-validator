'''
Classes for the runner.
- Box. This is a container to hold state and value for each action.
- Runner. This is the interacts wtih the workflow process to handle the filing
    retrieval of boxes.
'''

import mdrunner as RUN

class Workflow():
    '''Class to process a workflow object.'''

    def __init__(self):
        self.actions = {
        "s" : self.s,
        "d" : self.d,
        "m" : self.m,
        "e" : self.e,
        "t" : self.t,
        "f" : self.f }

    def is_number(self, input):
        try:
            int(input)
            return True
        except:
            return False


    def check_truth(self, in_list):
        for i in in_list:
            if i == False:
                return False
            else:
                return True


    def parse_steps(self, insteps):
        '''Take a raw set of steps and return as list of tuples.'''
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
        '''Take a string and return the right type of item.'''
        try:
            out_value = int(in_string)

        except ValueError:
            out_value = in_string.lower()

        return out_value


    def run_workflow(self, rules, in_steps):
        '''Process a rules and workflow steps. rules are a Rule object. 
        A workflow is a list of tuples. Returns a runner
        object.'''

        values = rules.checks # dictionary
        workflow = self.process_steps(in_steps)

        runner = RUN.Runner()
        runner.shelf_boxes(workflow)

        for workflow in workflows:
            workflow_states = []
            decision = None
            dec_flag = False
            merge = False
            counter = 0

            for step in workflow:
                counter += 1

                source = step[0] # source = self.make_proper(i[0])
                target = step[1] # target = self.make_proper(i[1])

                if self.is_number(source) and target == "d":
                    decision = values[source].state
                    dec_flag = True
                elif self.source == "t" and dec_flag == True:
                    if decision == True:
                        decision = values[target].state
                        dec_flag = False
                elif source == "f" and dec_flag == True:
                    if decision == False:
                        decision = values[target].state
                        dec_flag = False
                elif self.is_number(source) and target == "m":
                    if merge == False:
                        workflow_states.append(decision)
                        decision = None
                        merge = True
                    else:
                        merge = False
                elif self.is_number(source) and target != "m":
                    workflow_states.append(values[source].state)
        
        return runner