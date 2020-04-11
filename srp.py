"""An implementation of Irving's Algorithm for the Stable Roommates Problem."""
from __future__ import annotations
from dataclasses import dataclass


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

    def get_next_highest(self: Person) -> Person:
        """Get next highest preferred roommate in plist."""
        return next(Person.all_people[p] for p in self.plist if p)

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


def gen_offerers(people):
    """Yield the next Person that is eligible to make an offer."""
    all_matched = False
    while not all_matched:
        all_matched = True  # assume and correct if not
        for person in people:
            if not person.offer_sent and any(person.plist):
                all_matched = False
                yield person


def srp(people):
    """Irving's Algorithm."""

    # PHASE 1
    while True:
        # get next offerer
        try:
            offerer = next(gen_offerers(people))
        except StopIteration:
            break

        # get next offeree and the current person they've given a POC to
        offeree = offerer.get_next_highest()
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

    # PHASE 2 (Cycle Removal)
    Person.print_pref_table()


if __name__ == '__main__':
    PEOPLE = [
        Person('A', None, None, ['B', 'D', 'F', 'C', 'E']),
        Person('B', None, None, ['D', 'E', 'F', 'A', 'C']),
        Person('C', None, None, ['D', 'E', 'F', 'A', 'B']),
        Person('D', None, None, ['F', 'C', 'A', 'E', 'B']),
        Person('E', None, None, ['F', 'C', 'D', 'B', 'A']),
        Person('F', None, None, ['A', 'B', 'D', 'C', 'E'])
    ]
    srp(PEOPLE)
