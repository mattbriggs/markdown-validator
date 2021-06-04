'''
6. The ms.date attribute reflects the current work.
7. Shall perform evaluations on dates.
'''

import datetime

t1 = "10/10/20"
t2 = "1/1/21"

a = datetime.datetime.strptime(t1, '%m/%d/%y')
b = datetime.datetime.strptime(t2, '%m/%d/%y')
now = datetime.datetime.now()

# subtract date 1 from date b to get difference
print(a-b)

# evaluate date 1 and date
print(a == b)

# get how long ago a time happened
print(now-a)