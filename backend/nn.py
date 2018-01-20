import argparse
import dynet as dy
from vocab import Vocab
import yaml
import json


class RNNLM:

  def __init__(self, vocabs):
    self.word_vocab, self.pos_vocab, self.suffix_vocab = vocabs

    self.pc = dy.ParameterCollection()

  def one_epcoh():
    pass

  def loss():
    pass

  def topks():
    pass

class RNNLMTrainer:

  def __init__(self, epochs = 30):
    self.epochs = epochs

  def get_vocabs(self, quatrains):
    word_vocab = Vocab()
    pos_vocab = Vocab()
    suffix_vocab = Vocab()
    for quatrain in quatrains:
      for word, pos, suffix, syllable_count in quatrain:
        word_vocab.add(word)
        pos_vocab.add(pos)
        suffix_vocab.add(suffix)
    return word_vocab, pos_vocab, suffix_vocab

  def load_raw_quatrains(self, quatrains_filepath):
    quatrains = []
    for line in open(quatrains_filepath):
      if line.strip():
        quatrains.append(json.loads(line.strip()))
    return quatrains

  def train():
    for i in range(self.epochs):
      pass


if __name__ == '__main__':
  argp = argparse.ArgumentParser()
  argp.add_argument('quatrains_filepath')
  args = argp.parse_args()
  model_trainer = RNNLMTrainer()
  quatrains = model_trainer.load_raw_quatrains(args.quatrains_filepath)
  vocabs = model_trainer.get_vocabs(quatrains)
  print(vocabs)

