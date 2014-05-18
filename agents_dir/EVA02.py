# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *

import random
from collections import deque

class EVA02(LogAgent):

    """Test the LogAgent."""

    def __init__(self):
        super(EVA02, self).__init__()

    class NotFound(Exception): pass

    def itr_solve(self, status):
        stat = status.clone
        h = 0
        list_of_actions = []
        new_moves = []
        output_moves = []
        start_hash = hash(repr(stat))
        stateMap = { start_hash: []}
        i = 0
        resetLimit = 2
        while not stat.check_goal():
            if i > resetLimit:
                stat = status.clone
                print("reset!!!", i)
                i = 0
                resetLimit = resetLimit*2
                if resetLimit > 64:
                    resetLimit = 2
            curr_hash = hash(repr(stat))
            for move in stat.moves:
                clone = stat.clone
                clone.execute([move])
                child_hash = hash(repr(clone))
                if child_hash not in stateMap[curr_hash]:
                    stateMap[curr_hash].append(child_hash)
                    if move not in new_moves:
                        new_moves.append(move)
                if child_hash not in stateMap:
                    stateMap[child_hash] = []
                    stateMap[child_hash].append(curr_hash)
            if(len(new_moves) > 0):
                move = random.choice(new_moves)
            else:
                i = i - 1 #così i non crese alla fine
                print("ooooops!")
                move = random.choice(stat.moves)
            stat.execute([move])
            new_moves = []
            goal_state = stat.clone
            goal_hash = hash(repr(stat))
            i = i+1
        print(len(stateMap))
        #print("should be True:",len(stateMap)==len(set(stateMap)))
        #asdasd
        
        i = 0
        limiter = 0
        resetLimit = 2
        curr_hash = goal_hash
        while curr_hash != start_hash:
            if i > resetLimit:
                stat = goal_state.clone
                print("Going back a little")
                i = 0
                resetLimit = resetLimit*5
                if resetLimit > 64:
                    resetLimit = 2
                    limiter = limiter+1
                if limiter > 10:
                    print("Limit break reached!")
                    break
            curr_hash = hash(repr(stat))
            for move in stat.moves:
                clone = stat.clone
                clone.execute([move])
                child_hash = hash(repr(clone))
                if child_hash not in stateMap[curr_hash]:
                    stateMap[curr_hash].append(child_hash)
                    if move not in new_moves:
                        new_moves.append(move)
                if child_hash not in stateMap:
                    stateMap[child_hash] = []
                    stateMap[child_hash].append(curr_hash)
            if(len(new_moves) > 0):
                move = random.choice(new_moves)
            else:
                i = i - 1 #così i non crese alla fine
                move = random.choice(stat.moves)
            stat.execute([move])
            new_moves = []
            #goal_hash = hash(repr(stat))
            i = i+1
        print(len(stateMap))
        
        #asdasd
        print("Finding path with minum number of steps")
        best_path = self.search_shortest_path(stateMap, start_hash, goal_hash)
        #print(start_hash, goal_hash)
        #best_path.pop()
        #print("best_path",best_path)
        i = 1
        clone = status.clone
        #print("should be True", start_hash == hash(repr(clone)))
        for i in range(1, len(best_path)):
            #print(i)
            stat = clone.clone
            #print("lista",stat.moves)
            for move in stat.moves:
                #print("each move:", move)
                clone = stat.clone
                clone.execute([move])
                child_hash = hash(repr(clone))
                #print(best_path[i], child_hash)
                if best_path[i] == child_hash:
                    #print("hey!")
                    output_moves.append(move)
                    break

            #i = i + 1
        #print(output_moves)
        return output_moves

    def search_shortest_path(self, graph, start, goal):
        """Find the shortest path from start to goal in graph (which must be a
        map from a node to an iterable of adjacent nodes), using
        breadth-first search.

            >>> graph = {
            ...     1: [2, 4, 5],  
            ...     2: [1],
            ...     3: [4, 6],
            ...     4: [2, 1, 3],
            ...     5: [],
            ...     6: [7],
            ...     7: [],
            ... }
            >>> search_shortest_path(graph, 1, 7)
            [1, 4, 3, 6, 7]
            >>> search_shortest_path(graph, 1, 1)
            [1]
            >>> search_shortest_path(graph, 5, 1) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
                ...
            NotFound: No path from 5 to 1

        """
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
        raise NotFound('No path from {} to {}'.format(start, goal))                

    def solve(self, status, goal):           
        return self.itr_solve(status)
"""
itrNum = 10
partialScore = 0
goalAlwaysReached = True
i = itrNum - 1
asd = LogEnvironment("testconfig.json")
asd.add_agent(MyAgent())
print(asd.check_goal())
asd.execute()
print("Goal reached?:",asd.check_goal())
i = 0
print("score is:", asd.formatted_score())
while(i<10):
    asd = asd.clone
    #print(hash(repr(asd)))
    #print(hash(repr(asd.clone)))
    i = i+1
"""

"""
while i < itrNum:
    asd = test_env  
    asd.add_agent(MyAgent())
    asd.check_goal()
    asd.execute()
    asd.check_goal()
    if(not asd.check_goal()):
        goalAlwaysReached = False
    print("score is:", asd.formatted_score())
    partialScore += asd.score()
    asd = None
    i += 1
meanScore = partialScore / itrNum
print("Mean score is:", meanScore)
if(not goalAlwaysReached):
    print("Goal not always reached")
"""