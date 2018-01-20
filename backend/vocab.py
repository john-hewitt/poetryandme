class Vocab:

  def __init__(self):
    self.sym_to_int = {}
    self.int_to_sym = {}
    self.add('__FIRST')
    self.add('__SECOND')
    self.add('__THIRD')
    self.add('__FOURTH')

  def __getitem__(self, obj):
    if obj in self.sym_to_int:
      return self.sym_to_int[obj]
    elif obj in self.int_to_sym:
      return self.int_to_sym[obj]
    else:
      raise Exception("Symbol not found")

  def __repr__(self):
    return str(self.sym_to_int)

  def add(self, obj):
    if obj not in self.sym_to_int:
      successor = len(self.sym_to_int)
      self.sym_to_int[obj] = successor
      self.int_to_sym[successor] = obj
