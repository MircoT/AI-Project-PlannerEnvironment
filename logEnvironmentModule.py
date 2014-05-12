# -*- encoding: utf-8 -*-
import json
import codecs
from errorObjs import *
from collections import namedtuple

__all__ = ["LogEnvironment", "LogAgent"]

Position = namedtuple('position', ['x', 'y'])


class DictAttr(dict):

    """A special dictionary that can be used with attributes."""

    def __init__(self, *args, **kwargs):
        super(DictAttr, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Box(object):

    """Class for boxes objects."""

    id_num = 0

    def __init__(self, name=None):
        self._name = self.__get_name() if name is None else name

    @staticmethod
    def __get_name():
        """Get a prefixed name for the object."""
        Box.id_num += 1
        return "Box_{0}".format(Box.id_num)

    def __getattr__(self, attr):
        if attr == "name":
            return self._name

    def __repr__(self):
        return "{0}".format(self._name)


class Airplane(object):

    """Class for airplanes objects."""

    id_num = 0

    def __init__(self, name=None, maxbox=10):
        self._name = self.__get_name() if name is None else name
        self._boxes = DictAttr()
        self._maxbox = maxbox

    @staticmethod
    def __get_name():
        """Get a prefixed name for the object."""
        Airplane.id_num += 1
        return "Airplane_{0}".format(Airplane.id_num)

    def __contains__(self, key):
        return key in self._boxes

    def __getattr__(self, attr):
        if attr == "name":
            return self._name
        elif attr == "maxbox":
            return self._maxbox
        elif attr == "boxes":
            return self._boxes

    def __repr__(self):
        string = "{0} with {1}/{2} boxes: [".format(
            self._name, len(self._boxes), self._maxbox)
        for box in sorted(self._boxes.values(),
                          key=lambda obj: obj.name):
            string += "{0}, ".format(box)
        string = string[:-2] + "]"
        return string

    def set_max_box(self, max_):
        """Set the maximum number of boxes that the airplane can transport."""
        self._maxbox = max_

    def add_box(self, box):
        """Add a box to the airplane (only for environment initialization)."""
        if len(self._boxes) < self._maxbox:
            self._boxes[box.name] = box
        else:
            raise AirplaneMaxBoxExided(self)


class Airport(object):

    """Class for airports objects."""

    id_num = 0

    def __init__(self, name=None, position=None):
        self._position = Position(
            0, 0) if position is None else Position(*position)
        self._name = self.__get_name() if name is None else name
        self._boxes = DictAttr()
        self._airplanes = DictAttr()
        self._neighbors = DictAttr()

    @staticmethod
    def __get_name():
        """Get a prefixed name for the object."""
        Airport.id_num += 1
        return "Airport_{0}".format(Airport.id_num)

    def __contains__(self, key):
        return key in self._boxes or key in self._airplanes

    def __getattr__(self, attr):
        if attr == "name":
            return self._name
        elif attr == "position":
            return self._position
        elif attr == "neighbors":
            return self._neighbors
        elif attr == "boxes":
            return self._boxes
        elif attr == "airplanes":
            return self._airplanes
        elif attr == "edges":
            return self._neighbors

    def __repr__(self):
        string = "{0} at {1} {{\n".format(self._name, self._position)
        string += "\tboxes:\n".format(len(self._boxes))
        for box in sorted(self._boxes.values(),
                          key=lambda obj: obj.name):
            string += "\t\t- {0}\n".format(box)
        string += "\tairplanes:\n".format(len(self._boxes))
        for airplane in sorted(self._airplanes.values(),
                               key=lambda obj: obj.name):
            string += "\t\t- {0}\n".format(airplane)
        string += "\tneighbors:\n".format(len(self._boxes))
        for airport_name, weight in sorted(self._neighbors.items()):
            string += "\t\t- {0} -> {1}\n".format(airport_name, weight)
        string += "}"
        return string

    def set_position(self, position):
        """Set position of the airport (only for environment initialization)."""
        self._position = Position(*position)

    def add_link(self, airport_name, weight=1):
        """Add a link between airports (only for environment initialization)."""
        self._neighbors[airport_name] = weight

    def add_airplane(self, airplane):
        """Add an airplane to the airport (only for environment initialization)."""
        self._airplanes[airplane.name] = airplane

    def add_box(self, box):
        """Add a box to the airport (only for environment initialization)."""
        self._boxes[box.name] = box


class LogAgent(object):

    """Agent for LogEnvironment"""

    def __init__(self):
        self.score = 0
        self.moves = 0

    def solve(self, status, goal):
        """Virtual method called from the environment.

        This method must return a list of tuples, like this:

        [(method name, *args)]

        Arguments depend on called method.
        """
        pass

    def get_score(self):
        return "Score of {0} in {1} moves!".format(self.score, self.moves)


class LogEnvironment(object):

    """Class that represent the world for the simulation."""

    def __init__(self, json_file=None, obj=None):
        self.__allowed_methods = ["load", "unload", "move"]
        self._airports = DictAttr()
        self._airplanes = DictAttr()
        self._boxes = DictAttr()
        self._goal = list()
        self._agent = None
        temp_airplanes = dict()
        temp_boxes = dict()
        if obj is not None and isinstance(obj, LogEnvironment):
            for box in obj.boxes:
                self._boxes[box] = Box(box)
            for airplane, air_obj in obj.airplanes.items():
                self._airplanes[airplane] = Airplane(airplane, air_obj.maxbox)
                for box in air_obj.boxes:
                    self._airplanes[airplane].add_box(self._boxes[box])
            for airport, airport_obj in obj.airports.items():
                self._airports[airport] = Airport(airport)
                self._airports[airport].set_position(airport_obj.position)
                for box in airport_obj.boxes:
                    self._airports[airport].add_box(self._boxes[box])
                for airplane in airport_obj.airplanes:
                    self._airports[airport].add_airplane(
                        self._airplanes[airplane])
                for neighbor, weight in airport_obj.neighbors.items():
                    self._airports[airport].add_link(neighbor, weight)
            self._goal = [elem for elem in obj.goal_list]
            del self._agent
        if json_file is not None:
            with codecs.open(json_file, 'r', 'utf-8') as fsj:
                config = json.load(fsj)
            initial_status = config['initial_status']
            if isinstance(initial_status['airports'], list):
                pass
            else:
                for num in range(0, initial_status['airports']):
                    new_airport = Airport()
                    self._airports[new_airport.name] = new_airport
            if isinstance(initial_status['airplanes'], list):
                pass
            else:
                for num in range(0, initial_status['airplanes']):
                    new_airplane = Airplane()
                    self._airplanes[new_airplane.name] = new_airplane
                    temp_airplanes[new_airplane.name] = new_airplane
            if isinstance(initial_status['boxes'], list):
                pass
            else:
                for num in range(0, initial_status['boxes']):
                    new_box = Box()
                    self._boxes[new_box.name] = new_box
                    temp_boxes[new_box.name] = new_box
            self.__add_edges(
                initial_status['edges'])
            self.__add_vertices(
                initial_status['vertices'], temp_airplanes, temp_boxes)
            # Setup goal
            for sentence in config['goal']:
                objs, in_ = [
                    string.strip() for string in sentence.split("in")]
                objs = [string.strip()
                        for string in objs.split(",")]
                self._goal.append((objs, in_))
            self.__verify_goal()

    def __getattr__(self, attr):
        if attr == "airports":
            return self._airports
        elif attr == "airplanes":
            return self._airplanes
        elif attr == "boxes":
            return self._boxes
        elif attr == "goal_list":
            return self._goal
        elif attr == "goal":
            return self.get_goal()
        elif attr == "clone":
            return self.get_status()
        elif attr == "moves":
            return self.__moves()

    def __eq__(self, obj):
        return self.__repr__() == obj.__repr__()

    def __ne__(self, obj):
        return not self == obj

    def __repr__(self):
        string = "----- Environment -------\n"
        for airport_name in sorted(self._airports):
            string += "{0}".format(self._airports[airport_name])
            string += "\n"
        string += "-------------------------"
        return string

    def __moves(self):
        """Returns a list of all possible moves from current status."""
        list_ = list()
        for airport_name, airport_obj in self.airports.items():
            if len(airport_obj.boxes) > 0 and len(airport_obj.airplanes) > 0:
                for box in airport_obj.boxes:
                    for airplane_name, airplane in airport_obj.airplanes.items():
                        if len(airplane.boxes) < airplane.maxbox:
                            list_.append(("load", box, airplane_name))
            if len(airport_obj.airplanes) > 0:
                for airplane_name, airplane in airport_obj.airplanes.items():
                    if len(airplane.boxes) > 0:
                        for box in airplane.boxes:
                            list_.append(("unload", box, airplane_name))
                    for airport_target in self.airports:
                        if airport_target != airport_name and\
                           airport_target in airport_obj.edges:
                            list_.append(
                                ("move", airplane_name, airport_name, airport_target))
        return list_

    def __add_edges(self, edges):
        """Add edges."""
        for airport_name in edges:
            if airport_name not in self._airports:
                raise AirplaneNotExist(airport_name)
            for edge, weight in edges[airport_name].items():
                if edge not in self._airports:
                    raise AirplaneNotExist(edge)
                self._airports[airport_name].add_link(edge, weight)
                self._airports[edge].add_link(airport_name, weight)

    def __add_vertices(self, vertices, temp_airplanes, temp_boxes):
        """Add vertices."""
        for airport_name in vertices:
            if airport_name not in self._airports:
                raise AirplaneNotExist(airport_name)
            airport = vertices[airport_name]
            if 'position' in airport:
                self._airports[airport_name].set_position(
                    airport['position'])
            if 'boxes' in airport:
                for box_name in airport['boxes']:
                    if box_name in temp_boxes:
                        self._airports[airport_name].add_box(
                            temp_boxes.pop(box_name))
                    else:
                        raise BoxAlreadyAssigned(box_name)
            if 'airplanes' in airport:
                for airplane_name in airport['airplanes']:
                    if airplane_name not in temp_airplanes:
                        raise AirplaneAlreadyAssigned(airplane_name)
                    temp_airplanes[airplane_name].set_max_box(
                        airport['airplanes'][airplane_name]['maxbox'])
                    if 'boxes' in airport['airplanes'][airplane_name]:
                        for box_name in airport['airplanes'][airplane_name]['boxes']:
                            if box_name in temp_boxes:
                                temp_airplanes[airplane_name].add_box(
                                    temp_boxes.pop(box_name))
                            else:
                                raise BoxAlreadyAssigned(box_name)
                    self._airports[airport_name].add_airplane(
                        temp_airplanes.pop(airplane_name))

    def get_status(self):
        """Return the current status to the agent."""
        return LogEnvironment(obj=self)

    def get_goal(self):
        """The the goal status."""
        goal = DictAttr()
        for objs, dir_ in self._goal:
            goal[dir_] = [obj for obj in objs]
        return goal

    def __verify_goal(self):
        """Verify if the goal is plausible."""
        temp = dict()
        already_visited = list()
        for objs, dir_ in self._goal:
            temp[dir_] = set([obj for obj in objs])
        for key in temp:
            already_visited.append(key)
            for compare in [key_c for key_c in temp if key_c not in already_visited]:
                if len(temp[key] & temp[compare]) != 0:
                    raise GoalNotPlausible()

    def check_goal(self):
        """Check if the goal is reached."""
        results = True
        for objs, dir_ in self._goal:
            if dir_ in self._airports:
                for obj in objs:
                    results = results and obj in self._airports[dir_]
            elif dir_ in self._airplanes:
                for obj in objs:
                    results = results and obj in self._airplanes[dir_]
        return results

    def load(self, box, airplane_name):
        """Load a box in an airplane."""
        if box not in self._boxes or\
                airplane_name not in self._airplanes:
            if getattr(self, "_agent", False):
                self._agent.score -= 100
        else:
            temp_name = None
            for airport_name, airport in self._airports.items():
                if airplane_name in airport:
                    temp_name = airport_name
            if box in self._airports[temp_name].boxes:
                self._airports[temp_name].airplanes[airplane_name].add_box(
                    self._airports[temp_name].boxes.pop(box))
                if getattr(self, "_agent", False):
                    self._agent.score += 10
                    self._agent.moves += 1

    def unload(self, box, airplane_name):
        """Unload a box from an airplane to the airport."""
        if box not in self._boxes or\
                airplane_name not in self._airplanes:
            if getattr(self, "_agent", False):
                self._agent.score -= 100
        else:
            temp_name = None
            for airport_name, airport in self._airports.items():
                if airplane_name in airport:
                    temp_name = airport_name
            if box in self._airports[temp_name].airplanes[airplane_name].boxes:
                self._airports[temp_name].add_box(
                    self._airports[temp_name].airplanes[airplane_name].boxes.pop(box))
                if getattr(self, "_agent", False):
                    self._agent.score += 10
                    self._agent.moves += 1

    def move(self, airplane_name, from_, to_):
        """Move an airplane from an airport to another airport."""
        if from_ not in self._airports or\
            to_ not in self._airports or\
                airplane_name not in self._airplanes:
            if getattr(self, "_agent", False):
                self._agent.score -= 100
        else:
            if from_ in self._airports[to_].edges:
                self._airports[to_].airplanes[airplane_name] = self._airports[
                    from_].airplanes.pop(airplane_name)
                if getattr(self, "_agent", False):
                    self._agent.score += 10 * self._airports[to_].edges[from_]
                    self._agent.moves += 1
            else:
                raise LinkNotExist(from_, to_)

    def add_agent(self, agent):
        """Add an agent to the environment."""
        if isinstance(agent, LogAgent):
            self._agent = agent

    def execute(self, list_=None):
        """Execute the solution of the agent."""
        if getattr(self, "_agent", False):
            if self._agent is not None:
                actions = self._agent.solve(self.get_status(), self.get_goal())
                if isinstance(actions, list):
                    for action in actions:
                        method, args = action[0], action[1:]
                        if method in self.__allowed_methods:
                            func = getattr(self, method, None)
                            if callable(func):
                                func(*args)
        else:
            if isinstance(list_, list):
                for action in list_:
                    method, args = action[0], action[1:]
                    if method in self.__allowed_methods:
                        func = getattr(self, method, None)
                        if callable(func):
                            func(*args)
            else:
                raise ActionNotAList()

    def score(self):
        """Return the agent's score."""
        return self._agent.get_score()
