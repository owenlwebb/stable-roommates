"""Driver for the Stable Roommates problem. Used for testing purposes only."""
import srp


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

    matching = srp.irving(people)

    if not matching:
        print("No stable matching!")
