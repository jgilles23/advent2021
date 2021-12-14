inp = []
with open("day3_input.txt") as file:
    for line in file:
        inp.append([int(x) for x in line[:-1]])

#part1
sums = [sum(a) for a in zip(*inp)]
print(sums)
gamma_parts = [1 if x > len(inp)/2 else 0 for x in sums]
gamma = int("".join([str(x) for x in gamma_parts]),2)
epsilon = 2**12 - gamma - 1
print(gamma, epsilon)
print("part1", gamma*epsilon)

#part2
def shorten(A, pos, c):
    B = [x[pos] for x in A]
    s = sum(B)
    if s >= len(B)/2:
        val = c
    else:
        val = (c+1)%2
    A = [x for x in A if x[pos]==val]
    return(A)

def to_int(val):
    return int("".join([str(x) for x in val]),2)

A = [[y for y in x] for x in inp]
pos = 0
while True:
    if len(A) <= 1:
        break
    #print(len(A))
    A = shorten(A, pos, 1)
    pos = (pos + 1)%12
oxygen = to_int(A[0])

A = [[y for y in x] for x in inp]
pos = 0
while True:
    if len(A) <= 1:
        break
    #print(len(A))
    A = shorten(A, pos, 0)
    pos = (pos + 1)%12
co2 = to_int(A[0])

print(oxygen, co2)
print("part2", oxygen*co2)

