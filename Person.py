"""Person class for the Stable Roommates Problem."""
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
