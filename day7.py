import itertools
from enum import IntEnum
from dataclasses import dataclass

class DefaultDict(dict):
    def __missing__(self, key):
        return int(key)

card_map = DefaultDict({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14})

class HandType(IntEnum):
    HighCard = 0
    OnePair = 1
    TwoPair = 2
    ThreeOfAKind = 3
    FullHouse = 4
    FourOfAKind = 5
    FiveOfAKind = 6

@dataclass
class Hand:
    card_values: list[int]
    bid: int
    hand_type: HandType

    def __init__(self, s):
        cards, bid = s.split(" ")
        self.card_values = list(map(lambda k: card_map[k], cards))
        self.bid = int(bid)

        # Groups a hand like [13, 13, 6, 7, 7] => [[6], [7, 7], [13, 13]]
        grouped = [list(g) for k, g in itertools.groupby(sorted(self.card_values))]

        # Sort by largest group first, highest value second; the above becomes [[13, 13], [7, 7], [6]]
        group_size_sorted = sorted(grouped, key=lambda x: (len(x), x[0]), reverse=True)

        first_group = len(group_size_sorted[0])
        second_group = len(group_size_sorted[1]) if len(group_size_sorted) > 1 else 0
        if first_group == 5:
            self.hand_type = HandType.FiveOfAKind
        elif first_group == 4:
            self.hand_type = HandType.FourOfAKind
        elif first_group == 3 and second_group == 2:
            self.hand_type = HandType.FullHouse
        elif first_group == 3:
            self.hand_type = HandType.ThreeOfAKind
        elif first_group == 2 and second_group == 2:
            self.hand_type = HandType.TwoPair
        elif first_group == 2:
            self.hand_type = HandType.OnePair
        else:
            assert(len(group_size_sorted) == 5)
            self.hand_type = HandType.HighCard
    
    def __lt__(self, other):
        # Sort by hand type first...
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        # ... and card values second
        return self.card_values < other.card_values

if __name__=='__main__':
    lines = open('data/day7.txt').read().splitlines()
    hands = sorted(map(Hand, lines))

    # Part 1
    winnings = 0
    for i, hand in enumerate(hands):
        rank = i + 1
        winnings += rank * hand.bid

    print(f"Part 1: {winnings}")