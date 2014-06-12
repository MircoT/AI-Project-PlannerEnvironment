from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from heapq import nlargest

import random
from collections import deque

class DFS(LogAgent):

    """
    DFS LogAgent by Robert Parcus, 2014
    State space blind search using DFS. It is fast
    for small problems, and it won't find the best solution.

    This approach will go as deep as it can get...

    This version uses a special trick to avoid saving
    te fringe as a huge list of statuses.
    It saves a list o movements, which are smaller objs
    than statuses.

    A "state map" is kept but it is actually a graph
    with hashes from the statuses.

    It is necessary to avoid loops
    """

    def __init__(self):
        super(DFS, self).__init__()

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
            current_moves = fringe.pop() #CHANGING here we pass from BFS to DFS!!!! ＼（＠￣∇￣＠）／
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