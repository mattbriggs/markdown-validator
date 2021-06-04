''' CLI - Markdown XPATH Builder CLI

    This command line app is used to develop the validation rules for
    content.

    Matt Briggs V2.0.0: 4.12.2021
'''

import cmd
import sys
import json
sys.path.insert(0, 'tools-development\common')
import mdhandler as HA

APPVERSION = "Markdown XPATH Builder CLI Version 1.0.0.20210412\n"
RULE = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\concept.json"
PAGE_HOLD = ""

HELPTEXT = '''
This app has the following commands:

json::
header <json payload> : This will return a rule using a JSON document format.
        {
            "name" : "check author",
            "id": "1",
            "query": "author",
            "flag" : "",
            "operation" : "==",
            "value" : "PatAltimore",
            "level": "Required",
            "mitigation": "You must have an author in your document."
        }
body  <json payload> : This will return a rule using a JSON document format.
        {
            "name" : "must-have-h1",
            "id": "2",
            "query": "/html/body/h1",
            "flag" : "count",
            "operation" : "==",
            "value" : "1",
            "level": "Required",
            "mitigation": "You must have one H1 in your document."
        }
load <markdown-path> : Will parse the markdown file at the path.
dump <flag>: Will print the raw markdown loaded by the parser.
    metadata: print the topic metadata
    html: print the topic html

xpath (HTML)::
query <markdown-path> <xpath> <flag>: Run an Xpath query on a markdown file.
     `count` flag gets the count of items.
     'text` flag gets content of the item.
eval  <markdown-path> <xpath> <flag> <operator> <value>: Evaluate the truth of the result of an xpath query.

     operators

     == equals
     [] contains.  Case sensitive.
     [: starts with. Case sensitive.
     :] end with. Case sensitive.

pos <markdown-path> <xpath> <flag> <operator>: Run an expath query with the
    flag = text and operator = p1. The second element of the p is an index of 
    the setence and will return a part-of-speech.

convert <markdown-path> <saved-path> : convert markdown to HTML.

metadata (JSON)::
get <markdown-path> <metadata key> : Get the value of a metadata key.
ask <markdown-path> <metadata tag> <flag> <operator> <value>: Evaluate the truth of a given metadata value.
extract <markdown-path> <saved-path> : convert metadata to JSON.

test::
params : return the parameters passed in the cli. (diagnostic.)

control::
quit : closes the cli
exit : closes the cli
'''
class TagTerminal(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = "> "

    # commands

    def do_convert(self, line):
        '''Convert a page into HTML and save to the target.'''
        convert = line.split(" ")
        try:
            handler = HA.MDHandler()
            md_page = handler.get_page(convert[0])
            print(handler.make_html(md_page.html, convert[1]))
        except:
            print("Error. See `help` for command syntax.")
        return False


    def do_extract(self, line):
        '''Get the metdata from the file.'''
        convert = line.split(" ")
        try:
            handler = HA.MDHandler()
            md_page = handler.get_page(convert[0])
            print(handler.make_json(md_page.metadata, convert[1]))
        except:
            print("Error. See `help` for command syntax.")
        return False


    def do_query(self, line):
        '''Take a markdown path and xpath query and return a result.'''
        convert = line.split(" ")
        handler = HA.MDHandler()
        md_page = handler.get_page(convert[0])
        print(handler.process_xpath(md_page.html, convert[1], convert[2]))
        return False


    def do_get(self, line):
        '''Take the line and get the metadata.'''
        convert = line.split(" ")
        handler = HA.MDHandler()
        md_page = handler.get_page(convert[0])
        print(handler.process_metadata(md_page.metadata, convert[1]))
        return False

    def do_eval(self, line):
        '''Take a markdown path, xpath query, flag, operand, value and return a result.'''
        convert = line.replace("  ", " ").split(" ")
        try:
            eval_string = ""
            if len(convert) > 1:
                for inx, i in enumerate(convert):
                    if inx > 3:
                        eval_string += " " + i
            clear_string = eval_string.strip()
            handler = HA.MDHandler()
            md_page = handler.get_page(convert[0])
            print(handler.eval_query(md_page.html, convert[1], convert[2], convert[3], clear_string))
        except:
            print("Error. See `help` for command syntax.")
        return False

    def do_pos(self, line):
        '''Take a markdown path, xpath query, flag, operator.'''
        convert = line.replace("  ", " ").split(" ")
        try:
            eval_string = ""
            if len(convert) > 1:
                for inx, i in enumerate(convert):
                    if inx > 2:
                        eval_string += " " + i
            clear_string = eval_string.strip()
            handler = HA.MDHandler()
            md_page = handler.get_page(convert[0])
            print(handler.get_part_of_speech(md_page.html, convert[1], convert[2], clear_string))
        except:
            print("Error. See `help` for command syntax.")
        return False

    def do_ask(self, line):
        '''With the markdown path, keyword, flag, operator, and a value, produce true/false.'''
        convert = line.replace("  ", " ").split(" ")
        try:
            eval_string = ""
            if len(convert) > 1:
                for inx, i in enumerate(convert):
                    if inx > 3:
                        eval_string += " " + i
            clear_string = eval_string.strip()
            handler = HA.MDHandler()
            md_page = handler.get_page(convert[0])
            print(handler.eval_ask(md_page.metadata, convert[1], convert[2], convert[3], clear_string))


        except:
            print("Error. See `help` for command syntax.")
        return False

    def do_load(self,line):
        '''Take a URL and parse the page.'''
        global PAGE_HOLD
        convert = line.split(" ")
        handler = HA.MDHandler()
        PAGE_HOLD = handler.get_page(convert[0])
        return False


    def do_dump(self, line):
        '''Dump the raw of a page object held in the global variable.'''
        convert = line.split(" ")
        if convert[0] == "metadata":
            print(PAGE_HOLD.metadata)
        elif convert[0] == "html":
            print(PAGE_HOLD.html)
        else:
            print(PAGE_HOLD.raw)


    def do_header(self, line):
        '''header <markdown-path> <json payload>: This will return a rule using a JSON document format.
        { "name" : "check-author", "id": "1", "query": "author", "flag" : "", "operation" : "==", 
        "value" : "PatAltimore", "level": "Required", "mitigation": "You must have an author 
        in your document." }'''
        payload = json.loads(line.strip())
        try:
            handler = HA.MDHandler()
            print(handler.eval_ask(PAGE_HOLD.metadata, payload['query'], payload["flag"], payload['operation'], payload['value']))
        except Exception as e:
            print(e)
        return False


    def do_body(self, line):
        '''body <markdown-path> <json payload>: This will return a rule using a JSON document format.
        { "name" : "must-have-h1", "id": "2", "query": "/html/body/h1", "flag" : "count", 
        "operation" : "==", "value" : "1", "level": "Required", 
        "mitigation": "You must have one H1 in your document." }'''
        payload = json.loads(line.strip())
        try:
            handler = HA.MDHandler()
            print(handler.eval_query(PAGE_HOLD.html, payload['query'],  payload['flag'], payload['operation'],
            payload['value']))
        except Exception as e:
            print(e)
        return False


    def do_params(self, line):
        '''Function to see the input from the paramater line. Returns the param list.'''
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
        '''Exit.'''
        return True


if __name__ == '__main__':
    TagTerminal().cmdloop(APPVERSION)
