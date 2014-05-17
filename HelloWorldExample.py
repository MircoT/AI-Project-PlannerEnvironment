# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from logEnvironmentModule import *
from errorObjs import *

import random


if __name__ == '__main__':
    #test_env = LogEnvironment("testconfig_simple.json")
    #test_env = LogEnvironment("testconfig.json")

    class MyAgent(LogAgent):

        """Test the LogAgent."""

        def __init__(self):
            super(MyAgent, self).__init__()
        
        def itr_solve(self, status):
            stat = status.clone
            h = 0
            possible_moves = []
            list_of_actions = []
            while(not stat.check_goal()):
                for move in stat.moves:
                    clone = stat.clone
                    clone.execute([move])
                    h2 = self.heuristic(stat.goal, clone)
                    if h < h2:
                        h = h2
                        stat = clone.clone
                        list_of_actions.append(move)
                        continue
                    elif h == h2:
                        possible_moves.append(move)
                print('OPS! RADOM!')
                move = random.choice(possible_moves)
                possible_moves = []
                print(move)
                stat.execute([move])
                list_of_actions.append(move)
            self.heuristic(stat.goal, stat)
            return list_of_actions

        def heuristic(self, goal, status):
            '''
            http://www.urticator.net/essay/3/326.html
            '''
            results = 0
            #print("eccomi!",status.airports)
            for destination, objs in goal.items():
                #print('SUPER WHAT?!', objs, destination)
                if destination in list(status.airports.keys()):
                    for obj in objs:
                        #print('WHAT?!',obj)
                        if obj in status.airports[destination]:
                            results = results + 5 
                elif destination in list(status.airplanes.keys()):
                    for obj in objs:
                        #print('WHAT?!',obj)
                        if obj in status.airplanes[destination]:
                            results = results + 5
            print('heuristic',results)       
            return results                                   

        def solve(self, status, goal):
            '''
            Dear fellow Student,

            here I add some more examples on how to manipulate 
            the objects from the logEnvironmentModule.

            I also added a VERY dumb agent. 
            If your agent can't do better than this, you should work
            a little more on it.
            I hope it can help a little.

            Best regards,
            Robert

            '''

            #   Here are more examples of how you can play around
            #   with the objects in this module
            '''
            print(status)
            for airport in status.airports:
                print(airport)
                for plane in status.airports[airport].airplanes:
                    print("Contains", plane)
                    for box in status.airports[airport].airplanes[plane].boxes: 
                        print("scatole nell'aereo", box)
                    print("maxboxes:", status.airports[airport].airplanes[plane].maxbox)
                for neighbor in status.airports[airport].neighbors:
                    print("Is near to", neighbor)
                    print("with distance", status.airports[airport].neighbors[neighbor])
                for box in status.airports[airport].boxes:
                    print("Contains also", box)
            print(status.goal.items())
            for goal in status.goal:
                print(goal)
                print(status.goal[goal])
                print(dir(status.goal[goal]))
                print(status.goal[goal])'''
            
            #   This is a small code snippet to show you how to
            #   hash() a state. It could be usefull to someone..
            
            """
            print(status.clone)
            print(hash(print(status.clone)))
            print(hash(repr(status))) #this is how you should do it!
            clone = status.clone
            print(clone == status)
            clone.execute([status.moves[0],status.moves[1],status.moves[6]])
            print(hash(repr(clone)))
            print(clone)
            print(clone == status)
            #print(status.moves)"""
            
            return self.itr_solve(status)


    #   you should do this to try your agent only once
    """
    test_env.add_agent(MyAgent())
    print("MAIN Goal reached:", test_env.check_goal())
    test_env.execute()
    print("MAIN Goal reached:", test_env.check_goal())
    print("MAIN Agent score:", test_env.formatted_score())
    """

    #   here I try to run my simple agent many times
    #   then I get a mean value for the score
    itrNum = 10
    partialScore = 0
    goalAlwaysReached = True
    i = 0
    while i < itrNum:
        asd = LogEnvironment("testconfig_simple.json")
        asd.add_agent(MyAgent())
        asd.check_goal()
        asd.execute()
        asd.check_goal()
        if(not asd.check_goal()):
            goalAlwaysReached = False
        partialScore += asd.score()
        i += 1
    meanScore = partialScore / itrNum
    print("Mean score is:", meanScore)
    if(not goalAlwaysReached):
        print("Goal not always reached")