# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *
from collections import namedtuple
from itertools import permutations 
from random import choice

__all__ = ["DijPlanner"]
TargetT = namedtuple("TargetT", ["obj", "t_place"])


class DijPlannerEvo(LogAgent):

    """First planner."""

    def __init__(self):
        super(DijPlannerEvo, self).__init__()
        self.reached_goals = list()
        self.__num_steps = 50

    def solve(self, status, goal):
        """Override of the solve method of the LogAgent."""

        print("##### START OF SOLVE METHOD")
        print(status)
        print()

        anction_list = list()
        # TO DO
        return anction_list
