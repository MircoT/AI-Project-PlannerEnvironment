# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from logEnvironmentModule import *
from errorObjs import *


if __name__ == '__main__':
    test_env = LogEnvironment("testconfig_simple.json")

    class MyAgent(LogAgent):

        """Test the LogAgent."""

        def __init__(self):
            super(MyAgent, self).__init__()

        def solve(self, status, goal):
            clone = status.clone
            print("----- Print of CLONE -----")
            print(clone)
            print("CLONE AIRPORTS:", clone.airports)
            print("CLONE AIRPLANES:", clone.airplanes)
            print("CLONE BOXES:", clone.boxes)
            print("-------------------------")

            print("----- Print details of CLONE -----")
            for airport in clone.airports:
                print(airport)
            for airport_name, airport_obj in clone.airports.items():
                print("AIRPORT NAME:", airport_name)
                print(airport_obj)
            for box in clone.airports.Airport_1.boxes:
                print("BOX NAME", box)
            for airplane in clone.airports.Airport_1.airplanes:
                print("AIRPLANE NAME:", airplane)
            for box in clone.airports.Airport_1.airplanes.Airplane_1.boxes:
                print("BOX NAME", box)
            print("-------------------------")

            print("-->STASUS == CLONE:", status == clone)
            print("-->GOAL:", status.goal)
            print("-->CLONE MOVES:", clone.moves)

            list_of_actions = [action for action in clone.moves]

            print("-->EXECUTE MOVES IN CLONE:", list_of_actions)

            clone.execute(list_of_actions)

            print("-->STASUS == CLONE:", status == clone)
            print("-->CHECK GOAL IN CLONE:", clone.check_goal())

            new_clone = clone.clone

            print("-->NEW CLONE")
            print("-->STASUS != CLONE:", status != clone)
            print("-->STASUS == NEW_CLONE:", status == new_clone)
            print("-->NEW_CLONE == CLONE:", new_clone == clone)

            for box in clone.airports.Airport_2.airplanes.Airplane_1.boxes:
                print("-->BOX in Airplane_1 in Airport_2:", box)

            print("-->NEW_CLONE MOVES:", new_clone.moves)
            print("-->LAST MOVE CHECK:",
                  new_clone.moves[0] == ("unload", "Box_1", "Airplane_1"))

            try:
                new_clone.execute(("unload", "Box_1", "Airplane_1"))
            except ActionNotAList as e:
                print("-->!!! ERROR:", e)
                new_clone.execute([("unload", "Box_1", "Airplane_1")])

            print("-->CHECK GOAL IN NEW_CLONE", new_clone.check_goal())
            print("-------------------------")

            list_of_actions.append(("unload", "Box_1", "Airplane_1"))
            return list_of_actions

    test_env.add_agent(MyAgent())
    print("MAIN Goal reached:", test_env.check_goal())
    test_env.execute()
    print("MAIN Goal reached:", test_env.check_goal())
    print("MAIN Agent score:", test_env.score())
