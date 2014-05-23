# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from collections import namedtuple

__all__ = ["DijPlanner"]
TargetT = namedtuple("TargetT", ["obj", "t_place"])


class DijPlanner(LogAgent):

    """First planner."""

    def __init__(self):
        super(DijPlanner, self).__init__()

    @staticmethod
    def where_is(status, item, airport_only=False):
        print("### WHERE IS", item)
        if item in status.airports:
            return item
        for airport_name, airport_obj in status.airports.items():
            if item in airport_obj:
                return airport_name
            for airplane_name, airplane_obj in airport_obj.airplanes.items():
                if item in airplane_obj:
                    return airplane_name if not airport_only else airport_name

    @staticmethod
    def get_target_place(goal, target):
        for place, objs in goal.items():
            if target in objs:
                return place

    @staticmethod
    def dijkstra(status, source, target):
        """Search a path from a source to a targer."""
        try:
            from sys import maxint
        except ImportError:
            from sys import maxsize as maxint
        from random import choice
        print("### Dijkstra ---")
        dist = dict()
        prev = dict()
        for airport in status.airports:
            dist[airport] = maxint
            prev[airport] = None

        dist[source] = 0
        q_nodes = [name for name in status.airports]

        print("\t- SOURCE & TARGET", source, target)

        while len(q_nodes) > 0:
            print("\t\t- Q_NODES", q_nodes)
            print("\t\t- WHILE DIST", dist)
            smallest = choice(
                [vert for vert, val in dist.items()
                 if val == min([val_2 for vert_2, val_2 in dist.items() if vert_2 in q_nodes]) and vert in q_nodes])
            print("\t\t- Smallest", smallest)
            q_nodes.remove(smallest)
            if smallest == target:
                break
            if dist[smallest] == maxint:
                break

            for neighbor, weight in status.airports[smallest].neighbors.items():
                print("\t\t\t- FOR:", neighbor, weight)
                alt = dist[smallest] + weight
                print("\t\t\t- ALT:", alt)
                if alt < dist[neighbor]:
                    print("\t\t\t- IF:", alt, dist[neighbor])
                    dist[neighbor] = alt
                    prev[neighbor] = smallest

        print("\t- DIST", dist)
        print("\t- PREV", prev)

        result = list()
        result_points = list()
        tmp = target
        result.append(tmp)
        while prev[tmp] is not None:
            result.append(prev[tmp])
            tmp = prev[tmp]
        for elem in reversed(result):
            result_points.append(dist[elem] + 10)
        result = list(zip(reversed(result), reversed(result_points)))
        print("\t- RESULT", result)
        print("### ---")
        return result

    def check_preconditions(self, status, goal, target, path):
        """Check preconditions.

        returns:
            -1 : No solution
             0 : preconditions OK
             1 : not good start status
        """
        if len(path) == 0:
            return -1
        elif path[-1][0] != self.where_is(status, self.get_target_place(goal, target), airport_only=True):
            return -1
        elif len(status.airplanes) == 0:
            return -1
        if target in status.boxes and len(status.airports[self.where_is(status, target, airport_only=True)].airplanes) == 0:
            return 1
        return 0

    def h_function(self, status, goal, target, path):
        moves = [(move, 0) for move in status.moves]
        print(moves)

    def solve(self, status, goal):
        anction_list = list()
        places = goal.keys()
        targets = [item for list_ in goal.values() for item in list_]
        targetstuples = [TargetT(item, self.get_target_place(goal, item)) for list_ in goal.values() for item in list_]
        print("places:", places)
        print("targets:", targets)
        print("targetstuple", targetstuples)
        print("moves", status.moves)
        print("where is? Is in", self.where_is(status, targets[0]))
        path = self.dijkstra(status,
                      self.where_is(status, targets[0], airport_only=True),
                      self.where_is(status, self.get_target_place(goal, targets[0]), airport_only=True))
        print("Precontitions:", self.check_preconditions(status, goal, targets[0], path))
        return anction_list
