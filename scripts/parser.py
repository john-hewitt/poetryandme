import spacy
import json

import syllables

nlp = spacy.load('en_core_web_sm')

class WordTuple:
    def __init__(self, text = "", part_of_speech = "", syllables = 0, phonics = ""):
        self.text = text
        self.part_of_speech = part_of_speech
        self.syllables = syllables
        self.phonics = phonics

    def __repr__(self):
        return "%s <%s, %s, %d, %s>" % (self.__class__, self.text, self.part_of_speech, self.syllables, self.IPA)

    def __str__(self):
        return "%s <%s, %s, %d, %s>" % (self.__class__, self.text, self.part_of_speech, self.syllables, self.IPA)

#creates a list of WordTuples (only text and part of speech filled)
def FindPartOfSpeech(text, nlp):
    nlp_tokens = nlp(text)
    tokens = [WordTuple(x.text, x.pos_) for x in nlp_tokens]
    for token in tokens:
        if token.text == '\n':
            tokens.remove(token)
        if token.text == 'EOS':
            token.part_of_speech = 'SYM'

    return tokens

#determines syllables from list of WordTuple
def CountSyllables(word_tuples):
    for word_tuple in word_tuples:
        if word_tuple.text != 'EOS':
            if word_tuple.text.isalpha():
                word_tuple.syllables = syllables.count_syllables(word_tuple.text)
            else:
                word_tuple.syllables = 0

#find the ipa
def FindPhonics(word_tuples):
    for word_tuple in word_tuples:
        if word_tuple.text != 'EOS':
            word_tuple.phonics = word_tuple.text[-2:]

#output in json
def CreateTrainingData(word_tuples):
    word_tuple_list = list([word_tuple.text, word_tuple.part_of_speech, word_tuple.phonics, word_tuple.syllables] for word_tuple in word_tuples)
    return json.dumps(word_tuple_list)

#write to disk
def WriteJsonToDisk(data):
    with open("../data/training_data2.json", "w") as f:
        f.write(data)

with open("../data/test.qtr") as f:
    data = ""
    for line in f.readlines():
        #check for new sonnet
        if line[0] != '\n':
            word_tuples = FindPartOfSpeech(line, nlp)
            CountSyllables(word_tuples)
            FindPhonics(word_tuples)
            data += CreateTrainingData(word_tuples) + "\n"
        else:
            data += "\n"
    WriteJsonToDisk(data)

