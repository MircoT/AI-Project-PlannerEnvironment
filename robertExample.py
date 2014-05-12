# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from logEnvironmentModule import *
from errorObjs import *


if __name__ == '__main__':
    #test_env = LogEnvironment("testconfig_simple.json")
    test_env = LogEnvironment("testConfig.json")

    class MyAgent(LogAgent):

        """Test the LogAgent."""

        def __init__(self):
            super(MyAgent, self).__init__()
            self.list_of_statuses = []
        

        def rec_solve(self, status, goal, list_of_actions):
            clone = status.clone
            for move in status.moves:
                clone.execute([move])
                list_of_actions.append(move)
                if clone in self.list_of_statuses:
                    if len(list_of_actions) > 0:
                        list_of_actions.pop()
                    continue
                self.list_of_statuses.append(clone.clone)
                if clone.check_goal():
                    return list_of_actions
                else:
                    print("LA:",len(list_of_actions))
                    print("LS:",len(self.list_of_statuses))
                    return self.rec_solve(clone, goal, list_of_actions)
            """ 
            tmpList_of_actions = []
            for move in status.moves:
                if len(tmpList_of_actions) > 0:
                    tmpList_of_actions.pop()
                clone = status.clone
                self.list_of_statuses.append(clone.clone)
                clone.execute([move])
                #print(clone in self.list_of_statuses)
                if clone in self.list_of_statuses:
                    #print("CLONE:",clone)
                    #print("Lista degli stati:",self.list_of_statuses)
                    continue
                #print("nuovo stato aggiunto")
                tmpList_of_actions.append(move)
                #print(move)
                #print("LISTA DELLE AZIONI", list_of_actions)
                list_of_actions.extend(tmpList_of_actions)
                if clone.check_goal():
                    return list_of_actions
                else:
                    print(list_of_actions)
                    return self.rec_solve(clone, goal, list_of_actions)
            """    
                        

            """for move in clone.moves:
                if len(list_of_actions) < 10 and not clone.check_goal():
                    tmpStatus = clone.clone
                    tmpStatus.execute([move])
                    list_of_actions.append(move)    
                    #if not tmpStatus.check_goal():
                    list_of_actions.extend(self.rec_solve(clone, goal, list_of_actions))
            return list_of_actions"""



        def solve(self, status, goal):
            """clone = status.clone
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
            """
            return self.rec_solve(status, goal, [])



    test_env.add_agent(MyAgent())
    print("MAIN Goal reached:", test_env.check_goal())
    test_env.execute()
    print("MAIN Goal reached:", test_env.check_goal())
    print("MAIN Agent score:", test_env.score())
