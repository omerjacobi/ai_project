# featureExtractors.py
# --------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"Feature extractors for Pacman game states"
import util
import evaluation


class FeatureExtractor:  
  def getFeatures(self, state, action, player_index):
    """
      Returns a dict from features to counts
      Usually, the count will just be 1.0 for
      indicator functions.  
      :param player_index:
    """
    util.raiseNotDefined()



class SimpleExtractor(FeatureExtractor):
  """
  Returns simple features for a basic reflex Pacman:
  - whether food will be eaten
  - how far away the next food is
  - whether a ghost collision is imminent
  - whether a ghost is one step away
  """
  
  def getFeatures(self, state, action, player_index):
    features = util.Counter()
    successor = state.generate_successor(player_index, action)
    features["bias"] = 1.0
    features["sumito"] = evaluation.attacking_opponent(successor, player_index)
    features["op_sumito"] = -evaluation.attacked_by_opponent(successor,player_index)
    features["to_center"] = evaluation.dist_from_center(successor, player_index)/10
    features["marbles"] = evaluation.lost_marbles(successor,player_index)
    features.divideAll(10)
    if features["sumito"] + features["op_sumito"] +  features["marbles"] != 0:
        a = 1


    


    return features