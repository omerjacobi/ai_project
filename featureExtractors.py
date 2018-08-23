# featureExtractors.py
# --------------------

import util
import evaluation
from abalone import Marble, Action

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
    features = dict()
    successor = state.generate_successor(player_index, action)
    features["sumito"] = evaluation.attacking_opponent(successor, player_index) - evaluation.attacking_opponent(state, player_index)
    features["op_sumito"] = evaluation.attacked_by_opponent(successor,player_index) - evaluation.attacked_by_opponent(state,player_index)
    features["grouping"] = evaluation.own_marbles_grouping(successor, player_index) - evaluation.own_marbles_grouping(state, player_index)
    features["op_grouping"] = evaluation.opposing_marbles_grouping(successor, player_index) - evaluation.opposing_marbles_grouping(state, player_index)
    features["marbles"] = evaluation.lost_marbles(successor,player_index) - evaluation.lost_marbles(state,player_index)
    features["to_center"] = evaluation.dist_from_center(successor, player_index)
    features["op_to_center"] = evaluation.dist_from_center(successor, -player_index)



    # features["sumito"] = evaluation.attacking_opponent(successor, player_index)
    # features["op_sumito"] = evaluation.attacked_by_opponent(successor,player_index)
    # features["grouping"] = evaluation.own_marbles_grouping(successor, player_index)
    # features["op_grouping"] = evaluation.opposing_marbles_grouping(successor, player_index)
    # features["to_center"] = evaluation.dist_from_center(successor, player_index)

    



    return features