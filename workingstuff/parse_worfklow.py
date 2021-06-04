
def parse_steps(insteps):
    '''Take a raw set of steps and return as list of tuples.'''
    steps = insteps.split(",")
    workflow = []
    for i in steps:
        tup = tuple(i.split("->"))
        workflow.append(tup)

    return workflow

testit = "S->1,1->D,T->2,F->3,2->M,3->M,M->E"
print(parse_steps(testit))
