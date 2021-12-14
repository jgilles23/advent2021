inputs = []
outputs = []
with open("day8_input.txt") as file:
    for line in file:
        raw = line[:-1].split(" ")
        inputs.append(raw[:10])
        outputs.append(raw[11:])
#print(inputs)
#print(outputs)

#part1
count = 0
for output in outputs:
    for digit in output:
        x = len(digit)
        if x in [2,4,3,7]:
            count += 1
print('part1', count)

#part2
digits_by_segement = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
digits_by_segement = [set([x for x in digit]) for digit in digits_by_segement]
decoded_output = []
for input, output in zip(inputs,outputs):
    decode_map = {y:set([x for x in "abcdef"]) for y in "abcdef"}
    input.sort(key=len)
    input = [set([x for x in y]) for y in input]
    one = input[0]
    for option in decode_map[0]:
        if option not in one:
            one.remove(option)
    print(digits_by_segement)
    break