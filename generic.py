''' CLI - App Name

    This command line app will ...
    Input: Path to an include file.
    Output: Displays validation.

    Matt Briggs V1.0.1: 11.24.2020
'''

import cmd
import sys
sys.path.insert(0, 'common')
import uuid
import pathlib
import json
from datetime import datetime
import mod_utilities as MU

APPVERSION = "\nApp Name CLI Version 1.0.0.20210101\n"

HELPTEXT = '''
This app has the following commands:
params : return the parameters passed in the cli.
quit : closes the cli
exit : closes the cli
'''

class TagTerminal(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = "> "

    def params(self, line):
        print("Passed the following paramaters:")
        for i in sys.argv:
            print(i)

    def do_help(self, line):
        '''Type help to get help for the application.'''
        print(HELPTEXT)
        return False

    def do_quit(self, line):
        '''Type quit to exit the application.'''
        return True

    def do_exit(self, line):
        '''Type exit to exit the application.'''
        return True

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    TagTerminal().cmdloop(APPVERSION)