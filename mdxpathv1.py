''' CLI - Markdown XPATH Builder CLI

    This command line app is used to develop the validation rules for
    content.

    Matt Briggs V1.0.1: 4.6.2021
'''

import cmd
import sys
sys.path.insert(0, 'tools-development\common')
import uuid
import pathlib
import json
from datetime import datetime
from lxml import etree
import markdown
import mod_utilities as MU

APPVERSION = "\Markdown XPATH Builder CLI Version 1.0.0.20210406\n"
RULE = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\rules.json"

HELPTEXT = '''
This app has the following commands:

check <markdown-path> <xpath> <evaluate> : Evaluate the truth of an xpath query.
eval  <markdown-path> <xpath> <operator> <value>: Evaluate the truth of the result of an xpath query.
query <markdown-path> <xpath> : Run an Xpath query on a markdown file.
convert <markdown-path> <saved-path> : convert markdown to HTML.
params : return the parameters passed in the cli.
quit : closes the cli
exit : closes the cli
'''

#logic

def process_xpath(inrawbody, query, in_value):
    '''With raw markdown file and docs metadata block, turn just the body as the indicated 
    format, html, text, or markown'''
    try:
        body = MU.get_textfromMD(inrawbody)
        html_doc = markdown.markdown(body)
        htmlparser = etree.HTMLParser()
        tree = etree.fromstring(html_doc, htmlparser)
        result_raw = tree.xpath(query)
        if len(result_raw) == 1:
            if str(in_value) == str(1):
                return 1
            else:
                return result_raw[0].text
        else:
            return len(result_raw)
    except Exception as e:
        return ("Failed to query file.\n{}".format(e))


def operate_equal(in_string, in_value):
    '''Evaluate if the two strings are equal.'''
    if str(in_string).strip() == str(in_value).strip():
        return True
    else:
        return False


def operate_greater(in_string, in_value):
    '''Evaluate if the result is greater than the value.'''
    if str(in_string).strip() > str(in_value).strip():
        return True
    else:
        return False


def operate_less(in_string, in_value):
    '''Evaluate if the result is less than the value.'''
    if str(in_string).strip() < str(in_value).strip():
        return True
    else:
        return False


def operate_not(in_string, in_value):
    '''Evaluate if the two strings aren't equal.'''
    if str(in_string).strip() != str(in_value).strip():
        return True
    else:
        return False


def eval_query(in_string, query, operator, in_value):
    '''With the result of an xpath, the operator token, and a value, produce true/false'''
    try:
        result = process_xpath(in_string, query, in_value)
        if operator == "==":
            return operate_equal(result, in_value)
        elif operator == ">":
            return operate_greater(result, in_value)
        elif operator == "<":
            return operate_less(result, in_value)
        elif operator == "!=":
            return operate_not(result, in_value)
        else:
            return False
    except:
        return False


def process_check(inrawbody, query, evaluate):
    '''With raw markdown file and docs metadata block, turn just the body as the indicated 
    format, html, text, or markown'''
    try:
        result = process_xpath(inrawbody, query, evaluate)
        if result == evaluate:
            return True
        else:
            return False
    except Exception as e:
        return ("Failed to query file.\n{}".format(e))


def make_html(inrawbody, target):
    '''Make HTML (this is will be depracted)'''
    try:
        body = MU.get_textfromMD(inrawbody)
        html_doc = markdown.markdown(body)
        MU.write_text(html_doc, target)
        return "Saving file to: {}".format(target)
    except:
        return ("Failed to create and save file.")


def get_rules(RULE):
    '''Get the stem and path and create the a dictionary of stems to paths.'''
    schema_dict = {}
    schema_dict[RULE] = i
    return schema_dict

class TagTerminal(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = "> "

    # commands

    def do_convert(self, line):
        ''' '''
        convert = line.split(" ")
        try:
            print(make_html(convert[0], convert[1]))
        except:
            print("Error. See `help` for command syntax.")
        return False


    def do_query(self, line):
        '''Take a markdown path and xpath query and return a result.'''
        convert = line.split(" ")
        print(process_xpath(convert[0], convert[1], ""))
        return False


    def do_eval(self, line):
        '''Take a markdown path, xpath query, operand, value and return a result.'''
        convert = line.replace("  ", " ").split(" ")
        try:
            eval_string = ""
            if len(convert) > 1:
                for inx, i in enumerate(convert):
                    if inx > 2:
                        eval_string += " " + i
            clear_string = eval_string.strip()
            print(eval_query(convert[0], convert[1], convert[2], clear_string))
        except:
            print("Error. See `help` for command syntax.")
        return False


    def do_check(self, line):
        '''Take a markdown path and xpath query, and value and return a result.'''
        convert = line.split(" ")
        try:
            eval_string = ""
            if len(convert) > 1:
                for inx, i in enumerate(convert):
                    if inx > 1:
                        eval_string += " " + i
            clear_string = eval_string.strip()
            print(process_check(convert[0], convert[1], clear_string))
        except:
            print("Error. See `help` for command syntax.")
        return False


    def do_params(self, line):
        print("Passed the following paramaters:")
        for i in sys.argv:
            print(i)
        return False

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