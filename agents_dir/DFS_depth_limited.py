from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from heapq import nlargest

import random
from collections import deque

class DFS_depth_limited(LogAgent):

    """
    DFS_depth_limited LogAgent by Robert Parcus, 2014
    State space blind search using DFS and 
    a max_depth approach. It is garanteed to terminate
    if the problem is solvable in less than
    max_depth steps. It is very good on graphs with
    nodes having many children, because the memory
    impact of this approach is linear and not exponential,
    as in the BFS approach
    """

    def __init__(self):
        super(DFS_depth_limited, self).__init__()

    class NotFound(Exception): pass

    def discovery_forwards(self, status, stateMap):
        print("\n"*2)
        print("*"*60)
        print("\t", self.__doc__)
        print("\n"*2)
        fringe = deque()
        stat = status.clone
        start_hash = hash(repr(stat))
        current_moves = []
        if start_hash not in stateMap:
            stateMap[start_hash] = []
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
                    fringe.append(new_move)
            stat = status.clone
            #print(len(fringe[-1]))
            while len(fringe[-1]) >= 40:
                fringe.pop()
            current_moves = fringe.pop()
            stat.execute(current_moves)
            goal_state = stat.clone
            goal_hash = hash(repr(stat))
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

    def solve(self, status, goal):  
        return self.itr_solve(status)