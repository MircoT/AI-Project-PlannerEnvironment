from __future__ import print_function, unicode_literals
import json
from sys import argv, exit
from os import path
from random import randint, choice, sample
from time import sleep

CFG = dict()
BASEPATH = "cfg_dir"


def generate_random_cfg(name, num_airports, num_airplanes, num_boxes):
    """Generate a random configuration with a specific name."""
    tmp_positions = list()
    airplanes = ["Airplane_" + str(num)
                 for num in range(1, int(num_airplanes) + 1)]
    boxes = ["Box_" + str(num) for num in range(1, int(num_boxes) + 1)]
    sleep(1)
    with open(path.join(BASEPATH, name + ".json"), "w") as r_cfg:
        CFG['initial_status'] = dict()
        CFG['initial_status']['airports'] = int(num_airports)
        CFG['initial_status']['airplanes'] = int(num_airplanes)
        CFG['initial_status']['boxes'] = int(num_boxes)
        CFG['initial_status']['edges'] = dict()
        for num in range(1, int(num_airports) + 1):
            airport_name = "Airport_" + str(num)
            CFG['initial_status']['edges'][airport_name] = dict()
            for num_2 in range(1, int(num_airports) + 1):
                if num_2 != num and choice([True, False]):
                    airport_name_2 = "Airport_" + str(num_2)
                    CFG['initial_status']['edges'][
                        airport_name][airport_name_2] = randint(1, 100)
        CFG['initial_status']['vertices'] = dict()
        for num in range(1, int(num_airports) + 1):
            airport_name = "Airport_" + str(num)
            CFG['initial_status']['vertices'][airport_name] = dict()
            new_pos = [randint(0, 100), randint(0, 100)]
            while new_pos in tmp_positions:
                new_pos = [randint(0, 100), randint(0, 100)]
            tmp_positions.append(new_pos)
            CFG['initial_status']['vertices'][
                airport_name]['position'] = new_pos
            CFG['initial_status']['vertices'][airport_name]['boxes'] = list()
            if len(boxes) > 0:
                num_boxes = randint(0, choice(range(0, len(boxes) + 1)))
                for num_box in range(0, num_boxes):
                    if len(boxes) == 0:
                        break
                    box_choiced = choice(boxes)
                    boxes.remove(box_choiced)
                    CFG['initial_status']['vertices'][airport_name][
                        'boxes'].append(box_choiced)
            CFG['initial_status']['vertices'][
                airport_name]['airplanes'] = dict()
            if len(airplanes) > 0:
                num_airplanes = randint(0, len(boxes) + 1)
                for num_airplane in range(0, num_airplanes):
                    if len(airplanes) == 0:
                        break
                    airplane_choiced = choice(airplanes)
                    airplanes.remove(airplane_choiced)
                    CFG['initial_status']['vertices'][airport_name][
                        'airplanes'][airplane_choiced] = dict()
                    CFG['initial_status']['vertices'][airport_name][
                        'airplanes'][airplane_choiced]['maxbox'] = randint(1, 25)
                    CFG['initial_status']['vertices'][airport_name][
                        'airplanes'][airplane_choiced]['boxes'] = list()
                    if len(boxes) > 0 and len(boxes) >= CFG['initial_status']['vertices'][airport_name][
                            'airplanes'][airplane_choiced]['maxbox']:
                        num_boxes = randint(
                            0, CFG['initial_status']['vertices'][airport_name][
                                'airplanes'][airplane_choiced]['maxbox'])
                        for num_box in range(0, num_boxes):
                            if len(boxes) == 0:
                                break
                            box_choiced = choice(boxes)
                            boxes.remove(box_choiced)
                            CFG['initial_status']['vertices'][airport_name][
                                'airplanes'][airplane_choiced]['boxes'].append(box_choiced)
        if len(boxes) > 0:  # Assign remainings boxes
            for box in boxes:
                airport_name = choice(
                    list(CFG['initial_status']['vertices'].keys()))
                CFG['initial_status']['vertices'][
                    airport_name]['boxes'].append(box)
        if len(airplanes) > 0:  # Assign remainings airplanes
            for airplane in airplanes:
                airport_name = choice(
                    list(CFG['initial_status']['vertices'].keys()))
                CFG['initial_status']['vertices'][
                    airport_name]['airplanes'][airplane] = dict()
                CFG['initial_status']['vertices'][airport_name][
                    'airplanes'][airplane]['maxbox'] = randint(1, 25)
                if len(boxes) > 0 and len(boxes) >= CFG['initial_status']['vertices'][airport_name][
                        'airplanes'][airplane]['maxbox']:
                    num_boxes = randint(
                        0, CFG['initial_status']['vertices'][airport_name][
                            'airplanes'][airplane]['maxbox'])
                    for num_box in range(0, num_boxes):
                        if len(boxes) == 0:
                            break
                        box_choiced = choice(boxes)
                        boxes.remove(box_choiced)
                        CFG['initial_status']['vertices'][airport_name][
                            'airplanes'][airplane]['boxes'].append(box_choiced)
        CFG['goal'] = list()
        airports_list = ["Airport_" + str(num)
                         for num in range(1, int(num_airports) + 1)]
        airplanes_list = ["Airplane_" + str(num)
                          for num in range(1, int(num_airplanes) + 1)]
        airplanes = ["Airplane_" + str(num)
                     for num in range(1, int(num_airplanes) + 1)]
        boxes = ["Box_" + str(num) for num in range(1, int(num_boxes) + 1)]
        sleep(0.5)
        min_goal = (len(boxes) + len(airplanes)) % 10
        num_goals = randint(min_goal, len(boxes) + len(airplanes) + 2)
        while len(CFG['goal']) == 0:
            if not (len(boxes) > 0 and len(airplanes) > 0):
                airplanes = ["Airplane_" + str(num)
                             for num in range(1, int(num_airplanes) + 1)]
                boxes = ["Box_" + str(num)
                         for num in range(1, int(num_boxes) + 1)]
            for num_goal in range(0, num_goals):
                goal = ""
                if choice([True, False]):
                    if len(boxes) > 0:
                        sample_b = sample(boxes, randint(1, len(boxes)))
                        boxes = list(set(boxes) - set(sample_b))
                        goal += ", ".join(sample_b)
                        if choice([True, False]):
                            airport = choice(airports_list)
                            goal += " in " + airport
                        else:
                            airplane = choice(airplanes_list)
                            goal += " in " + airplane
                else:
                    if len(airplanes) > 0:
                        sample_a = sample(
                            airplanes, randint(1, len(airplanes)))
                        airplanes = list(set(airplanes) - set(sample_a))
                        goal += ", ".join(sample_a)
                        airport = choice(airports_list)
                        goal += " in " + airport
                CFG['goal'].append(goal)
            CFG['goal'] = list(filter(len, CFG['goal']))
        r_cfg.write(json.dumps(CFG, indent=4, sort_keys=True))
        print("Cfg", name + ".json created!")


if __name__ == '__main__':
    help_string = "Please use this tool like this:\n\n"\
        "\tpython cfg_generator.py name num_airports num_airplanes num_boxes\n"\
        "\nThanks!"
    random_strings = ["Are you kidding me?",
                      "What are you doing?",
                      "Serious, you don't mind that?",
                      "Tell yourself why you're so dumb...",
                      "You're wasting your time, dude!",
                      "If this is your best I'm upset!",
                      "Do you read the --help advice?"]
    if len(argv) != 5:
        print(help_string)
        exit(0)
    elif len(argv) == 2 and argv[1] == "--help":
        print(help_string)
        exit(0)
    elif len(argv) == 5:
        try:
            assert int(argv[2]) > 0, choice(random_strings)
            assert int(argv[3]) > 0, choice(random_strings)
            assert int(argv[4]) > 0, choice(random_strings)
        except ValueError:
            print(choice(random_strings))
            exit(0)
        else:
            generate_random_cfg(*argv[1:])
