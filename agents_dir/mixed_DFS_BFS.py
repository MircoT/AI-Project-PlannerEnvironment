from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from heapq import nlargest

import random
from collections import deque

class mixed_DFS_BFS(LogAgent):

    """mixed_DFS_BFS LogAgent by Robert Parcus, 2014
    State space blind search with DFS, using
    a max_depth approach mixed with a BFS.

    Whenever we are too deep, we pop away that instruction
    and we backtrack to the begining of the stack.

    In the end it get's harder and harder to find new states,
    infact many of the initial states have already been found.
    In many cases we may find many more know states than new
    discoveries, so it tends to get preety slow if a solution
    is not found rapdly.

    Its' memory impact isn't as big as BFS but is bigger than
    the pure max_depth DFS approach.

    This approach is a mix of the strenghts and weaknesses of 
    DFS & BFS uninformed searches.
    """

    def __init__(self):
        super(mixed_DFS_BFS, self).__init__()

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
            #if we go too deep
            if len(fringe[-1]) >= 50:
                #let's use a BFS approach
                current_moves = fringe.popleft()
                #and pop the fringe a bit
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