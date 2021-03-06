from nn import RNNLM, RNNLMTrainer
import sys
import dynet as dy
from vocab import FIRST_TOK, SECOND_TOK, THIRD_TOK, FOURTH_TOK
import numpy
from vocab import Vocab
import argparse
import en_core_web_sm
from penn_syllables import count_syllables
nlp = en_core_web_sm.load()



class SonnetPredictor:

  def __init__(self, param_path, vocab_path):
    self.pc = dy.ParameterCollection()

    loader = RNNLMTrainer(self.pc)
    self.vocabs = Vocab.vocabs_from_file(vocab_path)
    self.rnnlm = RNNLM(self.vocabs, self.pc)

    self.pc.populate(param_path)

    self.state = None

    self.quatrain_tokens = [FIRST_TOK, SECOND_TOK, THIRD_TOK, FOURTH_TOK]


  def load_RNNLM(self, param_path):
    pass

  def add_word(self, token):
    if isinstance(token, str):
      doc = nlp(token)
      token = [self.rnnlm.word_vocab[token], 
          self.rnnlm.pos_vocab[doc[0].pos_],
          self.rnnlm.suffix_vocab[doc[0].text[-2:]],
          count_syllables(doc[0].text)]
    else:
      word, pos, suff, syll = token
      token = [self.rnnlm.word_vocab[word],
          self.rnnlm.pos_vocab[pos],
          self.rnnlm.suffix_vocab[suff],
          syll]

    self.state, probs = self.rnnlm.add_input(self.state, token)
    prob_values = probs.value()
    topks = numpy.argsort(prob_values)[-10:]

    return [self.rnnlm.word_vocab[x] for x in topks]

  def new_poem(self):
    self.quatrain_index = 0
    self.new_quatrain()

  def new_quatrain(self):
    self.state = self.rnnlm.initialize()
    quatrain_token = self.quatrain_tokens[self.quatrain_index]
    self.state, probs = self.rnnlm.add_input(self.state,
        [self.rnnlm.word_vocab[quatrain_token], self.rnnlm.pos_vocab[quatrain_token],
          self.rnnlm.suffix_vocab[quatrain_token], 0])
    self.quatrain_index = self.quatrain_index + 1 if self.quatrain_index < 3 else 0

  def delete_word(self):
    # Delete two words from the RNNLM (one will be added back in by backend.)
    self.state = self.rnnlm.delete_word()
    self.state = self.rnnlm.delete_word()

    


if __name__ == '__main__':
  argp = argparse.ArgumentParser()
  argp.add_argument('param_path')
  argp.add_argument('vocab_path')
  args = argp.parse_args()

  sp = SonnetPredictor(args.param_path, args.vocab_path)
  sp.new_poem()
  poem = ''
  print('Listening...')
  while True:
    try:
      word = input().strip()
      poem += ' ' + word if word != 'eos' else '\n' + word
      print()
      sp.add_word(word)
      print(poem)
    except KeyboardInterrupt:
      print('Exiting...')
      exit()
