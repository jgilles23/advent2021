import itertools
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

def translate(translator, digit):
    translated_segments = "".join([chr(translator.index(d)+97) for d in digit])
    return translated_segments

base_translator = {x:2**i for i,x in enumerate("abcdefg")}
def translate(digit_string, translator=base_translator):
    return sum([translator[x] for x in digit_string])

#part2
digits_by_segement = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
segement_to_digit = {"abcefg":0, "cf":1, "acdeg":2, "acdfg":3, "bcdf":4, "abdfg":5, "abdefg":6, "acf":7, "abcdefg":8, "abcdfg":9}
values_to_digit = {translate(k):v for k,v in segement_to_digit.items()}

ans = 0
for i, input, output in zip(range(len(inputs)), inputs, outputs):
    for p in itertools.permutations("abcdefg"):
        translator = {x:2**i for i,x in enumerate(p)}
        found_digits = set()
        for digit in input:
            value = translate(digit, translator)
            if value in values_to_digit:
                #print("Found a digit:", digit, translator, value)
                found_digits.add(value)
        if found_digits == set(values_to_digit.keys()):
            out = [values_to_digit[translate(digit, translator)] for digit in output]
            out = int("".join([str(x) for x in out]))
            print(i, translator, out)
            ans += out
print("part2", ans)

