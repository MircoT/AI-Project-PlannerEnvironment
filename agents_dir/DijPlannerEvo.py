# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from collections import namedtuple
from random import choice
import logging

__all__ = ["DijPlannerEVO"]
TargetT = namedtuple("TargetT", ["obj", "t_place"])


class DijPlannerEvo(LogAgent):

    """First planner."""

    def __init__(self):
        super(DijPlannerEvo, self).__init__()
        self.reached_goals = list()
        self.__num_steps = 50
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s - Method(%(funcName)s) at line %(lineno)s: %(message)s")

    def solve(self, status, goal):
        """Override of the solve method of the LogAgent."""
        logging.debug("START OF SOLVE METHOD")
        anction_list = list()
        # TO DO
        return anction_list
