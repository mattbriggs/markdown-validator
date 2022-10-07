'''
Get a percentage of the topic that has numbered lines.
'''

import re
import mod_utilities as MU

class CountNoLines:
    def __init__(self):
        self.state = ""

    def tally(self, filein):
        ''' '''
        file = MU.get_textfromfile(filein)
        file_lines = file.split("\n")
        totalno = len(file_lines)
        tally = 0
        for i in file_lines:
            leftadjust = i.lstrip()
            if re.match("^[0-9]", leftadjust):
                tally += 1
        perc = tally/totalno
        print("Count: {}/{} = {}".format(tally, totalno, perc))
        return perc