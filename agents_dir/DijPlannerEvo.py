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
    def get_target_place(goal, target):
        """Get the place of the target from goal object."""
        for place, objs in goal.items():
            if target in objs:
                return place

    def resolve(self, status, goal, anction_list, target, t_place):
        """Method that solve a specific goal."""
        cur_status = status
        reached = False
        logging.debug("current target = %s | target place = %s", target, t_place)
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
