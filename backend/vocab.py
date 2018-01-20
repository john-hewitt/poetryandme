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
