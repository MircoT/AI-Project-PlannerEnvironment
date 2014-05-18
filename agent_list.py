# -*- coding:utf-8 -*-
import inspect
import importlib
from os import path, walk

__all__ = ["ALL_AGENTS"]

#
# All Agents TABLE
ALL_AGENTS = {}
MODULES = {}
EXCEPTIONS = ["errorObjs", "logEnvironmentModule"]


for root, dirs, files in walk("agents_dir"):
    for file_ in files:
        name, ext = path.splitext(file_)
        if ext == ".py" and name not in EXCEPTIONS:
            MODULES[name] = importlib.import_module(
                "agents_dir.{0}".format(name))
            clsmembers = inspect.getmembers(MODULES[name], inspect.isclass)
            for class_name, class_ in clsmembers:
                pkg, mod = path.splitext(class_.__module__)
                if mod == ".{0}".format(name):
                    ALL_AGENTS[name] = class_
