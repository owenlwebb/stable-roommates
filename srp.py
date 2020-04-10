"""An implementation of Irving's Algorithm for the Stable Roommates Problem."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Person:
    """Dataclass representation of a person in the SRP."""
    all_people = {}  # static dictionary of ALL init'd People

    name: str
    mate: str
    plist: list

    def __post_init__(self):
        """Add Person to the dict of all People."""
        Person.all_people[self.name] = self

    def pref_of(self: Person, other: Person) -> int:
        """Returns this Person's preference for another."""
        return len(self.plist) - self.plist.index(other.name)

    def has_best_match(self: Person) -> bool:
        """Is this person currently matched with their best possible partner
        according to their current preference list?"""
        if self.mate:
            for name in self.plist:
                if name:
                    return name == self.mate
        return False

    def get_next_highest(self: Person) -> str:
        """Get next highest preferred roommate in plist."""
        for person in self.plist:
            if person:
                return Person.all_people[person]
        return None

    @staticmethod
    def reset():
        """Reset the Person-wide all_people to an empty dictionary."""
        Person.all_people = {}


def srp(people):
    """Irving's Algorithm."""

    # PHASE 1
    for person in (p for p in people if not p.has_best_match()):
        potential = person.get_next_highest()


if __name__ == '__main__':
    PEOPLE = [
        Person('A', None, ['B', 'D', 'F', 'C', 'E']),
        Person('B', None, ['D', 'E', 'F', 'A', 'C']),
        Person('C', None, ['D', 'E', 'F', 'A', 'B']),
        Person('D', None, ['F', 'C', 'A', 'E', 'B']),
        Person('E', None, ['F', 'C', 'D', 'B', 'A']),
        Person('F', None, ['A', 'B', 'D', 'C', 'E'])
    ]
    srp(PEOPLE)
