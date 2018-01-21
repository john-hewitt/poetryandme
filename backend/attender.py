import dynet as dy

class EmptyAttender:
  '''
  Does nothing to a decoder state
  '''

  def get_attention_state(self, main, states):
    return main

  def get_affinity(self, main, aux):
    pass

  def get_prob_dist(self, main, aux):
    pass

class BilinearAttender:
  '''
  Defines a bilinear attention
  '''

  def __init__(self, pc, dimension):
    self.dimension = dimension
    self.pc = pc
    self.W = self.pc.add_parameters((dimension, dimension))
    self.Wa = self.pc.add_parameters((dimension, 2*dimension ))
    self.b = self.pc.add_parameters((dimension))

  def get_attention_state(self, main, states):
    if not states:
      return main
    affinities = [self.get_affinity(main, state) for state in states]
    states_exp = dy.transpose(dy.concatenate_cols(states))
    scores_exp = dy.softmax(dy.concatenate(affinities))
    context = None
    if len(states) == 1:
      context = dy.transpose(states_exp)
    else:
      context = dy.transpose(states_exp)*scores_exp

    Wa = dy.parameter(self.Wa)
    b = dy.parameter(self.b)
    hidden_state = dy.affine_transform([b, Wa, dy.concatenate([main, context])])
    return hidden_state


  def get_affinity(self, main, aux):
    W = dy.parameter(self.W)
    score = (dy.transpose(main) * W) * aux
    return score
