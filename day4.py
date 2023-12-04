import re

NUMBER_REGEX = re.compile(r'\d+')

if __name__=='__main__':
    lines = open('data/day4.txt').read().splitlines()

    sum = 0
    for line in lines:
        _, winning, my = re.split('[:|]', line)
        winning_numbers = NUMBER_REGEX.findall(winning)
        my_numbers = NUMBER_REGEX.findall(my)

        num_winning = len(set(my_numbers) & set(winning_numbers))
        score = 2**(num_winning - 1) if num_winning > 0 else 0
        sum += score
    
    print(f"Part 1: {sum}")