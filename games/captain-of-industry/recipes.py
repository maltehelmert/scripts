# -*- coding: utf-8 -*-

from collections import defaultdict


class Recipe(defaultdict):
    def __init__(self, data=(), /, title=None):
        defaultdict.__init__(self, int)
        self.update(data)
        self.title = title

    def copy(self):
        return Recipe(self, title=self.title)

    def __add__(self, other):
        result = self.copy()
        for key, value in other.items():
            result[key] += value
        return result

    def __iadd__(self, other):
        for key, value in other.items():
            self[key] += value
        return self

    def set_title(self, title):
        self.title = title

    def dump(self):
        if self.title:
            print(f"{self.title}:")
        for key, value in sorted(self.items()):
            print(f"    {key:35} {float(value):10.4f} {value}")
