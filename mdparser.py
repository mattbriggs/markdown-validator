'''
Classes for the parser.
- MDPage, a container class.
- MDParser, the Parser logic for a markdown file.
'''

import devrelutilities as DV
import markdown


class MDPage():
    '''Class that holds page data.'''

    def __init__(self):
        self.filepath = ""
        self.raw = ""
        self.metadata = {}
        self.html = ""


class MDParser():
    '''Class that parses a markdown file and return a json payload.'''


    def __init__(self):
        self.state = "New"
        self.raw = ""

    def get_raw_body(self, inpath):
        '''With a path return text.'''
        try:
            body = DV.get_text_from_file(inpath)
            self.raw = body
            return body
        except Exception as e:
            return "A path wasn't passed to the Parser. Error: {e}"

    def butcher(self):
        '''Split a file into three parts.'''
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
        '''Clears the metadata of garbage.'''
        a = fixit.strip()
        b = a.replace("\n", "")
        c = b.replace("# ", "")
        return c


    def process_meta(self):
        '''Creates key value pairs out of the lines of the metadata file.'''
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
        '''Converts the body markdown into HTML.'''
        if self.raw:
            file_body = self.butcher()[1]
            return markdown.markdown(file_body )
        else:
            return "Need to load a file with Parser.get_raw_body(<file-path>)."