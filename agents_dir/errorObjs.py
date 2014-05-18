"""
    This contains all error handling functions for the
    logistic Environment Module.
"""

class Error(Exception):

    """Base class for exceptions in this module."""

    pass


class ActionNotAList(Error):

    """Exception raised when goal is not plausible."""

    def __str__(self):
        return "Actions passed is not a list!"


class GoalNotPlausible(Error):

    """Exception raised when goal is not plausible."""

    def __str__(self):
        return "Goal is NOT plausible!"


class AirplaneMaxBoxExided(Error):

    """Exception raised for errors in the airplanes when a box is added."""

    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return "{0} max boxes exceeded!".format(self.obj)


class BoxAlreadyAssigned(Error):

    """Exception raised for errors in the assignment of boxes."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{0} already assigned or not exist!".format(self.name)


class AirplaneNotExist(Error):

    """Exception raised for errors in the assignment of airplanes."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{0} not exist!".format(self.name)


class AirplaneAlreadyAssigned(Error):

    """Exception raised for errors in the assignment of airplanes."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{0} already assigned or not exist!".format(self.name)


class LinkNotExist(Error):

    """Exception raised when two airport are not linked."""

    def __init__(self, from_, to_):
        self.from_ = from_
        self.to_ = to_

    def __str__(self):
        return "Link from {0} to {1} not exist!".format(self.from_, self.to_)
