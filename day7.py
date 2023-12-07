import itertools
from enum import IntEnum
from dataclasses import dataclass

class DefaultDict(dict):
    def __missing__(self, key):
        return int(key)

card_map = DefaultDict({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14})
card_map_joker = DefaultDict({'J': 1, 'T': 10, 'Q': 12, 'K': 13, 'A': 14})

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

    @classmethod
    def calculate_hand_type(cls, card_values, joker = False):
        jokers = card_values.count(1)

        # Groups a hand like [13, 13, 6, 7, 7] => [[6], [7, 7], [13, 13]]
        grouped = [list(g) for k, g in itertools.groupby(sorted(card_values))]

        # Sort by largest group first, highest value second; the above becomes [[13, 13], [7, 7], [6]]
        grouped_sorted = sorted(grouped, key=lambda x: (len(x), x[0]), reverse=True)

        # If the largest group is jokers, rewrite them into instances of the second-largest group,
        # or the math below will fail. For example, [[1, 1, 1], [4], [2]] => [[4, 4, 4, 4], [2]]
        # The length check is needed to cover the case of 5 jokers.
        if joker and grouped_sorted[0][0] == 1 and len(grouped_sorted) > 1:
            grouped_sorted[0] = [grouped_sorted[1][0]] * (len(grouped_sorted[1]) + jokers)
            del grouped_sorted[1]
            jokers = 0 # They're already accounted for, don't count them twice below

        # Calculate the sizes of the two first groups (at most two groups are needed for a hand, except high card)
        first_group = len(grouped_sorted[0]) + jokers
        second_group = len(grouped_sorted[1]) if len(grouped_sorted) > 1 else 0

        if first_group >= 5:
            hand_type = HandType.FiveOfAKind
        elif first_group == 4:
            hand_type = HandType.FourOfAKind
        elif first_group == 3 and second_group == 2:
            hand_type = HandType.FullHouse
        elif first_group == 3:
            hand_type = HandType.ThreeOfAKind
        elif first_group == 2 and second_group == 2:
            hand_type = HandType.TwoPair
        elif first_group == 2:
            hand_type = HandType.OnePair
        else:
            # A hand with jokers can never give a high card hand
            assert(jokers == 0)
            # A high card hand can't have pairs, so the 5 cards must be unique and so non-grouped
            assert(len(grouped_sorted) == 5)

            hand_type = HandType.HighCard

        return hand_type

    def __init__(self, s, joker = False):
        cards, bid = s.split(" ")
        self.joker = joker
        self.card_values = list(map(lambda k: card_map[k] if not self.joker else card_map_joker[k], cards))
        self.bid = int(bid)
        self.hand_type = Hand.calculate_hand_type(self.card_values, joker)
    
    def __lt__(self, other):
        # Sort by hand type first...
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        # ... and card values second
        return self.card_values < other.card_values

def calculate_winnings(lines, joker = False):
    hands = sorted(map(lambda x: Hand(x, joker=joker), lines))
    winnings = 0
    for i, hand in enumerate(hands):
        rank = i + 1
        winnings += rank * hand.bid
    return winnings

if __name__=='__main__':
    lines = open('data/day7.txt').read().splitlines()
    print(f"Part 1: {calculate_winnings(lines, joker=False)}")
    print(f"Part 2: {calculate_winnings(lines, joker=True)}")