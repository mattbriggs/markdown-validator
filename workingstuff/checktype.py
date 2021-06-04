'''
Check datatype in metadata.

t = "10/10/20"
datetime.datetime.strptime(t, '%m/%d/%y')
'''

def check_date(instring):
    parts = instring.split("/")
    if len(parts) == 3:
        for i in parts:
            if len(i) > 2 or len(i) < 1:
                return False
            return True
    return False


def check_datatype(instring):
    '''With a string try to simply datatype and then check.'''
    try:
        int(instring)
        return "number"
    except ValueError:
        try:
            float(instring)
            return "float"
        except ValueError:
            if check_date(instring):
                return "date"
            else:
                return "string"

checkitems = ["1", "10/10/21", "dog", "1.234567"]
checkdate = ["10/10/21", "1/1/1", "903/10", "//2", "1/5/6"]

for i in checkdate:
    print("{} : {}".format(i, check_date(i)))

for i in checkitems:
    print(check_datatype(i))