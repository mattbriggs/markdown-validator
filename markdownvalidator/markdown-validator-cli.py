''' Markdown Validator Command Line Interface Tool

    This command line app is used to develop the validation rules for
    content.

    Matt Briggs V2.0.0: 6.4.2021
'''

import sys
import cmd
import json
import markdownvalidator.mod_utilities as MU
import markdownvalidator.mdhandler as HA

APPVERSION = "Markdown Validator Command Line Interface Tool Version 1.0.0.20210604\n"
PAGE_HOLD = ""

HELPTEXT = MU.get_textfromfile(r'C:\git\mb\markdown-validator\markdown-validator-cli-help.txt')

class TagTerminal(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = "> "

    # commands

    def do_convert(self, line):
        """Convert a page into HTML and save to the target.

        :param line: [filepath], defaults to empty.
        :type filepath: [filepath](required)
        ...
        :raises Error: Catches all errors and displays the error string in the
        terminal.
        ...
        :return: Prints the page as rendered HTML in the terminal.
        :rtype: text, HTML.
        """
        convert = line.split(" ")
        try:
            handler = HA.MDHandler()
            md_page = handler.get_page(convert[0])
            print(handler.make_html(md_page.html, convert[1]))
        except:
            print("Error. See `help` for command syntax.")
        return False


    def do_extract(self, line):
        """ Get the metdata from the file.'''

        :param line: [filepath], defaults to empty.
        :type filepath: [filepath](required)
        ...
        :raises Error: Catches all errors and displays the error string in the
        terminal.
        ...
        :return: Prints the metdata as JSON in the terminal.
        :rtype: text, JSON
        """

        convert = line.split(" ")
        try:
            handler = HA.MDHandler()
            md_page = handler.get_page(convert[0])
            print(handler.make_json(md_page.metadata, convert[1]))
        except:
            print("Error. See `help` for command syntax.")
        return False


    def do_query(self, line):
        """Take a markdown path and xpath query and return a result.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        convert = line.split(" ")
        handler = HA.MDHandler()
        md_page = handler.get_page(convert[0])
        print(handler.process_xpath(md_page.html, convert[1], convert[2]))
        return False


    def do_get(self, line):
        """Take the line and get the metadata.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        convert = line.split(" ")
        handler = HA.MDHandler()
        md_page = handler.get_page(convert[0])
        print(handler.process_metadata(md_page.metadata, convert[1]))
        return False


    def do_eval(self, line):
        """Take a markdown path, xpath query, flag, operand, value and return a result.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
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
            print(handler.eval_list(md_page.html, convert[1], convert[2], convert[3], clear_string))
        except:
            print("Error. See `help` for command syntax.")
        return False

    def do_pos(self, line):
        """Take a markdown path, xpath query, flag, operator.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
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
        """With the markdown path, keyword, flag, operator, and a value, produce true/false.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
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
        """Take a URL and parse the page.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        global PAGE_HOLD
        convert = line.split(" ")
        handler = HA.MDHandler()
        PAGE_HOLD = handler.get_page(convert[0])
        return False


    def do_dump(self, line):
        """Dump the raw of a page object held in the global variable.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        convert = line.split(" ")
        if convert[0] == "metadata":
            print(PAGE_HOLD.metadata)
        elif convert[0] == "html":
            print(PAGE_HOLD.html)
        else:
            print(PAGE_HOLD.raw)


    def do_header(self, line):
        """header <markdown-path> <json payload>: This will return a rule using a JSON document format.
        { "name" : "check-author", "id": "1", "query": "author", "flag" : "", "operation" : "==", 
        "value" : "PatAltimore", "level": "Required", "mitigation": "You must have an author 
        in your document." }

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        payload = json.loads(line.strip())
        try:
            handler = HA.MDHandler()
            print(handler.eval_ask(PAGE_HOLD.metadata, payload['query'], payload["flag"], payload['operation'], payload['value']))
        except Exception as e:
            print(e)
        return False


    def do_body(self, line):
        """body <markdown-path> <json payload>: This will return a rule using a JSON document format.
        { "name" : "must-have-h1", "id": "2", "query": "/html/body/h1", "flag" : "count", 
        "operation" : "==", "value" : "1", "level": "Required", 
        "mitigation": "You must have one H1 in your document." }

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        payload = json.loads(line.strip())
        try:
            handler = HA.MDHandler()
            print(handler.eval_query(PAGE_HOLD.html, payload['query'],  payload['flag'], payload['operation'],
            payload['value']))
        except Exception as e:
            print(e)
        return False


    def do_params(self, line):
        """Function to see the input from the paramater line. Returns the param list.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        print("Passed the following paramaters:")
        for i in sys.argv:
            print(i)
        print("passed the following in the line (all):")
        print(line)
        print("As a list:")
        print(line.split(" "))
        return False


    def do_help(self, line):
        """Type help to get help for the application.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        print(HELPTEXT)
        return False

    def do_quit(self, line):
        """Type quit to exit the application.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        return True

    def do_exit(self, line):
        """Type exit to exit the application.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        return True

    def do_EOF(self, line):
        """Type EOF to exit the application.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        return True


if __name__ == '__main__':
    TagTerminal().cmdloop(APPVERSION)
