"""An implementation of Irving's Algorithm for the Stable Roommates Problem."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Person:
    """Dataclass representation of a person in the SRP."""
    prefs = {}  # static dictionary of ALL preference lists

    name: str
    mate: str
    plist: list

    def __post_init__(self):
        """Add Person's pref list to the dict of all pref lists."""
        Person.prefs[self.name] = self.plist
        self.plist = Person.prefs[self.name]

    def pref_of(self: Person, other: Person) -> int:
        """Returns this Person's preference for another."""
        return len(self.plist) - self.plist.index(other.name)

    def has_best_match(self: Person) -> bool:
        """Is this person currently matched with their best possible partner
        according to their current preference list?"""
        if self.mate:
            for person_label in self.prefs:
                if person_label:
                    return person_label == self.mate
        return False


def srp(people):
    """Irving's Algorithm."""
    pass


if __name__ == '__main__':
    PEOPLE = [Person('A', None, ['B', 'D', 'F', 'C', 'E']),
              Person('B', None, ['D', 'E', 'F', 'A', 'C']),
              Person('C', None, ['D', 'E', 'F', 'A', 'B']),
              Person('D', None, ['F', 'C', 'A', 'E', 'B']),
              Person('E', None, ['F', 'C', 'D', 'B', 'A']),
              Person('F', None, ['A', 'B', 'D', 'C', 'E'])
              ]
    srp(PEOPLE)
