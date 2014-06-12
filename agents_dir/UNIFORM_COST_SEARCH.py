from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
#from heapq import nlargest
import bisect

import random
from collections import deque

class UNIFORM_COST_SEARCH(LogAgent):

    """
    UNIFORM_COST_SEARCH LogAgent by Robert Parcus, 2014
    State space blind search using Uniform Cost Search.

    In standard breadth-ﬁrst search, we are always expanding nodes
    that are closest to the initial state in terms of the number 
    of actions in the path.

    But in Uniform Cost search we expand the nodes that are closest
    to the initial state in terms of the cost of their path.
    Consequently, nodes on the fringe will have approximately equal
    costs.

    It the cost of all actions is the same, Uniform Cost seach is
    equivalent to standard BFS.
    Uniform Cost search can be implemented by a queue that is
    ordered by means of the path cost function (lowest cost first).

    """

    def __init__(self):
        super(UNIFORM_COST_SEARCH, self).__init__()

    class NotFound(Exception): pass

    def discovery_forwards(self, status, stateMap):
        # we can't use deques here, insert() is supported only
        # on lists.
        fringe = []
        stat = status.clone
        start_hash = hash(repr(stat))
        current_moves = []

        print("\n")
        print("*"*60)
        print("\tUNIFORM COST SEARCH: a variant of BFS")
        #broken
        #print("\t", self.__doc__)
        print("\n"*2)

        if start_hash not in stateMap:
            stateMap[start_hash] = []
        cost_list = []
        while not stat.check_goal():
            curr_hash = hash(repr(stat))
            for move in stat.moves:
                child = status.clone
                new_move = current_moves + [move]
                child.execute(new_move)
                child_hash = hash(repr(child))
                if child_hash not in stateMap[curr_hash]:
                    stateMap[curr_hash].append(child_hash)
                if child_hash not in stateMap:
                    stateMap[child_hash] = []
                    stateMap[child_hash].append(curr_hash)
                    # We find the cost of this moves list
                    move_cost = self.get_solution_cost(status, new_move)
                    # we find the position this moves should take on the list
                    position = bisect.bisect_left(cost_list, move_cost)
                    # we update the costs list
                    bisect.insort_left(cost_list, move_cost)
                    # finally we insert the move on it's ordered position
                    fringe.insert(position, new_move)
            stat = status.clone
            # here we pop() from the left, like in BFS
            current_moves = fringe.pop(0)
            # and we trow away the current_move cost from the list
            print("\r\tCurrent cost:", cost_list.pop(0), "Fringe size:", len(fringe), end='')
            stat.execute(current_moves)
            goal_state = stat.clone
            goal_hash = hash(repr(stat))
        #print(current_moves)
        return {'stateMap': stateMap, 'goal_hash': goal_hash, 'goal_state': goal_state, 'start_hash': start_hash, "final_moves": current_moves}


    def itr_solve(self, status):
        start_hash = hash(repr(status))
        stateMap = {start_hash: []}
        goal_hash = []
        goal_state = []

        tmp = self.discovery_forwards(status.clone, stateMap)
        stateMap = tmp["stateMap"]
        goal_state.append(tmp["goal_state"])
        start_hash = tmp["start_hash"]
        final_moves = tmp["final_moves"]
        goal_hash.append(tmp["goal_hash"])

        return final_moves

    def get_solution_cost(self, status, moves):
        cost = 0
        for move in moves:
            if move[0] in ["unload", "load"]:
                cost += 10
            else:
                cost += 10*status.airports[move[2]].neighbors[move[3]]
        return cost

    def solve(self, status, goal):  
        #print("YEAH!!")
        return self.itr_solve(status)