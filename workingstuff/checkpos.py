'''
    Part of Speech Extract
    Module returns the ratio of the parts-of-speech based on the Penn Treebank Project.
    Matt Briggs
    v1.0 2018.08.21
    v1.1 2021.5.17

    Refactor the module for use in my markdown parser.
    handles the following use cases:
    11. Shall evaluate the part of speech and position in a sentence.

'''

import os
import csv
import datetime
import nltk


THISDATE = str(datetime.date.today())

'''Alphabetical list of part-of-speech tags used in the Penn Treebank Project.'''

PENN_TOKENS = {
 "WRB": "Wh-adverb",
 "WP$": "Possessive wh-pronoun",
 "WDT": "Wh-determiner",
 "VBZ": "Verb, 3rd person singular present",
 "VBP": "Verb, non-3rd person singular present",
 "VBN": "Verb, past participle",
 "VBG": "Verb, gerund or present participle",
 "VBD": "Verb, past tense",
 "SYM": "Symbol",
 "RBS": "Adverb, superlative",
 "RBR": "Adverb, comparative",
 "PRP": "Personal pronoun",
 "POS": "Possessive ending",
 "PDT": "Predeterminer",
 "NNS": "Noun, plural",
 "NNP": "Proper noun, singular",
 "JJS": "Adjective, superlative",
 "JJR": "Adjective, comparative",
 "WP": "Wh-pronoun",
 "VB": "Verb, base form",
 "UH": "Interjection",
 "TO": "to",
 "RP": "Particle",
 "RB": "Adverb",
 "NN": "Noun, singular or mass",
 "MD": "Modal",
 "LS": "List item marker",
 "JJ": "Adjective",
 "IN": "Preposition or subordinating conjunction",
 "FW": "Foreign word",
 "EX": "Existential there",
 "DT": "Determiner",
 "CD": "Cardinal number",
 "CC": "Coordinating conjunction",
 "PRP$": "Possessive pronoun",
 "NNPS": "Proper noun, plural"

}


def to_str(bytes_or_str):
    '''Converts files into UTF-8'''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value


def get_textfromfile(path):
    '''Return text from a filename path'''
    textout = ""
    fh = open(path, "r", encoding="utf8")
    for line in fh:
        textout += line
    fh.close()
    textout = to_str(textout)
    return textout


def parse_sentences(incorpus):
    '''Take a body text and return sentences in a list.'''
    sentences = nltk.sent_tokenize(incorpus)
    return sentences


def number_sentences(incorpus):
    lisofsentences = parse_sentences(incorpus)
    return len(lisofsentences)


def parse_words(insentence):
    '''Take a sentence and return tokens in the sentence.'''
    tokens = nltk.word_tokenize(insentence)
    tagged = nltk.pos_tag(tokens)
    return tagged


def make_model(incorpus):
    '''Take a text body and return a parsed model that contains a
    list of lists. Each sublist is a set of tuples that identify 
    the word and part-of-speech.'''
    my_body = parse_sentences(incorpus)
    model = []
    for sentence in my_body:
        my_tokens = parse_words(sentence)
        for t in my_tokens:
            model.append(t)
    return model


def get_word_pos(insentence, index):
    pointer = index-1
    model = make_model(insentence)
    return model[pointer][1]


def export_csv(infile, outloc):
    '''Opens the file and then parses the sentences for part of speech 
    tokens, tallys them and creates the report.'''
    OUTPUTLOCATION = outloc + r"\partofspeech_{}.csv".format(THISDATE)

    print("Starting...")
    tally = []
    tally.append(["Part-of-speech", "Ratio"])

    # parse the file

    print("Getting file ... {}".format(infile))
    
    corpus = get_textfromfile(infile)
    parsed_sentences = make_model(corpus)
    part_of_speech = {}
    for token in parsed_sentences:
        if token[1] in part_of_speech.keys():
            part_of_speech[token[1]] += 1
        else:
            part_of_speech[token[1]] = 1
    totalcount = sum(part_of_speech.values())
    for i in part_of_speech.keys():
        if i in PENN_TOKENS.keys():
            ratio = part_of_speech[i]/totalcount
            tally.append([PENN_TOKENS[i], "{:.2%}".format(ratio)])

    # Generate CSV output

    csvout = open(OUTPUTLOCATION, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in tally:
        csvwrite.writerow(r)
    csvout.close()

    print("Creating your report at: " + OUTPUTLOCATION)

def main():
    # Shall evaluate the part of speech and position in a sentence.
    corpus1 = "Start the machine with the proper key."
    print(get_word_pos(corpus1, 1))

    # Shall count the number of sentences in an element (such as a paragraph).
    corpus2 = '''Disk IOPS (Input/Output Operations Per Second) on Azure Stack Hub 
is a function of VM size instead of the disk type. This means that for a Standard_Fs 
series VM, regardless of whether you choose SSD or HDD for the disk type, the IOPS limit 
for a single additional data disk is 2300 IOPS. The IOPS limit imposed is a cap (maximum 
possible) to prevent noisy neighbors. It isn't an assurance of IOPS that you'll get on a 
specific VM size.'''
    print(number_sentences(corpus2 ))


if __name__ == "__main__":
    main()
