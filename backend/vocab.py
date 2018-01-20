import json

FIRST_TOK = '__FIRST'
SECOND_TOK = '__SECOND'
THIRD_TOK = '__THIRD'
FOURTH_TOK = '__FOURTH'
UNK_TOK = '__UNK'
EOQ_TOK = '</quatrain>'

class Vocab:

  def __init__(self):
    self.sym_to_int = {}
    self.int_to_sym = {}
    self.add(FIRST_TOK)
    self.add(SECOND_TOK)
    self.add(THIRD_TOK)
    self.add(FOURTH_TOK)
    self.add(UNK_TOK)

  @staticmethod
  def vocabs_from_file(filepath):
    word_data, pos_data, suffix_data = json.load(open(filepath))
    word_vocab = Vocab()
    word_vocab.sym_to_int, word_vocab.int_to_sym = word_data
    word_vocab.int_to_sym = {int(c):word_vocab.int_to_sym[c] for c in word_vocab.int_to_sym}
    pos_vocab = Vocab()
    pos_vocab.sym_to_int, pos_vocab.int_to_sym = pos_data
    pos_vocab.int_to_sym = {int(c):pos_vocab.int_to_sym[c] for c in pos_vocab.int_to_sym}
    suffix_vocab = Vocab()
    suffix_vocab.sym_to_int, suffix_vocab.int_to_sym = suffix_data
    suffix_vocab.int_to_sym = {int(c):suffix_vocab.int_to_sym[c] for c in suffix_vocab.int_to_sym}
    return word_vocab, pos_vocab, suffix_vocab

  @staticmethod
  def vocabs_to_file(vocabs, filepath):
    word_vocab, pos_vocab, suffix_vocab = vocabs
    print(word_vocab.int_to_sym)
    json.dump(
        [[word_vocab.sym_to_int, word_vocab.int_to_sym],
          [pos_vocab.sym_to_int, pos_vocab.int_to_sym],
          [suffix_vocab.sym_to_int, suffix_vocab.int_to_sym]
        ], open(filepath, 'w'))


  def __getitem__(self, obj):
    if obj in self.sym_to_int:
      return self.sym_to_int[obj]
    elif obj in self.int_to_sym:
      return self.int_to_sym[obj]
    elif isinstance(obj, str):
      return self.sym_to_int[UNK_TOK]
    else:
      raise Exception("Int not found")

  def __repr__(self):
    return str(self.sym_to_int)

  def __len__(self):
    return len(self.sym_to_int)

  def add(self, obj):
    if obj not in self.sym_to_int:
      successor = len(self.sym_to_int)
      self.sym_to_int[obj] = successor
      self.int_to_sym[successor] = obj
