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

    def weighted_random(self, pairs):
        total = sum(pair[0] for pair in pairs)
        r = random.randint(1, total)
        for (weight, value) in pairs:
            r -= weight
            if r <= 0: return value

    def get_relevant_objs(self, status):
        relevant_objs = {'planes':[], 'airports':[], 'boxes': []}
        planes = 'planes'
        airports = 'airports'
        boxes = 'boxes'
        for goal in status.goal:
            #print('goal',goal)
            #print('status.goal[goal]',status.goal[goal])
            if goal in status.airplanes:
                relevant_objs[planes].append(goal)
            if goal in status.airports:
                relevant_objs[airports].append(goal)
            if isinstance(status.goal[goal], list):
                relevant_objs[boxes].extend(status.goal[goal])
            relevant_objs[planes] = list(set(relevant_objs[planes]))
            relevant_objs[airports] = list(set(relevant_objs[airports])) 
            relevant_objs[boxes] = list(set(relevant_objs[boxes])) 
        return relevant_objs 

    def get_relevance(self, status, relevant_objs, move):
        relevance = 0
        #print(move)
        #print(relevant_objs)
        #print(move[1])
        if move[0] == "unload":
            relevance = self.weighted_random([(1,1),(9,0)])
            # if the box is relevant somehow
            if move[1] in relevant_objs["boxes"]:
                relevance = 2
            # if the plane is relevant somehow
            if  move[2] in relevant_objs["planes"]:
                relevance = 1
                #if the box is in the plane it should be
                if move[1] in status.goal[move[2]]:
                    relevance = self.weighted_random([(9,1),(1,0)])
                    #print(relevance)
        elif move[0] == "load":
            relevance = self.weighted_random([(7,1),(3,0)])
            #if the plane is somehow relevant
            if  move[2] in relevant_objs["planes"]:
                relevance = 1
            #if te box is not relevant, never load it!
            if move[1] not in relevant_objs["boxes"]:
                relevance = 0
            else:
                # if the box is in the airport it should be 
                # why should you load it to a plane?
                for airport in status.airports:
                    if airport in relevant_objs["airports"]:
                        if move[1] in status.airports[airport].boxes:
                            if move[1] in status.goal[airport]:
                                #print("i work!!!!!!!")
                                relevance = 0
        else:
            relevance = self.weighted_random([(7,1),(3,0)])
            """if move[3] in relevant_objs:
                relevance = relevance + 10
            if move[2] in relevant_objs:
                relevance = relevance - 5
            if move[1] in relevant_objs:
                relevance = relevance * 5"""
        return relevance

    def discovery_forwards(self, status, relevant_objs, stateMap):
        stat = status.clone
        list_of_actions = []
        new_moves = []
        relevant_moves = []
        output_moves = []
        start_hash = hash(repr(stat))
        foundEarlier = None
        if start_hash not in stateMap:
            stateMap[start_hash] = []
        #stateMap = { start_hash: []}
        i = 0
        maxDepth = 4
        resetLimit = 2
        while not stat.check_goal():
            if i > resetLimit:
                #################
                #stat = status.clone
                stat = clone.clone
                print("\r\t", "Searching:", "*"*i, end='')
                i = 0
                resetLimit = resetLimit*1.3
                if resetLimit > maxDepth:
                    ###########
                    stat = status.clone
                    ###########
                    resetLimit = 1
                    maxDepth += 1
            curr_hash = hash(repr(stat))
            if curr_hash not in stateMap:
                stateMap[curr_hash] = []
            for move in stat.moves:
                #print(move)
                relevance = self.get_relevance(status, relevant_objs, move) 
                #print(relevance)
                if relevance > 0:
                    relevant_moves.append(move)
                    #print("sometimes we are relevant")
                    clone = stat.clone
                    clone.execute([move])
                    child_hash = hash(repr(clone))
                    #print("test")
                    if child_hash not in stateMap[curr_hash]:
                        stateMap[curr_hash].append(child_hash)
                        if move not in new_moves:
                            new_moves.append(move)
                    if child_hash not in stateMap:
                        stateMap[child_hash] = []
                        stateMap[child_hash].append(curr_hash)
                    if clone.check_goal():
                        #print("OGMOMGOMGOMGOMGOMGOMG")
                        foundEarlier = move
                        break
                #print("no relevant move!!!!")
            #print("number of relevances", relevants)
            #print("mmmm", i)
            if foundEarlier:
                move = foundEarlier
            elif(len(new_moves) > 0):
                move = random.choice(new_moves)
            else:
                i = i - self.weighted_random([(50,1),(50,0)])
                #print("ooooops!", i)
                if len(relevant_moves) > 0:
                    move = random.choice(relevant_moves)
                else:
                    move = random.choice(stat.moves)
            #print(move)
            #print(move)
            stat.execute([move])
            new_moves = []
            relevant_moves = []
            goal_state = stat.clone
            goal_hash = hash(repr(stat))
            i = i+1
        print(len(stateMap))
        return {'stateMap': stateMap, 'goal_hash': goal_hash, 'goal_state': goal_state, 'start_hash': start_hash, 'stat': stat}

    def discovery_backwards(self, status, stateMap, start_hash, curr_hash):
        stat = status.clone
        new_moves = []
        i = 0
        limiter = 0
        resetLimit = 2
        #curr_hash = goal_hash
        while curr_hash != start_hash:
            if i > resetLimit:
                stat = status.clone
                i = 0
                resetLimit = resetLimit*8
                if resetLimit > 16:
                    resetLimit = 2
                    print( "\r", "Going back a little:", limiter,"%", end='')
                    limiter = limiter + 1
                if limiter > 100:
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
                i = i - 1 #così i non cresce alla fine
                move = random.choice(stat.moves)
            stat.execute([move])
            new_moves = []
            #goal_hash = hash(repr(stat))
            i = i+1
        print(len(stateMap))
        return  stateMap

    def itr_solve(self, status):
        #print(dir(status.goal[goal]))
        relevant_objs = self.get_relevant_objs(status)
        #print(relevant_objs)
        start_hash = hash(repr(status))
        stateMap = {start_hash: []}
        for x in range(3):
            tmp = self.discovery_forwards(status.clone, relevant_objs, stateMap)
            #{'statemap': statemap, 'goal_hash': goal_hash, 'goal_state': goal_state, 'start_hash': start_hash}
            stateMap = tmp["stateMap"]
            goal_hash = tmp["goal_hash"]
            goal_state = tmp["goal_state"]
            start_hash = tmp["start_hash"]
            stat = tmp['stat']
        #asdasd
        stateMap = self.discovery_backwards(goal_state.clone, stateMap, start_hash, goal_hash)
        print("Finding path with minum number of steps")
        best_path = self.search_shortest_path(stateMap, start_hash, goal_hash)
        #print(start_hash, goal_hash)
        #best_path.pop()
        #print("best_path",best_path)
        i = 1
        output_moves = []
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
        """
                                print(status)
                                print(goal)
                                print(status.moves)
                                return 
                                """
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