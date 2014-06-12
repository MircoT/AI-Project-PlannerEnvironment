from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from heapq import nlargest

import random
from collections import deque

class BFS(LogAgent):

    """
    BFS LogAgent by Robert Parcus, 2014
    State space blind search using BFS. It is very fast
    for small problems, but impractical for realistic
    situations.
    """

    def __init__(self):
        super(BFS, self).__init__()

    class NotFound(Exception): pass

    def discovery_forwards(self, status, stateMap):
        print("\n"*2)
        print("*"*60)
        print("\t", self.__doc__)
        print("\n"*2)
        
        fringe = deque()
        stat = status.clone
        start_hash = hash(repr(stat))
        if start_hash not in stateMap:
            stateMap[start_hash] = []
        while not stat.check_goal():
            curr_hash = hash(repr(stat))
            for move in stat.moves:
                child = stat.clone
                child.execute([move])
                child_hash = hash(repr(child))
                if child_hash not in stateMap[curr_hash]:
                    stateMap[curr_hash].append(child_hash)
                if child_hash not in stateMap:
                    stateMap[child_hash] = []
                    stateMap[child_hash].append(curr_hash)
                    fringe.append(child.clone)
            stat = fringe.popleft()
            goal_state = stat.clone
            goal_hash = hash(repr(stat))
        return {'stateMap': stateMap, 'goal_hash': goal_hash, 'goal_state': goal_state, 'start_hash': start_hash}


    def itr_solve(self, status):
        start_hash = hash(repr(status))
        stateMap = {start_hash: []}
        goal_hash = []
        goal_state = []
        best_path = []
        output_moves = []

        tmp = self.discovery_forwards(status.clone, stateMap)
        stateMap = tmp["stateMap"]
        goal_state.append(tmp["goal_state"])
        start_hash = tmp["start_hash"]
        goal_hash.append(tmp["goal_hash"])

        print("Finding path with minimum number of steps")
        for i in range(len(goal_hash)):
            best_path.append(self.search_shortest_path(stateMap, start_hash, goal_hash[i]))
        final_moves = []
        for path in best_path:
            clone = status.clone
            for i in range(1, len(path)):
                stat = clone.clone
                for move in stat.moves:
                    clone = stat.clone
                    clone.execute([move])
                    child_hash = hash(repr(clone))
                    if path[i] == child_hash:
                        output_moves.append(move)
                        break
            if len(final_moves) > 0:
                if self.get_solution_cost(status, output_moves) < self.get_solution_cost(status, final_moves):
                    final_moves = output_moves
            else:
                final_moves = output_moves
            output_moves = []
        best_path = min(best_path, key=len)

        clone = status.clone
        for i in range(1, len(best_path)):
            stat = clone.clone
            for move in stat.moves:
                clone = stat.clone
                clone.execute([move])
                child_hash = hash(repr(clone))
                if best_path[i] == child_hash:
                    output_moves.append(move)
                    break
        #return output_moves
        return final_moves

    def search_shortest_path(self, graph, start, goal):
        visited = {start: None}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node == goal:
                path = []
                while node is not None:
                    path.append(node)
                    node = visited[node]
                return path[::-1]
            for neighbour in graph[node]:
                if neighbour not in visited:
                    visited[neighbour] = node
                    queue.append(neighbour)
        raise self.NotFound('No path from {} to {}'.format(start, goal))  

    def get_solution_cost(self, status, moves):
        cost = 0
        for move in moves:
            if move[0] in ["unload", "load"]:
                cost += 10
            else:
                cost += 10*status.airports[move[2]].neighbors[move[3]]
        return cost

    def solve(self, status, goal):  
        return self.itr_solve(status)