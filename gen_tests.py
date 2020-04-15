"""Generate a JSON test file to srp.py for each possible SRP input of a given
 size."""
import itertools
from copy import deepcopy
from random import shuffle
from random import seed


def builder(l):
    perms = itertools.permutations
    if len(l) == 1:
        for p in perms(l[0]):
            yield [list(p)]
        return

    for p in perms(l[0]):
        p = list(p)
        for subp in builder(l[1:]):
            yield [p] + subp


def gen_tests(n, rand=False):
    people = [str(x) for x in list(range(1, n + 1))]
    prefs = [[x for x in people if x != y] for y in people]

    if rand:
        while True:
            for i, plist in enumerate(prefs):
                shuffle(prefs[i])
            test = {}
            for i, plist in enumerate(prefs):
                test[str(i+1)] = plist
            yield deepcopy(test)
    else:
        for plists in builder(prefs):
            test = {}
            for i, pref_list in enumerate(plists):
                test[str(i + 1)] = pref_list

            yield deepcopy(test)
