def operate_contains(in_string, in_value):
    '''Evaluate if a string is contained in another string. Case sensitive.'''
    a_string = in_string.lower()
    b_string = in_value.lower().strip()
    if a_string.find(b_string) > 0:
        return True
    else:
        return False

a = " Tutorial - Deploy a Linux application in AKS on Azure Stack HCI"
b = "tutorial"

print(operate_contains(a, b))