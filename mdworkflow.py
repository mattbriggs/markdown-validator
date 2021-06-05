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

    # actions
    def action(self, checks, inbox=RUN.Box()):
        '''Action node. Processes a rule.'''
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Action. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def s(self, checks, inbox=RUN.Box()):
        '''Start node. Initiates the workflow.'''
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def d(self, checks, inbox=RUN.Box()):
        '''Decision node. Results in a true or false condition.'''
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def m(self, checks, inbox=RUN.Box()):
        '''Merge node. Collects branched control flows.'''
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "Merge. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def e(self, checks, inbox=RUN.Box()):
        '''End node. Terminates the workflow.'''
        outbox = RUN.Box()
        outbox.state = False
        outbox.value = "End. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def t(self, checks, inbox=RUN.Box()):
        '''Truth node. Connects to a true condition from the `d' node.'''
        outbox = RUN.Box()
        outbox.state = True
        outbox.value = "True. Input: {}".format((inbox.state, inbox.value))
        return outbox

    def f(self, checks, inbox=RUN.Box()):
        '''False node. Connects to a false condition from the `d' node.'''
        outbox = RUN.Box()
        outbox.state = False
        outbox.value = "False. Input: {}".format((inbox.state, inbox.value))
        return outbox


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

        checks = rules.checks # dictionary
        workflow = self.process_steps(in_steps)

        runner = RUN.Runner()
        runner.shelf_boxes(workflow)

        COUNT = 0

        #iterates over the list of tuples for the workflow
        for i in workflow:
            COUNT += 1
            a = None
            MESSAGE = ""

            source = self.make_proper(i[0])
            target = self.make_proper(i[1])

            print("In-loop: {} | source {} target {} state {}".format(COUNT, source, target, runner.d.state))

            if source == 't' and runner.d.state == True:
                runner.boxes[target] = self.actions[str(target)](checks, runner.d)
                runner.d = runner.boxes[target]
                MESSAGE = runner.boxes[target].value
                print("T-TERM: {} | {} {} {}".format(COUNT, source, target, runner.d.state))
                continue

            elif source == 'f' and runner.d.state == False:
                runner.boxes[target] = self.actions[str(target)](checks, runner.d)
                runner.d = runner.boxes[target]
                MESSAGE = runner.boxes[target].value
                print("f-TERM: {} | {} {} {}".format(COUNT, source, target, runner.d.state))
                continue

            else:
                try:
                    a = runner.boxes[int(source)]
                    MESSAGE = a.value

                except ValueError:
                    if source == "s":
                        MESSAGE = "Start"

                    elif source == "m":
                        runner.state = runner.reconcile()
                        MESSAGE = "Merge"
                try:
                    if a:
                        # run the target action
                        runner.boxes[int(target)] = self.actions["action"](checks, 
                        MESSAGE = runner.boxes[int(target)].value
                    else:
                        runner.boxes[target] = self.actions[str(target)](checks)
                        MESSAGE = runner.boxes[int(target)].value

                except ValueError:
                    if target == 'd':
                        runner.d = self.actions[str(source)](checks)
                        MESSAGE = "Decision"

                    elif target == 'm':
                        runner.m.append(runner.boxes[source])
                        MESSAGE = "Merge"

                    elif target == 'e':
                        MESSAGE = "End"
            
            print("LOOP-TERM: {} | {} {} {}\n".format(COUNT, source, target, runner.d.state))

            runner.history += "Loop: {} | {} \n".format(COUNT, MESSAGE)
        
        return runner