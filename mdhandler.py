''' Markdown XPATH Functions

    This is a library of functions for the markdown path processor.

    Matt Briggs V1.0.1: 4.6.2021
'''

import json
from lxml import etree
import mod_utilities as MU
import mdparser as PA
from datetime import date, datetime, timedelta
import re
import html2text
import mdpartofspeech as POS

class MDHandler():
    '''Object that contains the logic for processing queries.'''

    def __init__(self):
        '''Initital state is new.'''
        self.state = "New"


    def process_xpath(self, in_html, query, flag=""):
        '''With html, an XPATH query, and a flag `count`/`text`, returns the
        the count of nodes, or the content of the first node.'''
        try:
            htmlparser = etree.HTMLParser()
            tree = etree.fromstring(in_html, htmlparser)
            if flag == "all":
                return html2text.html2text(in_html)
            else:
                result_raw = tree.xpath(query)
                if flag == "count":
                    return(len(result_raw))
                elif flag == "text":
                    if result_raw:
                        return result_raw[0].text
                    else:
                        return None
                elif flag == "dom":
                    if result_raw:
                        return result_raw[0].tag
                    else:
                        return None
        except Exception as e:
            return "Failed to query file.\n{}".format(e)


    def process_metadata(self, in_json, value1):
        '''With a metdata file check the key and return the value.'''
        return in_json[value1]


    def operate_equal(self, in_string, in_value):
        '''Evaluate if the two strings are equal.'''
        return bool(in_string.strip() == in_value.strip())


    def operate_greater(self, in_string, in_value):
        '''Evaluate if the result is greater than the value.'''
        return bool((in_string).strip() > str(in_value).strip())


    def operate_less(self, in_string, in_value):
        '''Evaluate if the result is less than the value.'''
        return bool((in_string).strip() < str(in_value).strip())


    def operate_not(self, in_string, in_value):
        '''Evaluate if the two strings aren't equal.'''
        return bool((in_string).strip() != str(in_value).strip())


    def operate_contains(self, in_string, in_value):
        '''Evaluate if a string is contained in another string. Case sensitive.'''
        a_string = " {}".format(in_string.lower())
        b_string = in_value.lower().strip()
        if a_string.find(b_string) > 0:
            return True
        else:
            return False


    def operate_starts(self, in_string, in_value):
        '''Evaluate if a string is starts another string. Case sensitive.'''
        return in_string.startswith(in_value.strip())


    def operate_ends(self, in_string, in_value):
        '''Evaluate if a string is ends with another string. Case sensitive.'''
        return in_string.endswith(in_value.strip())


    def prepare_date(self, instring):
        '''With a date string, m/d/year, convert to a date object.'''
        if instring.find("/") > -1:
            instring = instring.replace("/", "-")
        dl = instring.split("-")
        if len(dl[2]) == 4:
            tl = dl[:2]
            tl.append(dl[2][2:])
            return date(month=int(tl[0]), day=int(tl[1]), year=int(tl[2]))
        else:
            return date(month=int(dl[0]), day=int(dl[1]), year=int(dl[2]))


    def eval_date(self, indate, operator, in_value):
        '''With a date, an operator, and a value return a bool.'''
        date1 = self.prepare_date(indate)

        if in_value.lower() == "now":
            date2 = datetime.now()
        else:
            try:
                in_value = int(in_value)
                date_x = datetime.now() - timedelta(days=in_value)
                date2 = datetime.date(date_x)
            except ValueError:
                date2 = self.prepare_date(in_value)

        if operator == "==":
            return bool(date1 == date2)
        elif operator == ">":
            return bool(date1 > date2)
        elif operator == "<":
            return bool(date1 < date2)
        elif operator == "!=":
            return bool(date1 != date2)


    def eval_length(self, instring, in_value):
        size = len(instring)
        print("{} : {}".format(size, in_value))
        return bool(size < int(in_value))


    def get_part_of_speech(self, in_html, query, flag, operator):
        result = str(self.process_xpath(in_html, query, flag))
        index = int(operator[1:])
        sentences = POS.MDPartofspeecher()
        pos = sentences.get_word_pos(result, index)
        return pos


    def eval_part_of_speech(self, result, index, in_value):
        sentences = POS.MDPartofspeecher()
        pos = sentences.get_word_pos(result, index)
        return bool(pos == in_value)


    def eval_number_sentences(self, result, in_value):
        sentences = POS.MDPartofspeecher()
        no_sent = sentences.number_sentences(result)
        return bool(no_sent <= int(in_value))


    def eval_query(self, in_html, query, flag, operator, in_value):
        '''With the result of an xpath, the operator token, and a value, produce true/false'''
        try:
            result = str(self.process_xpath(in_html, query, flag))
            if operator == "==":
                return self.operate_equal(result, in_value)
            elif operator == ">":
                return self.operate_greater(result, in_value)
            elif operator == "<":
                return self.operate_less(result, in_value)
            elif operator == "!=":
                return self.operate_not(result, in_value)
            elif operator == "[]":
                return self.operate_contains(result, in_value)
            elif operator == "[:":
                return self.operate_starts(result, in_value)
            elif operator == ":]":
                return self.operate_ends(result, in_value)
            elif operator == "l":
                return self.eval_length(result, in_value)
            elif operator[0] == "p":
                index = int(operator[1:])
                return self.eval_part_of_speech(result, int(index), in_value)
            elif operator == "s":
                return self.eval_number_sentences(result, in_value)
            elif operator == "r":
                return bool(re.match(in_value, result))
            else:
                return False
        except:
            return False


    def clear_list(self, in_list):
        '''With a string dellimited by commas, create a list.'''
        val_list = in_list.split(",")
        truth_list = []
        for v in val_list:
            truth_list.append(v.strip())
        return truth_list


    def eval_list(self, in_html, keyword, flag, operator, in_value):
        '''With the metadata block as json, the operator token, and a value, produce true/false.'''
        in_list = self.clear_list(in_value)
        truth = []
        for i in in_list:
            one_truth = self.eval_query(in_html, keyword, flag, operator, i)
            truth.append(one_truth)
        for i in truth:
            if i == False:
                return False
            else:
                return True


    def eval_ask(self, in_json, keyword, flag, operator, in_value):
        '''With the metadata block as json, the operator token, and a value, produce true/false.'''
        if flag.lower() == "" or flag.lower() == "value":
            try:
                result = str(in_json[keyword])
                if operator == "==":
                    return self.operate_equal(result, in_value)
                elif operator == ">":
                    return self.operate_greater(result, in_value)
                elif operator == "<":
                    return self.operate_less(result, in_value)
                elif operator == "!=":
                    return self.operate_not(result, in_value)
                elif operator == "[]":
                    return self.operate_contains(result, in_value)
                else:
                    return False
            except:
                return False
        elif flag.lower() == "check":
            try:
                in_json[keyword]
                return True
            except:
                return False
        elif flag.lower() == "date":
            result = str(in_json[keyword])
            return self.eval_date(result, operator, in_value)
        elif flag.lower() == "pattern":
            result = str(in_json[keyword])
            return bool(re.match(result, in_value))


    def get_page(self, infile):
        ''' '''
        md_page = PA.MDPage()
        md_parser = PA.MDParser()
        md_parser.get_raw_body(infile)
        md_page.raw = md_parser.raw
        md_page.metadata = md_parser.process_meta()
        md_page.html = md_parser.process_body()
        return md_page


    def make_html(self, string_html, target):
        '''Make HTML'''
        try:
            MU.write_text(string_html, target)
            return "Saving file to: {}".format(target)
        except Exception as e:
            return "Failed to create and save file: {}".format(e)

    def make_json(self, page, target):
        '''Make json'''
        try:
            with open(target, 'w') as json_file:
                json.dump(page, json_file)
            return "Saving file to: {}".format(target)
        except Exception as e:
            return "Failed to create and save file: {}".format(e)

    def eval_meta(self, in_json, value1):
        '''With a key and value, evalute the value. Returns T/F.'''
        if in_json[value1]:
            return in_json[value1]
        else:
            return False

    def get_rules(self, RULE):
        '''Get the stem and path and create a dictionary of stems to paths.'''
        schema_dict = {}
        return schema_dict
