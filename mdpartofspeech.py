'''
Class for the part of speech parser.
'''

import nltk


class MDPartofspeecher():
    '''Parser that parses sentences and can return number of sentences and part
    of speech.'''

    def __init__(self):
        self.PENN_TOKENS = {
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


    def parse_sentences(self, incorpus):
        '''Take a body text and return sentences in a list.'''
        sentences = nltk.sent_tokenize(incorpus)
        return sentences


    def number_sentences(self, incorpus):
        lisofsentences = self.parse_sentences(incorpus)
        return len(lisofsentences)


    def parse_words(self, insentence):
        '''Take a sentence and return tokens in the sentence.'''
        tokens = nltk.word_tokenize(insentence)
        tagged = nltk.pos_tag(tokens)
        return tagged


    def make_model(self, incorpus):
        '''Take a text body and return a parsed model that contains a
        list of lists. Each sublist is a set of tuples that identify 
        the word and part-of-speech.'''
        my_body = self.parse_sentences(incorpus)
        model = []
        for sentence in my_body:
            my_tokens = self.parse_words(sentence)
            for t in my_tokens:
                model.append(t)
        return model


    def get_word_pos(self, insentence, index):
        pointer = int(index)-1
        model = self.make_model(insentence)
        return model[pointer][1]