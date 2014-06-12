from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
#from heapq import nlargest
import bisect
from . priodict import priorityDictionary

import random
from collections import deque

class EVA13(LogAgent):

    """
    EVA13 LogAgent by Robert Parcus, 2014
    State space search using a variant of Uniform Cost Search (UCS).

    EVA13 adds partial solutions to the fringe only if they are better than
    a huge fraction of moves already seen.

    We do some graph prunning.

    We use an heuristic C() to calculate actions cost up to that partial result.

    We use an heuristic D() to estimate the distance between a certain
    status and the goal. It IS a semplification and it WILL underestimate
    the real distance.

    If H(x) = C(x) + D(x) is the total score of partial solution x, then
    we execute our expansions in ascending order starting from the partial
    solution with min(H(x)) each time, among those in the fringe.

    EVA13 will explore all solutions of equal, minimal cost until it reaches a
    goal state.

                            *****IMPORTANT*****
    This agent needs module priodict on its same folder.
                            *******************
    """

    def __init__(self):
        super(EVA13, self).__init__()

    class NotFound(Exception): pass

    def solve(self, status, goal):      
        start_hash = hash(repr(status))
        stateMap = [start_hash]
        return self.discovery_forwards(status.clone, stateMap)

    def discovery_forwards(self, status, stateMap):
        # we can't use deques here, insert() is supported only
        # on lists.
        fringe = []
        stat = status.clone
        start_hash = hash(repr(stat))
        current_moves = []

        relevant_objs = self.get_relevant_objs(status)
        distanceMap = self.make_airports_map(status)

        print("\n"*2)
        print("*"*60)
        print("\t", self.__doc__)
        print("\n"*2)

        if start_hash not in stateMap:
            stateMap.append(start_hash)
        cost_list = []
        while not stat.check_goal():
            curr_hash = hash(repr(stat))
            for move in stat.moves:
                #graph prunning
                if self.move_is_relevant(status, relevant_objs, move):
                    child = status.clone
                    new_move = current_moves + [move]
                    child.execute(new_move)
                    child_hash = hash(repr(child))
                    if child_hash not in stateMap:
                        stateMap.append(child_hash)
                        # We find the score of this moves list
                        move_score =  self.get_solution_cost(status, new_move)
                        move_score += 500*self.get_distance_from_goal(child, relevant_objs, distanceMap)
                        # we find the position this moves should take on the list
                        position = bisect.bisect_left(cost_list, move_score)
                        #if this move i among the x best moves I could do
                        if position < (len(fringe)/10)+10:
                            # we update the costs list
                            bisect.insort_left(cost_list, move_score)
                            # finally we insert the move on it's ordered position
                            fringe.insert(position, new_move)
                        if child.check_goal():
                            print("\n")
                            print("*"*60)
                            return new_move
            stat = status.clone
            # here we pop(0). From the left, like in BFS.
            current_moves = fringe.pop(0)
            # and we trow away the current_move cost from the list.
            print("\r\t","Current score:", cost_list.pop(0), "Fringe size:", len(fringe), "\t\t", end='')
            stat.execute(current_moves)
        print("\n")
        print("*"*60)
        return current_moves

    def get_relevant_objs(self, status):
        relevant_objs = {'planes':[], 'airports':[], 'boxes': []}
        planes = 'planes'
        airports = 'airports'
        boxes = 'boxes'
        for goal in status.goal:
            if goal in status.airports:
                    relevant_objs[airports].append(goal)
            if goal in status.airplanes:
                relevant_objs[planes].append(goal)
            for obj in status.goal[goal]:
                if obj in status.airports:
                    relevant_objs[airports].append(obj)
                if obj in status.airplanes:
                    relevant_objs[planes].append(obj)
                else:
                    relevant_objs[boxes].append(obj)
        relevant_objs[planes] = list(set(relevant_objs[planes]))
        relevant_objs[airports] = list(set(relevant_objs[airports])) 
        relevant_objs[boxes] = list(set(relevant_objs[boxes])) 
        return relevant_objs

    def make_airports_map(self,status):
        mappa = {}
        distanceMap = {}
        for airport in status.airports:
            mappa[airport] = {}
            for neighbour, distance in status.airports[airport]._neighbors.items():
                mappa[airport].update({neighbour: distance})
        #print("mappa!", mappa)
        # we get the distance of between all the airports
        for airport in status.airports:
            distanceMap[airport] = self.Dijkstra(mappa, airport)[0]
        # we can use the output like this : distanceMap["Airport_1"]["Airport_2"]
        return distanceMap

    def get_solution_cost(self, status, moves):
        cost = 0
        for move in moves:
            if move[0] =="load":
                cost += 15
            elif move[0] =="unload":
                cost += 10
            else:
                cost += 10*status.airports[move[2]].neighbors[move[3]]
        return cost

    def get_distance_from_goal(self, stat, relevant_objs, distanceMap):
        goal = stat.goal
        distance = 0

        for airport in stat.airports:
            for box in stat.airports[airport].boxes:
                if box in relevant_objs["boxes"]:
                    for destination in goal:
                        if destination in relevant_objs["airports"]:
                            if box in goal[destination]:
                                #print(airport, destination, "\n")
                                distance += distanceMap[airport][destination]
                        elif destination in relevant_objs["planes"]:
                            if box in goal[destination]:
                                for dest_airport in stat.airports:
                                    if destination in stat.airports[dest_airport].airplanes:
                                        distance += distanceMap[airport][dest_airport]+10
            for plane in stat.airports[airport].airplanes:
                if plane in relevant_objs["planes"]:
                    for destination in relevant_objs["airports"]:
                        if plane in goal[destination]:
                            #print(airport, destination, "\n")
                            distance += distanceMap[airport][destination]
                for box in stat.airports[airport].airplanes[plane].boxes:
                    if box in relevant_objs["boxes"]:
                        for destination in goal:
                            if destination in stat.airports:
                                if box in goal[destination]:
                                    #print(airport, destination, "\n")
                                    distance += distanceMap[airport][destination]
                            elif destination in stat.airplanes:
                                if box in goal[destination]:
                                    for dest_airport in stat.airports:
                                        if destination in stat.airports[dest_airport]:
                                            distance += distanceMap[airport][dest_airport]+25
        return distance

    def planeSpace(self, status, plane):
            return status.airplanes[plane].maxbox - len(status.airplanes[plane].boxes)

    def move_is_relevant(self, status, relevant_objs, move):
        action = move[0]
        obj = move[1]
        ########################################################
        #preparation code
        if action == "move":
            source = move[2]
            destination = move[3]
        elif action == "load":
            destination = move[2]
            for airport in status.airports:
                if destination in status.airports[airport].airplanes:
                    source = airport
        else:
            source = move[2]
            for airport in status.airports:
                if source in status.airports[airport].airplanes:
                    destination = airport
        ########################################################
        #end of preparation code
        if action == "load":
            if obj not in relevant_objs["boxes"]:
                return False
            else:
                # if the box is in the airport it should be 
                # why should you load it to a plane?
                for airport in status.airports:
                    if airport in relevant_objs["airports"]:
                        if obj in status.airports[airport].boxes:
                            if obj in status.goal[airport]:
                                return False
        elif action == "unload":
            if obj not in relevant_objs["boxes"]:
                if self.planeSpace(status, source):
                    return False
            elif source in status.goal and obj in status.goal[source]:
                if self.planeSpace(status, source):
                    return False
        return True

    #This NEEDS module priodict. ***IMPORTANT***
    def Dijkstra(self, G,start,end=None):
        D = {}  # dictionary of final distances
        P = {}  # dictionary of predecessors
        Q = priorityDictionary()   # est.dist. of non-final vert.
        Q[start] = 0
        
        for v in Q:
            D[v] = Q[v]
            if v == end: break
            
            for w in G[v]:
                vwLength = D[v] + G[v][w]
                if w in D:
                    if vwLength < D[w]:
                        raise ValueError
                #Dijkstra: found better path to already-final vertex
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v
        return (D,P)