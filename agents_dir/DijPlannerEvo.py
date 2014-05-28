# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from collections import namedtuple
from random import choice
import logging
import json

__all__ = ["DijPlannerEVO"]
TargetT = namedtuple("TargetT", ["target", "place"])


class DijPlannerEvo(LogAgent):

    """First planner."""

    def __init__(self):
        super(DijPlannerEvo, self).__init__()
        # dict of the last actions (reversed) for each goal
        self.last_goals_moves = dict()
        self.max_timer = 100
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s - Method(%(funcName)s) at line %(lineno)s: %(message)s")

    @staticmethod
    def where_is(item, status):
        """Check where is an item."""
        result = None
        if item in status.airports:
            result = item
        for airport_name, airport_obj in status.airports.items():
            if item in airport_obj:
                result = airport_name
            for airplane_name, airplane_obj in airport_obj.airplanes.items():
                if item in airplane_obj:
                    result = airplane_name
        logging.debug("item %s is in %s", item, result)
        return result

    @staticmethod
    def which_airport(item, status):
        """Check in which airport is an item."""
        result = None
        if item in status.airports:
            result = item
        for airport_name, airport_obj in status.airports.items():
            if item in airport_obj:
                result = airport_name
            for airplane_name, airplane_obj in airport_obj.airplanes.items():
                if item in airplane_obj:
                    result = airport_name
        logging.debug("item %s is in airport %s", item, result)
        return result

    @staticmethod
    def get_target_place(goal, target):
        """Get the place of the target from goal object."""
        for place, objs in goal.items():
            if target in objs:
                return place

    @staticmethod
    def check_single_goal(target, t_place, status):
        """Check if a single goal is reached."""
        if t_place in status.airports:
            return target in status.airports[t_place]
        elif t_place in status.airplanes:
            return target in status.airplanes[t_place]
        return False

    @staticmethod
    def dijkstra(status, source, target):
        """Search a path from a source to a target"""
        try:
            from sys import maxint
        except ImportError:
            from sys import maxsize as maxint

        logging.debug("Start of dijkstra!")

        dist = dict()
        prev = dict()
        for airport in status.airports:
            dist[airport] = maxint
            prev[airport] = None

        dist[source] = 0
        q_nodes = [name for name in status.airports]

        while len(q_nodes) > 0:

            logging.debug("Q_NODES = %s", json.dumps(q_nodes, indent=4))
            logging.debug("DIST = %s", json.dumps(dist, indent=4))

            smallest = choice(
                [vert for vert, val in dist.items()
                 if val == min([val_2 for vert_2, val_2 in dist.items() if vert_2 in q_nodes]) and vert in q_nodes])

            logging.debug("Smallest = %s", smallest)

            q_nodes.remove(smallest)
            if smallest == target:
                break
            if dist[smallest] == maxint:
                break

            for neighbor, weight in status.airports[smallest].neighbors.items():

                logging.debug("FOR neighbor = %s | weight = %s",
                              neighbor, weight)

                alt = dist[smallest] + weight

                logging.debug("ALT = %s", alt)

                if alt < dist[neighbor]:

                    logging.debug("IF alt %s with neighbors = %s",
                                  alt, json.dumps(dist[neighbor], indent=4))

                    dist[neighbor] = alt
                    prev[neighbor] = smallest

        logging.debug("DIST = %s", json.dumps(dist, indent=4))
        logging.debug("PREV = %s", json.dumps(prev, indent=4))

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

        logging.debug("RESULT = %s", json.dumps(result, indent=4))
        logging.debug("End of dijkstra!")

        return result

    def __verify_preconditions(self, status, goal, target, dij_path):
        """Verifies preconditions.

        returns:
            -1 : No solution
             0 : preconditions OK
             1 : not good start status
        """
        if len(dij_path) == 0:  # Empty list of moves
            logging.debug("Empty list of moves!")
            return -1
        # End path must be equal to the goal place
        elif dij_path[-1][0] != self.which_airport(self.get_target_place(goal, target), status):
            logging.debug("End path not equal to the goal place!")
            return -1
        elif len(status.airplanes) == 0:  # If there are no airplanes
            logging.debug("There are no airplanes!")
            return -1
        t_place = self.get_target_place(goal, target)

        # If there are no airplanes in the airport of the box
        if target in status.boxes and len(status.airports[self.which_airport(target, status)].airplanes) == 0:
            logging.debug(
                "There are no airplanes on the airport of the target box!")
            return 1
        # If the target place is a full airplane
        elif t_place in status.airplanes and len(status.airplanes[t_place].boxes) == status.airplanes[t_place].maxbox:
            logging.debug("The target place is a full airplane!")
            return 1
        return 0

    def preconditions_h_function(self, status, goal, target, t_place, path):
        """Heuristic function for preconditions."""
        moves_list = list()
        neighbors = list()
        full_airplanes = list()
        for airport, value in path:
            neighbors.append(airport)
            for near_1 in status.airports[airport].neighbors:
                neighbors.append(near_1)
                for near_2 in status.airports[near_1].neighbors:
                    neighbors.append(near_2)
        for airplane_name, airplane_obj in status.airplanes.items():
            if len(airplane_obj.boxes) == airplane_obj.maxbox:
                full_airplanes.append(airplane_name)
        for move in status.moves:
            score = 0
            if move in self.last_goals_moves:
                score -= 250
            if move[0] == "load":
                score -= 100
            if t_place in move:
                score += 10
            for neighbor in neighbors:
                if neighbor in move:
                    score += 10
            for airplane in full_airplanes:
                if airplane in move:
                    score += 10
                if move[0] == "unload":
                    score += 50
            moves_list.append((move, score))
        moves_list = list(sorted([(move, score)
                          for move, score in moves_list if score > 0],
                          key=lambda elem: elem[1], reverse=True))
        return moves_list

    def check_preconditions(self, status, goal, target, t_place, dij_path):
        """Checks preconditions for current target."""
        timer = 0
        moves_list = list()
        clone = cur_status.clone
        while self.__verify_preconditions(clone, goal, target, dij_path) == 1 and timer < self.max_timer:
            moves = self.preconditions_h_function(
                cur_status, goal, target, t_place, dij_path)
            logging.debug("prec moves: %s", moves)
            next_move, weight = moves.pop(0)
            moves_list.append(next_move)
            clone.execute(next_move)
            timer += 1
        if timer == self.max_timer:
            logging.debug("check preconditions FAIL!")
            return status, []
        else:
            return clone, moves_list

    def resolve(self, status, goal, anction_list, target, t_place):
        """Method that solve a specific goal."""
        cur_status = status
        reached = False

        logging.debug("current target = %s | target place = %s",
                      target, t_place)

        dij_source = self.which_airport(target, cur_status)
        dij_target = self.which_airport(t_place, cur_status)

        logging.debug("dij_source = %s | dij_target = %s",
                      dij_source, dij_target)

        dij_path = self.dijkstra(cur_status, dij_source, dij_target)
        cur_status, prec_moves = self.check_preconditions(
            cur_status, goal, target, t_place, dij_path)
        return cur_status, reached

    def solve(self, status, goal):
        """Override of the solve method of the LogAgent."""

        logging.debug("START OF SOLVE METHOD")

        cur_status = status
        anction_list = list()
        boxes_in_airplanes = list()
        boxes_in_airports = list()
        airplanes_in_airports = list()

        for place, targets in goal.items():
            for target in targets:
                if target in status.boxes:
                    if place in status.airplanes:
                        boxes_in_airplanes.append(TargetT(target, place))
                    elif place in status.airports:
                        boxes_in_airports.append(TargetT(target, place))
                elif target in status.airplanes:
                    airplanes_in_airports.append(TargetT(target, place))

        # Sorted by targets names.
        targetstuples = boxes_in_airplanes + \
            boxes_in_airports + airplanes_in_airports

        logging.debug("targetstuples = " + json.dumps(targetstuples, indent=4))

        for target, t_place in targetstuples:
            cur_status, reached = self.resolve(
                cur_status, goal, anction_list, target, t_place)
            if reached:
                self.reached_goals.append((target, t_place))
        logging.debug("anction_list = %s", json.dumps(anction_list, indent=4))
        return anction_list
