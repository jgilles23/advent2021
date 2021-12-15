from collections import Counter

with open("day14_input.txt") as file:
    polymer_string = file.readline()[:-1]
    polymer_values = [x for x in polymer_string]
    polymer_nexts = list(range(1,len(polymer_values))) + [None]
    file.readline()
    subs = {line[0:2]:line[6] for line in file}
#print(polymer_values)
#print(subs)

def step():
    pos_a = 0
    pos_c = polymer_nexts[pos_a]
    while pos_c is not None:
        element_a = polymer_values[pos_a]
        pos_c = polymer_nexts[pos_a]
        element_c = polymer_values[pos_c]
        element_pair = element_a + element_c
        if element_pair in subs:
            element_b = subs[element_pair]
            pos_b = len(polymer_values)
            polymer_values.append(element_b)
            polymer_nexts[pos_a] = pos_b
            polymer_nexts.append(pos_c)
        pos_a = pos_c
        pos_c = polymer_nexts[pos_a]

def score():
    occurances_dict = Counter(polymer_values)
    occurances = list(occurances_dict.values())
    occurances.sort()
    ans = occurances[-1] - occurances[0]
    return ans

pair_expansions = {key:[] for key in subs}
for key in pair_expansions:
    if key not in subs:
        continue
    a,c = key[0], key[1]
    b = subs[key]
    if a+b in subs:
        pair_expansions[key].append(a+b)
    if b+c in subs:
        pair_expansions[key].append(b+c)
#print(pair_expansions)

pair_counts = {pair:0 for pair in subs}
for i in range(len(polymer_string)-1):
    pair_counts[polymer_string[i:i+2]] += 1
#print(sum(pair_counts.values()))

def iterate(pair_counts):
    new_pair_counts = {k:0 for k in pair_counts}
    for pair in pair_counts:
        new_pairs = pair_expansions[pair]
        for new_pair in new_pairs:
            new_pair_counts[new_pair] += pair_counts[pair]
    return new_pair_counts

def score_counts(pair_counts):
    occ_dict = {}
    for pair in pair_counts:
        for c in pair:
            if c in occ_dict:
                occ_dict[c] += pair_counts[pair]
            else:
                occ_dict[c] = pair_counts[pair]
    occ_dict[polymer_string[0]] += 1
    occ_dict[polymer_string[-1]] += 1
    for element in occ_dict:
        occ_dict[element] = occ_dict[element]//2
    print(occ_dict)
    occurances = list(occ_dict.values())
    occurances.sort()
    ans = occurances[-1] - occurances[0]
    return ans

#print(pair_counts)
for i in range(10):
    pair_counts = iterate(pair_counts)
    #print(pair_counts)
print("part1", score_counts(pair_counts))

for i in range(30):
    pair_counts = iterate(pair_counts)
    #print(pair_counts)
print("part2", score_counts(pair_counts))


