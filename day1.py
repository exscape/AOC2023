lines = open('data/day1.txt', 'r').readlines()

digitMap = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

sum = 0
for line in lines:
    digits = list(filter(str.isdigit, line))
    sum += int(digits[0] + digits[-1])

print(f"Part 1: {sum}")

sum = 0
for line in lines:
    digits = []
    pos = 0

    while (partialLine := line[pos:]):
        if partialLine[0].isdigit():
            digits.append(partialLine[0])
        else:
            for k,v in digitMap.items():
                if partialLine.startswith(k):
                    digits += str(v)
                    break
        pos += 1

    sum += int(digits[0] + digits[-1])

print(f"Part 2: {sum}")