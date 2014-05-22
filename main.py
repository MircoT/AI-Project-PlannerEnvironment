# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from agents_dir.logEnvironmentModule import *
from agents_dir.errorObjs import *
from agent_list import *
from sys import argv
from glob import glob
from os import path


def parse_args(list_, first, second):
    """Helper function to parse args."""
    if first is not False:
        if second is not False:
            if second > first:
                list_ = [
                    agent for agent in list_ if agent in argv[first:second]]
            else:
                list_ = [
                    agent for agent in list_ if agent in argv[first:]]
        else:
            list_ = [
                agent for agent in list_ if agent in argv[first:]]
    return list_

if __name__ == '__main__':
    try:
        CONFIG = argv.index("-c")
    except ValueError:
        CONFIG = False
    try:
        AGENTS = argv.index("-a")
    except ValueError:
        AGENTS = False
    AGENTS_LIST = ALL_AGENTS.keys()
    ENVS_LIST = glob("cfg_dir/*.json")
    AGENTS_LIST = parse_args(AGENTS_LIST, AGENTS, CONFIG)
    ENVS_LIST = [path.join("cfg_dir", env) for env in parse_args(
        [path.basename(env) for env in ENVS_LIST], CONFIG, AGENTS)]
    print(ALL_AGENTS)
    ENV = LogEnvManager(
        ALL_AGENTS, AGENTS_LIST, ENVS_LIST)
    ENV.execute()
    ENV.get_score()
