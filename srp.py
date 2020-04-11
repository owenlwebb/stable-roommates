"""An implementation of Irving's Algorithm for the Stable Roommates Problem."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import islice


@dataclass
class Person:
    """Dataclass representation of a person in the SRP.

    POC = Promise of Consideration.
    """
    all_people = {}     # static dictionary of ALL init'd People

    name: str
    offer_sent: str     # Person to whom an offer was sent and a POC was recvd
    offer_held: str     # Person who gave self an offer and self sent a POC
    plist: list         # Preference list

    def __post_init__(self):
        """Add Person to the dict of all People."""
        Person.all_people[self.name] = self

    def pref_of(self: Person, other: Person) -> int:
        """Returns this Person's preference for another."""
        try:
            return len(self.plist) - self.plist.index(other.name)
        except ValueError:
            # return -1 when other is not found in plist. Must be that other
            # was set to None
            return -1

    def get_nth_highest(self: Person, n: int) -> Person:
        """Get the nth highest preferred roommate in plist."""
        non_null_prefs = (Person.all_people[p] for p in self.plist if p)
        return next(islice(non_null_prefs, n - 1, None))

    def remove(self: Person, other: Person) -> None:
        """Remove other from self's preference list."""
        self.plist[self.plist.index(other.name)] = None

    def reject(self: Person, other: Person) -> None:
        """self and other symetrically reject."""
        assert self.offer_held and (self.offer_held == other.name)
        assert other.offer_sent and (other.offer_sent == self.name)

        other.offer_sent = None
        self.offer_held = None
        other.remove(self)
        self.remove(other)

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
        return Person.all_people[name] if name else None

    @staticmethod
    def reset() -> None:
        """Reset the Person-wide all_people to an empty dictionary."""
        Person.all_people = {}

    @staticmethod
    def print_pref_table() -> None:
        """Print the table of people and their preference lists."""
        for person in sorted(Person.all_people.values(), key=lambda p: p.name):
            print_list = [p if p else ' ' for p in person.plist]
            print(f"{person.name} | " + ' '.join(print_list))


def main():
    """Testing."""
    people = [
        Person('A', None, None, ['B', 'D', 'F', 'C', 'E']),
        Person('B', None, None, ['D', 'E', 'F', 'A', 'C']),
        Person('C', None, None, ['D', 'E', 'F', 'A', 'B']),
        Person('D', None, None, ['F', 'C', 'A', 'E', 'B']),
        Person('E', None, None, ['F', 'C', 'D', 'B', 'A']),
        Person('F', None, None, ['A', 'B', 'D', 'C', 'E'])
    ]
    matching = srp(people)

    if not matching:
        print("No stable matching!")


def srp(people):
    """Irving's Algorithm."""

    # PHASE 1 ~ Gale-Shaple-esque
    for offerer in gen_offerers(people):
        # get next offeree and the current person they've given a POC to
        offeree = offerer.get_nth_highest(1)
        offeree_poc = Person.get_person(offeree.offer_held)

        # Offeree accepts automatically
        if not offeree_poc:
            offerer.offer_sent = offeree.name
            offeree.offer_held = offerer.name
        # Offeree trades up
        elif offeree.pref_of(offerer) > offeree.pref_of(offeree_poc):
            offeree.reject(offeree_poc)  # symetrically reject former
            offerer.offer_sent = offeree.name
            offeree.offer_held = offerer.name
        # Offereee rejects
        else:
            offerer.remove(offeree)
            offeree.remove(offerer)

    # If someone does not hold an offer after Phase 1, no stable matching exists
    if not all(p.offer_held for p in people):
        return []

    # PHASE 1 ~ Reduction
    for person in people:       # Pg. 582 of Irving.
        person.reduce_lower()   # del those to whom person prefers offer_held
        person.reduce_higher()  # del those who offer_held is better than person

    # PHASE 2 ~ Cycle Removal
    Person.print_pref_table()
    for orig_person in gen_cycle_start(people):
        curr_person = orig_person
        to_remove = curr_person.get_nth_highest(2)


def gen_offerers(people):
    """Yield the next Person that is eligible to make an offer."""
    all_matched = False
    while not all_matched:
        all_matched = True  # assume and correct if not
        for person in people:
            if not person.offer_sent and any(person.plist):
                all_matched = False
                yield person


def gen_cycle_start(people):
    """Yield the next person whose preference list indicates the start of a
    preference cycle. This is simply any person who has more than one entry
    left in their preference list. Raise StopIteration when no such person
    exists, or there exists a person with an empty preference list."""
    cycles_exist = True
    while cycles_exist:
        cycles_exist = False  # assume and correct if not
        for person in people:
            prefs_left = len(person.plist) - person.plist.count(None)
            if prefs_left > 1:
                cycles_exist = True
                yield person
            elif prefs_left == 0:
                return


if __name__ == '__main__':
    main()
