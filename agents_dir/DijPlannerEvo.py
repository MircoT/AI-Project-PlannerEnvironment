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
        self.reached_goals = list()
        self.__num_steps = 50
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
    def dijkstra(status, source, target):
        """Search a path from a source to a targer."""
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
        return cur_status, reached

    def solve(self, status, goal):
        """Override of the solve method of the LogAgent."""
        logging.debug("START OF SOLVE METHOD")
        anction_list = list()
        # Sorted by targets names.
        targetstuples = sorted([TargetT(item, self.get_target_place(goal, item))
                                for list_ in goal.values() for item in list_],
                               reverse=True,
                               key=lambda elem: elem[0])
        logging.debug("targetstuples = " + json.dumps(targetstuples, indent=4))
        for target, t_place in targetstuples:
            status, reached = self.resolve(
                status, goal, anction_list, target, t_place)
            if reached:
                self.reached_goals.append((target, t_place))
        logging.debug("anction_list = %s", json.dumps(anction_list, indent=4))
        return anction_list
