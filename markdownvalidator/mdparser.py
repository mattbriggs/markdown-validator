'''
Classes for the parser.
- MDPage, a container class.
- MDParser, the Parser logic for a markdown file.
'''

import markdownvalidator.mod_utilities as MU
import markdown


class MDPage():
    """Class that holds page data.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """

    def __init__(self):
        self.filepath = ""
        self.raw = ""
        self.metadata = {}
        self.html = ""


class MDParser():
    """Class that parses a markdown file and return a json payload.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """


    def __init__(self):
        self.state = "New"
        self.raw = ""

    def get_raw_body(self, inpath):
        """With a path return text.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        try:
            body = MU.get_textfromfile(inpath)
            self.raw = body
            return body
        except Exception as e:
            return "A path wasn't passed to the Parser. Error: {}".format(e)

    def butcher(self):
        """Split a file into three parts.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        parts = self.raw.split("---")
        sized = len(parts)
        part_one = parts[1]
        merge = ""
        for i in range(sized):
            if i > 1:
                merge += parts[i]
        return_index = [part_one, merge]
        return return_index


    def clear_it(self, fixit):
        """Clears the metadata of garbage.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        a = fixit.strip()
        b = a.replace("\n", "")
        c = b.replace("# ", "")
        return c


    def process_meta(self):
        """Creates key value pairs out of the lines of the metadata file.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        if self.raw:
            file_meta = self.butcher()[0]
            mdata = file_meta.split("\n")
            meta_data = {}
            for i in mdata:
                if i:
                    key_value = i.split(":")
                    meta_data[self.clear_it(key_value[0])] = self.clear_it(key_value[1])
            return meta_data
        else:
            return "Need to load a file with Parser.get_raw_body(<file-path>)."


    def process_body(self):
        """Converts the body markdown into HTML.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
        if self.raw:
            file_body = self.butcher()[1]
            return markdown.markdown(file_body )
        else:
            return "Need to load a file with Parser.get_raw_body(<file-path>)."