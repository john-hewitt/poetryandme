import argparse
import dynet as dy
from vocab import Vocab, FIRST_TOK, SECOND_TOK, THIRD_TOK, FOURTH_TOK, EOQ_TOK
import sys
from attender import EmptyAttender
import en_core_web_sm
nlp = en_core_web_sm.load()
import yaml
import json
import spacy
from tqdm import tqdm


class RNNLM:

  def __init__(self, vocabs, pc):
    self.word_vocab, self.pos_vocab, self.suffix_vocab = vocabs

    self.pc = pc
    self.WORD_EMBED_SIZE = 100
    self.POS_EMBED_SIZE = 20
    self.SUFFIX_EMBED_SIZE = 40
    self.SYLL_SIZE = 1
    self.total_input_size = self.WORD_EMBED_SIZE + self.POS_EMBED_SIZE \
        + self.SUFFIX_EMBED_SIZE + self.SYLL_SIZE

    self.RNN_HIDDEN_SIZE = 80

    self.rnn = dy.VanillaLSTMBuilder(1, self.total_input_size, self.RNN_HIDDEN_SIZE, pc)

    self.attender = EmptyAttender()

    self.word_vecs = self.pc.add_lookup_parameters((len(self.word_vocab), self.WORD_EMBED_SIZE))
    self.pos_vecs = self.pc.add_lookup_parameters((len(self.pos_vocab), self.POS_EMBED_SIZE))
    self.suffix_vecs = self.pc.add_lookup_parameters((len(self.suffix_vocab), self.SUFFIX_EMBED_SIZE))

    self.W = self.pc.add_parameters((len(self.word_vocab), self.RNN_HIDDEN_SIZE))
    self.b = self.pc.add_parameters((len(self.word_vocab)))

  def initialize(self):
    self.states_so_far = []
    return self.rnn.initial_state()

  def get_concatenated_representation(self, token):
    word, pos, suffix, syll_count = token
    word_vec = self.word_vecs[word]
    pos_vec = self.pos_vecs[pos]
    suffix_vec = self.suffix_vecs[suffix]
    syll_vec = dy.inputVector([syll_count])
    return dy.concatenate([word_vec, pos_vec, suffix_vec, syll_vec])

  def generate(self, state):
    for last_tok in [FIRST_TOK, SECOND_TOK, THIRD_TOK, FOURTH_TOK]:
      last_pos = last_tok
      last_suffix = last_tok
      syll_count = 0
      string_so_far = ''
      toks_so_far = []
      token = [self.word_vocab[last_tok], self.pos_vocab[last_tok], self.suffix_vocab[last_tok], syll_count]
      while last_tok != EOQ_TOK and len(toks_so_far) < 3*15 :
        token = [self.word_vocab[last_tok], self.pos_vocab[last_pos], self.suffix_vocab[last_suffix], syll_count]

        state, probs = self.add_input(state, token)
        probs = probs.value()
        next_word_tok = self.word_vocab[probs.index(max(probs))]

        string_so_far += next_word_tok + ' ' if next_word_tok != 'EOS' else '\n'
        parsed_string = nlp(string_so_far)
        toks_so_far.append(next_word_tok)
        last_tok = next_word_tok
        last_pos = parsed_string[-1].tag_
        last_suffix = parsed_string[-1].text
        syll_count = 0 #len(parsed_string[-1].text)/3
      print(string_so_far)

  def add_input(self, state, token):
    input_vec = self.get_concatenated_representation(token)
    hidden_state = state.add_input(input_vec)
    prediction_vector = hidden_state.output()
    b = dy.parameter(self.b)
    W = dy.parameter(self.W)

    probs = dy.softmax(dy.affine_transform([b, W, prediction_vector]))
    return hidden_state, probs

class RNNLMTrainer:

  def __init__(self, pc, epochs=30):
    self.epochs = epochs
    self.pc = pc
    self.trainer = dy.AdamTrainer(pc)
    self.BATCH_SIZE = 1

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

  def symbol_augment_quatrain(self, quatrain, quatrain_index):
    augment_symbols = [FIRST_TOK, SECOND_TOK, THIRD_TOK, FOURTH_TOK]
    return [[augment_symbols[quatrain_index]]*3 + [0] ] + quatrain + [[EOQ_TOK]*3 + [0]]
  
  def load_raw_quatrains(self, quatrains_filepath):
    quatrains = []
    quatrain_index = 0
    for line in open(quatrains_filepath):
      if line.strip():
        quatrain = self.symbol_augment_quatrain(
            json.loads(line.strip()), quatrain_index)
        quatrains.append(quatrain)
        quatrain_index+= 1
        quatrain_index = quatrain_index  if quatrain_index < 4 else 0
        print(quatrain)
    return quatrains

  def integerize_quatrains(self, vocabs, quatrains):
    word_vocab, pos_vocab, suffix_vocab = vocabs
    integerized_quatrains = []
    for quatrain in quatrains:
      integerized_tokens = []
      for word, pos, suffix, num_syll in quatrain:
        integerized_tokens.append((word_vocab[word], pos_vocab[pos], suffix_vocab[suffix], num_syll))
      integerized_quatrains.append(integerized_tokens)
      #print(integerized_tokens)
    return integerized_quatrains

  def train(self, rnnlm, quatrains):
    min_loss = sys.maxsize
    for i in tqdm(range(self.epochs), desc='Training'):
      losses = []
      tqdm.write('Epoch {}'.format(i))
      total_loss = 0
      state = rnnlm.initialize()
      for count, quatrain in enumerate(quatrains):
        #print(count, quatrain[0])
        for token, (next_word, _, _, _) in zip(quatrain, quatrain[1:]):
          state, probs = rnnlm.add_input(state, token)
          loss = -dy.log(dy.pick(probs, next_word))
          losses.append(loss)
        if count % self.BATCH_SIZE == 0:
          loss = dy.esum(losses)
          total_loss += loss.value()
          loss.backward()
          self.trainer.update()
          losses = []
          #dy.renew_cg()
          #state = rnnlm.initialize()
        if (count + 1)% 4 == 0:
          dy.renew_cg()
          state = rnnlm.initialize()
      tqdm.write('Training Loss: {}'.format(total_loss))
      rnnlm.generate(rnnlm.initialize())
      if total_loss < min_loss:
        min_loss = total_loss

if __name__ == '__main__':
  argp = argparse.ArgumentParser()
  argp.add_argument('quatrains_filepath')
  args = argp.parse_args()
  pc = dy.ParameterCollection()
  model_trainer = RNNLMTrainer(pc)
  quatrains = model_trainer.load_raw_quatrains(args.quatrains_filepath)
  vocabs = model_trainer.get_vocabs(quatrains)
  integerized_quatrains = model_trainer.integerize_quatrains(vocabs, quatrains)
  rnnlm = RNNLM(vocabs, pc)
  model_trainer.train(rnnlm, integerized_quatrains)
