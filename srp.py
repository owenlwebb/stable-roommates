"""An implementation of Irving's Algorithm for the Stable Roommates Problem."""
import Person.Person


class SRP:
    def srp(people):
        """Irving's Algorithm."""

        # PHASE 1 ~ Gale-Shaple-esque
        for offerer in gen_offerers(people):
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

        # If someone does not hold an offer after Phase 1, no stable matching exists
        if not all(p.offer_held for p in people):
            return []

        # PHASE 1 ~ Reduction
        for person in people:       # Pg. 582 of Irving.
            person.reduce_lower()   # del those to whom person prefers offer_held
            person.reduce_higher()  # del those who offer_held is better than person

        # PHASE 2 ~ Cycle Removal
        for person in gen_cycle_start(people):
            pass
        Person.print_pref_table()

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
