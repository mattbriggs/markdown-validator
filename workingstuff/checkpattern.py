'''
Check if a pattern is contained in a string.
'''

import re

def check_pattern(pattern, instring):
    '''Check if a pattern is contained in a string.'''
    return bool(re.match(pattern, instring))

pat1 = "hello[0-9]+"
str1 = "hello1"

print(check_pattern(pat1, str1))