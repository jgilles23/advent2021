import re
import numpy as np
inp = []
with open("day5_input.txt") as file:
    for line in file:
        inp.append([int(x) for x in re.split(",| ", line[:-1]) if x!="->"])


#part1
def plus_minus(q):
    if q == 0: return 0
    elif q > 0: return 1
    else: return -1

def compute(straight_only=True):
    M = np.full((1000,1000), 0)
    for x1, y1, x2, y2 in zip(*zip(*inp)):
        if straight_only and (x1!=x2) and (y1!=y2):
            continue
        inc_x = plus_minus(x2-x1)
        inc_y = plus_minus(y2-y1)
        L = max(abs(x2-x1), abs(y2-y1))
        for i in range(L+1):
            M[x1+i*inc_x, y1+i*inc_y] += 1
    return(sum(sum(M >= 2)))

print("part1", compute(True))
print("part2", compute(False))
