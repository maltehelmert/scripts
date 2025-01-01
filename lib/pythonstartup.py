# -*- coding: utf-8 -*-

import os
import sys

from combinatorics import bin, fac
from statistics import mean, variance, stddev, median

def password(length=8):
    import random
    import string
    symbols = "".join(c for c in string.printable if not c.isspace())
    rng = random.SystemRandom()
    return "".join(rng.choice(symbols) for _ in range(length))

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    try:
        import rlcompleter
    except ImportError:
        print("Module rlcompleter not available.")
    else:
        readline.parse_and_bind("tab: complete")
        del rlcompleter
    del readline

h = [None]

class Prompt:
    def __init__(self, str="h[%d] >>> "):
        self.str = str

    def __str__(self):
        try:
            if _ not in [h[-1], None, h]:
                h.append(_)
        except NameError:
            pass
        return self.str % len(h)

    def __radd__(self, other):
        return str(other) + str(self)


if os.environ.get("TERM") in ["xterm", "vt100"]:
    sys.ps1 = Prompt("\001\033[01;31m\002h[%d] >>> \001\033[00m\002")
else:
    sys.ps1 = Prompt()
sys.ps2 = ""

# print("Beware of the Toilet Limbo Dancer!")

del os
del sys
