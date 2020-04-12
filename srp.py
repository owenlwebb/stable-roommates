"""An implementation of Irving's Algorithm for the Stable Roommates Problem."""
from __future__ import annotations

import glob
import json
import os
from dataclasses import dataclass
from itertools import islice


@dataclass
class Person:
    """Dataclass representation of a person in the SRP.

    POC = Promise of Consideration.
    """
    all_people = {}     # static dictionary of ALL init'd People

    name: str
    plist: list         # Preference list

    def __post_init__(self):
        """Add Person to the dict of all People and set default values for
        whether this person has made an offer and who they hold an offer from"""
        Person.all_people[self.name] = self
        self.offer_sent = False     # Has this person made their offer?
        self.offer_held = None      # Person self is holding an offer from

    def pref_of(self: Person, other: Person) -> int:
        """Returns this Person's preference for another."""
        try:
            return len(self.plist) - self.plist.index(other.name)
        except ValueError:
            # must be that that person was already deleted for consideration
            # from the preference list.
            return -1

    def get_nth_highest(self: Person, n: int) -> Person:
        """Get the nth highest preferred roommate in plist. Return least
        preferred person if n = -1."""
        non_null_prefs = (Person.all_people[p]
                          for p in self.plist if p is not None)
        for i, pref in enumerate(non_null_prefs):
            if i + 1 == n:
                return pref
        if n == -1:
            return pref     # return last pref if n == -1
        raise ValueError(f"Less than n entries in {self.name} preference list")

    def remove(self: Person, other: Person) -> None:
        """Remove other from self's preference list."""
        self.plist[self.plist.index(other.name)] = None

    def reduce_lower(self: Person) -> None:
        """Delete all of those in self's preference list that are less desirable
        than self's offer_held."""
        index = self.plist.index(self.offer_held)
        self.plist = [p if i <= index else None for i,
                      p in enumerate(self.plist)]

    def reduce_higher(self: Person) -> None:
        """Delete all of those in self's preference list who's offer_held is
        more preferable than self."""
        for i, person in enumerate(self.plist):
            if not person:  # ignore already deleted entries
                continue

            # get this Person and their currently held offer
            person = Person.all_people[person]
            curr_offer = Person.all_people[person.offer_held]
            if person.pref_of(curr_offer) > person.pref_of(self):
                self.plist[i] = None

    @staticmethod
    def get_person(name: str) -> Person:
        """Return the person object corresponding to name."""
        return Person.all_people[name] if name is not None else None

    @staticmethod
    def reset() -> None:
        """Reset the Person-wide all_people to an empty dictionary."""
        Person.all_people = {}

    @staticmethod
    def print_pref_table() -> None:
        """Print the table of people and their preference lists."""
        for person in sorted(Person.all_people.values(), key=lambda p: p.name):
            print_list = [p if p is not None else ' ' for p in person.plist]
            print(f"{person.name} | " + ' '.join(print_list))


def main():
    """Testing. Test files should be a single JSON dictionary mapping a name
    to a list of preferences."""
    os.chdir(os.getcwd())
    for test_file in glob.glob("*.test.json"):
        with open(test_file, 'r') as fin:
            test = json.load(fin)

            people = []
            for name, prefs in test.items():
                people.append(Person(name, prefs))

            print(f'*** TESTING: {test_file} ***')
            srp(people)
            Person.reset()
            print()


def srp(people):
    """Irving's Algorithm."""
    Person.print_pref_table()
    print()

    # PHASE 1 ~ Gale-Shaple-esque
    for offerer in gen_offerers(people):
        # get next offeree and the current person they've given a POC to
        offeree = offerer.get_nth_highest(1)
        offeree_curr = Person.get_person(offeree.offer_held)

        # Offeree accepts automatically
        if offeree_curr is None:
            offerer.offer_sent = True
            offeree.offer_held = offerer.name
        # Offeree trades up
        elif offeree.pref_of(offerer) > offeree.pref_of(offeree_curr):
            # reject former partner
            offeree.remove(offeree_curr)
            offeree_curr.remove(offeree)
            offeree_curr.offer_sent = False

            offerer.offer_sent = True
            offeree.offer_held = offerer.name
        # Offereee rejects
        else:
            offerer.remove(offeree)
            offeree.remove(offerer)

    # If someone does not hold an offer after Phase 1, no stable matching exists
    if not all(p.offer_held is not None for p in people):
        print("No stable matching (failed after phase 1)")
        return

    # PHASE 1 ~ Reduction
    for person in people:       # Pg. 582 of Irving.
        person.reduce_lower()   # del those to whom person prefers offer_held
        person.reduce_higher()  # del those who offer_held is better than person

    # Failure check
    if any((len(p.plist) - p.plist.count(None) == 0) for p in people):
        print("No stable matching (failed after phase 1 reduction)")

    # PHASE 2 ~ Cycle Removal
    for person in people:
        prefs_left = len(person.plist) - person.plist.count(None)
        if prefs_left == 0:
            break  # No stable matching
        if prefs_left >= 2:
            cycle = [person]
            try:
                # build the preference cycle
                while (len(cycle) == 1) or (cycle[0] != cycle[-1]):
                    cycle.append(cycle[-1].get_nth_highest(2))
                    cycle.append(cycle[-1].get_nth_highest(-1))

                # consecutive pairs in the cycle reject each other
                for i in range(1, len(cycle) - 1, 2):
                    cycle[i].remove(cycle[i + 1])
                    cycle[i + 1].remove(cycle[i])
            except ValueError:
                # something when wrong in cycle creation/removal.
                # No stable matching.
                break

    # Final check if preference lists specify a stable matching
    if all((len(p.plist) - p.plist.count(None) == 1) for p in people):
        print('Stable matching found!\n')
        Person.print_pref_table()
    else:
        print('No stable matching (failed after phase 2')


def gen_offerers(people):
    """Yield the next Person that is eligible to make an offer."""
    all_matched = False
    while not all_matched:
        all_matched = True  # assume and correct if not
        for person in people:
            if not person.offer_sent and any(person.plist):
                all_matched = False
                yield person


if __name__ == '__main__':
    main()
