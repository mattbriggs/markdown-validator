'''
Classes for the runner.
- Box. This is a container to hold state and value for each action.
- Runner. This is the interacts wtih the workflow process to handle the filing
    retrieval of boxes.
'''

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


