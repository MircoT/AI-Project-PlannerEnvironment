from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from heapq import nlargest

import random
from collections import deque

class iterative_deepening(LogAgent):

    """iterative_deepening LogAgent by Robert Parcus, 2014
    State space blind search with DFS using INCREMENTAL 
    max_depth approach. 

    When the agent hits too many known statuses and too
    few new ones, it is time to increase the
    max_depth a little.

    This is also called ITERATIVE DEEPENING  
    
    """

    def __init__(self):
        super(iterative_deepening, self).__init__()

    class NotFound(Exception): pass

    def discovery_forwards(self, status, stateMap):
        fringe = deque()
        stat = status.clone
        start_hash = hash(repr(stat))
        current_moves = []
        hits = 1
        misses = 1
        threshold = 3.5
        max_depth = 10
        print("\n")
        print("*"*60)
        print("\tITERATIVE DEEPENING: using DFS+BFS")
        print("\t", self.__doc__)
        print("\n"*2)
        print("\tHits threshold:", threshold)

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
                    hits += 1
                else:
                    misses += 1    
                if child_hash not in stateMap:
                    stateMap[child_hash] = []
                    stateMap[child_hash].append(curr_hash)
                    fringe.append(new_move)
                    hits += 1
                else:
                    misses += 1
            stat = status.clone
            hit_ratio = hits / misses
            print("\r\tMax_depth:", max_depth, "hits ratio:", hit_ratio, end='')
            if hit_ratio < threshold:
                max_depth += 1
            #if we go too deep
            if len(fringe[-1]) >= max_depth:
                #let's use a BFS approach
                current_moves = fringe.popleft()
                #and pop the fringe a bit. 
                # we are effectively giving up on going on that path any further.
                fringe.pop()
            else:
                #otherwhise DFS is COOL
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