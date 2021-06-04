'''
Workflow for v3. of the validator. This version works with parsing the workflow
description in JSON. It is modeled using a simple decision.

Used to develop my workflow handler.

5.7.2021
'''

# these actions require the class Runner has been instantieted as runner.

class Box():
    '''Box holds the values from execution.'''

    def __init__(self):
        self.state = None
        self.value = None

class Runner():
    '''Runner executed a workflow'''

    def __init__(self):
        self.state = True
        self.value = None
        self.d = Box()
        self.m = []
        self.history = ""
        self.list_of_boxes = []
        self.boxes = {}


    def shelf_boxes(self, workflow):
        '''Take a valid workflow and create containers for each process
        indexed by the box key.'''
        for i in workflow:
            for box in i:
                try:
                    a = int(box)
                    if a not in self.list_of_boxes:
                        box = Box()
                        self.list_of_boxes.append(a)
                        self.boxes[a] = box
                except ValueError:
                    pass

    def reconcile(self):
        '''Update the state based on the list of items in the merg list.'''
        truthiness = []
        if self.m:
            for i in self.m:
                truthiness.append(i.state)
            return len(truthiness) == sum(truthiness)
        return False


def make_proper(in_string):
    '''Take a string and return the right type of item.'''
    try:
        out_value = int(in_string)

    except ValueError:
        out_value = in_string.lower()

    return out_value

def action1(inbox=Box()):
    ''' '''
    outbox = Box()
    outbox.state = True
    outbox.value = "Action 1. Input: {}".format((inbox.state, inbox.value))
    return outbox

def action2(inbox=Box()):
    ''' '''
    outbox = Box()
    outbox.state = True
    outbox.value = "Action 2. Input: {}".format((inbox.state, inbox.value))
    return outbox

def action3(inbox=Box()):
    ''' '''
    outbox = Box()
    outbox.state = True
    outbox.value = "Action 3. Input: {}".format((inbox.state, inbox.value))
    return outbox

def action4(inbox=Box()):
    ''' '''
    outbox = Box()
    outbox.state = True
    outbox.value = "Action 4. Input: {}".format((inbox.state, inbox.value))
    return outbox

def s(inbox=Box()):
    '''Start function.'''
    outbox = Box()
    outbox.state = True
    outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
    return outbox

def d(inbox=Box()):
    outbox = Box()
    outbox.state = True
    outbox.value = "Start. Input: {}".format((inbox.state, inbox.value))
    return outbox

def m(inbox=Box()):
    outbox = Box()
    outbox.state = True
    outbox.value = "Merge. Input: {}".format((inbox.state, inbox.value))
    return outbox

def e(inbox=Box()):
    outbox = Box()
    outbox.state = False
    outbox.value = "End. Input: {}".format((inbox.state, inbox.value))
    runner.state = False
    return outbox

def t(inbox=Box()):
    outbox = Box()
    outbox.state = True
    outbox.value = "True. Input: {}".format((inbox.state, inbox.value))
    return outbox

def f(inbox=Box()):
    outbox = Box()
    outbox.state = False
    outbox.value = "False. Input: {}".format((inbox.state, inbox.value))
    return outbox

actions = { "s" : s,
            "d" : d,
            "m" : m,
            "e" : e,
            "t" : t,
            "f" : f,
            "1" : action1,
            "2" : action2,
            "3" : action3,
            "4" : action4
        }


def test_workflow():

    COUNT = 0

    for i in workflow:
        COUNT += 1
        a = None
        MESSAGE = ""

        source = make_proper(i[0])
        target =  make_proper(i[1])

        print("In-loop: {} | {} {} {}".format(COUNT, source, target, runner.d.state))

        if source == 't' and runner.d.state == True:
            runner.boxes[target] = actions[str(target)](runner.d)
            runner.d = runner.boxes[target]
            MESSAGE = runner.boxes[target].value
            print("T-TERM: {} | {} {} {}".format(COUNT, source, target, runner.d.state))
            continue

        elif source == 'f' and runner.d.state == False:
            runner.boxes[target] = actions[str(target)](runner.d)
            runner.d = runner.boxes[target]
            MESSAGE = runner.boxes[target].value
            print("f-TERM: {} | {} {} {}".format(COUNT, source, target, runner.d.state))
            continue

        elif target == None:
            pass

        else:
            print("Action: {} {}".format(target, runner.d.value ))
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
                    runner.boxes[int(target)] = actions[str(target)](a)
                    MESSAGE = runner.boxes[int(target)].value
                else:
                    runner.boxes[target] = actions[str(target)]()
                    MESSAGE = runner.boxes[int(target)].value

            except ValueError:
                if target == 'd':
                    runner.d = actions[str(source)]()
                    MESSAGE = "Decision"

                elif target == 'm':
                    runner.m.append(runner.boxes[source])
                    MESSAGE = "Merge"

                elif target == 'e':
                    MESSAGE = "End"
        
        print("LOOP-TERM: {} | {} {} {}\n".format(COUNT, source, target, runner.d.state))

        runner.history += "Loop: {} | {} \n".format(COUNT, MESSAGE)

workflow = [("S","1"),("1","D"),("T","2"),("F","3"),("2","M"),("3","M"),("M","E")]

runner = Runner()
runner.shelf_boxes(workflow)
test_workflow()
print(runner.history)