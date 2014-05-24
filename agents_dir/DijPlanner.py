# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from collections import namedtuple
from itertools import permutations
from random import choice

__all__ = ["DijPlanner"]
TargetT = namedtuple("TargetT", ["obj", "t_place"])


class DijPlanner(LogAgent):

    """First planner."""

    def __init__(self):
        super(DijPlanner, self).__init__()
        self.reached_goals = list()

    @staticmethod
    def where_is(item, status, airport_only=False):
        print("### WHERE IS", item, "| airport_only:", airport_only)
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

    @staticmethod
    def check_single_goal(target, place_t, status):
        if place_t in status.airports:
            return target in status.airports[place_t]
        elif place_t in status.airplanes:
            return target in status.airplanes[place_t]
        return False

    def check_preconditions(self, status, goal, target, path):
        """Check preconditions.

        returns:
            -1 : No solution
             0 : preconditions OK
             1 : not good start status
        """
        if len(path) == 0:
            return -1
        elif path[-1][0] != self.where_is(self.get_target_place(goal, target), status, airport_only=True):
            print(path[-1][0], self.where_is(self.get_target_place(goal, target), status, airport_only=True))
            return -1
        elif len(status.airplanes) == 0:
            return -1
        if target in status.boxes and len(status.airports[self.where_is(target, status, airport_only=True)].airplanes) == 0:
            return 1
        return 0

    def h_function(self, status, goal, target, place_t, path):
        moves = list()
        place = self.where_is(
            self.get_target_place(goal, target), status, airport_only=True)
        print("-------------", place, place_t)
        real_place = self.where_is(self.get_target_place(goal, target), status)
        for move in status.moves:
            print("\t- Move", move)
            score = 0
            if target in move:
                score += 100
                print("\t\t!!! target IN move !!!")
            if place in move:
                score += 25
                print("\t\t!!! place IN move !!!")
            if real_place in move:
                score += 25
                print("\t\t!!! real_place IN move !!!")
            if place_t in move:
                score += 25
                print("\t\t!!! place_t IN move !!!")
            for node, dist in path:
                print("\t\t- node and dist", node, dist)
                if node in move:
                    score += dist
                    print("\t\t\t!!! node IN move !!!")
            if score != 0:
                moves.append((move, score))
        print("\t# Accepted moves:",
              sorted(moves, key=lambda elem: elem[1], reverse=True))
        return([move for move in sorted(moves, key=lambda elem: elem[1], reverse=True)])
        # print(len(moves), len(permutations(moves)))
        # for permutation in permutations(moves):
        #     print(permutation)

    def resolve(self, status, goal, anction_list, target, place_t):
        tmp_status = status
        print("##### TARGET and PLACE #####", target, place_t)
        dij_source = self.where_is(target, tmp_status, airport_only=True)
        dij_target = self.where_is(place_t, tmp_status, airport_only=True)
        path = self.dijkstra(tmp_status, dij_source, dij_target)
        print("### Dijkstra path", path)
        prec_ret = self.check_preconditions(tmp_status, goal, target, path)
        print("### Precontitions return:", prec_ret)
        timer = 0
        if prec_ret == 1:
            while self.check_preconditions(tmp_status, goal, target, path) == 1 and timer < 100:
                moves = list()
                neighbors = list()
                for move in tmp_status.moves:
                    for p_t, val, in path:
                        if p_t in move:
                            moves.append(move)
                            for neighbor in tmp_status.airports[p_t].neighbors:
                                neighbors.append(neighbor)
                                for neighbor_2 in tmp_status.airports[neighbor].neighbors:
                                    neighbors.append(neighbor_2)
                    for neighbor in neighbors:
                        if neighbor in move:
                            moves.append(move)
                    if place_t in move:
                        moves.append(move)
                next_move = choice(moves)
                clone = tmp_status.clone
                clone.execute([next_move])
                consistency = True
                for target, place_t in self.reached_goals:
                    consistency = consistency and self.check_single_goal(
                        target, place_t, clone)
                if consistency and self.check_preconditions(clone, goal, target, path) != -1:
                    tmp_status = clone
                    anction_list.append(next_move)
                timer += 1
        if prec_ret == -1:
            return None
        moves = self.h_function(tmp_status, goal, target, place_t, path)

        return tmp_status

    def solve(self, status, goal):
        print(status)
        anction_list = list()
        targetstuples = [TargetT(item, self.get_target_place(goal, item))
                         for list_ in goal.values() for item in list_]
        for target, place_t in targetstuples:
            if status is not None:
                status = self.resolve(
                    status, goal, anction_list, target, place_t)
        print("- #@#@# Action list:", anction_list)
        return anction_list
