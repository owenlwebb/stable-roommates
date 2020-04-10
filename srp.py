"""An implementation of Irving's Algorithm for the Stable Roommates Problem."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Person:
    """Dataclass representation of a person in the SRP."""
    label: str
    roommate: str
    prefs: list

    def pref_of(self: Person, other: Person) -> int:
        """Returns this Person's preference for another."""
        return len(self.prefs) - self.prefs.index(other.label)

    def has_best_match(self: Person) -> bool:
        """Is this person currently matched with their best possible partner
        according to their current preference list?"""
        if self.roommate:
            for person_label in self.prefs:
                if person_label:
                    return person_label == self.roommate
        return False


def srp(people):
    """Irving's Algorithm."""

    # Phase 1
    for person in people:
        if not person.has_best_match():
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
