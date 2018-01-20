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
        if token.text == 'EOS':
            token.part_of_speech = 'SYM'

    return tokens

#determines syllables from list of WordTuple
def CountSyllables(word_tuples):
    for word_tuple in word_tuples:
        if word_tuple.text != 'EOS':
            word_tuple.syllables = syllables.count_syllables(word_tuple.text)

#find the ipa
def FindPhonics(word_tuples):
    for word_tuple in word_tuples:
        if word_tuple.text != 'EOS':
            word_tuple.phonics = word_tuple.text[-2:]

#output in json
def CreateTrainingData(word_tuples):
    return json.dumps(list({'word': word_tuple.text, 'POS': word_tuple.part_of_speech, 'suffix': word_tuple.phonics, 'syllable': word_tuple.syllables} for word_tuple in word_tuples))

#write to disk
def WriteJsonToDisk(data):
    with open("../data/training_data.json", "w") as f:
        f.write(data)

with open("../data/sonnets.qtr") as f:
    data = ""
    for line in f.readlines():
        #check for new sonnet
        if line[0] != '\n':
            word_tuples = FindPartOfSpeech(line, nlp)
            CountSyllables(word_tuples)
            FindPhonics(word_tuples)
            data += CreateTrainingData(word_tuples) + ","
    data = data[:-1]
    WriteJsonToDisk(data)

