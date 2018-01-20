import spacy

def create_pos_tag(text, nlp):
    tokens = nlp(text)
    lst_pos = [x.pos_ for x in tokens]
    for token in tokens:
        if token.text == '#':
            print(token.pos_);

nlp = spacy.load('en')

with open("../data/sonnets2.qtr") as f:
    f.readline()
    for line in f.readlines():
        create_pos_tag(line, nlp);
