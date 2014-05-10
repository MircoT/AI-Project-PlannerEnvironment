# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from logEnvironmentModule import *

if __name__ == '__main__':
    test_env = LogEnvironment("testconfig.json")
    # print(test_env)

    class MyAgent(LogAgent):

        """Test the LogAgent."""

        def __init__(self):
            super(MyAgent, self).__init__()

        def solve(self, status, goal):
            print(status)
            print("GOAL:", status.get_goal())
            import json
            print(json.dumps(status.moves, indent=4))
            # print("STATUS:", status.Airport_1.airplanes)
            # print("STATUS:", status.Airport_2.airplanes)
            # for airplane in status.Airport_1.airplanes:
            #     print("PLANE:", airplane)
            # print("STATUS:", status.Airport_2.airplanes.Airplane_2.boxes)
            # print("GOAL:", goal)
            # print("GOAL Airplane_3:", goal.Airplane_3)
            # return [
            #     ("move", "Airplane_2", "Airport_2", "Airport_1"),
            #     ("load", "Box_7", "Airplane_3"),
            #     ("unload", "Box_4", "Airplane_1")
            # ]

    test_env.add_agent(MyAgent())
    print("Goal reached:", test_env.check_goal())
    test_env.execute()
    # print(test_env)
    print("Goal reached:", test_env.check_goal())
    print("Agent score:", test_env.score())
