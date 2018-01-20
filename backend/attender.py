class EmptyAttender:
  '''
  Does nothing to a decoder state
  '''

  def get_attention_state(self, main, aux):
    return main

  def get_affinity(self, main, aux):
    pass

  def get_prob_dist(self, main, aux):
    pass

