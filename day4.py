import re

NUMBER_REGEX = re.compile(r'\d+')

if __name__=='__main__':
    lines = open('data/day4.txt').read().splitlines()

    card_match_count = {} # Map of card ID -> # of matching numbers on that card
    card_instances = {} # Map of card ID -> # of copies we have of that card

    # Parse cards and calculate score for part 1
    score = 0
    for line in lines:
        card, winning, my = re.split('[:|]', line)
        card_number = int(NUMBER_REGEX.search(card).group(0))
        winning_numbers = NUMBER_REGEX.findall(winning)
        my_numbers = NUMBER_REGEX.findall(my)

        num_matches = len(set(my_numbers) & set(winning_numbers))
        card_match_count[card_number] = num_matches
        card_instances[card_number] = 1
        card_score = 2**(num_matches - 1) if num_matches > 0 else 0
        score += card_score
    
    print(f"Part 1: {score}")

    # Calculate card instances for part 2
    for card, num_matches in card_match_count.items():
        for instance in range(card_instances[card]):
            # num_matches matches gives one copy of each card in the range card + 1 to card + num_matches (inclusive)
            for c in range(card + 1, card + num_matches + 1):
                card_instances[c] += 1

    print(f"Part 2: {sum(card_instances.values())}")