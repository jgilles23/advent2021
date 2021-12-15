import numpy as np
import itertools


with open("day11_input.txt") as file:
    inp = [[int(y) for y in x[:-1]] for x in file]
inp = np.array(inp)
print(inp)

N = inp.shape[0]

def step(energy):
    energy += 1
    flash_count = 0
    for i,j in itertools.product(range(N), range(N)):
        flash_count += pulse(energy, i, j, initial=True)
    return flash_count

def pulse(energy, i, j, initial=False):
    #Check the i & j are in range:
    if i < 0 or i >= N or j < 0 or j >= N:
        return 0
    #Check that octipus has not already pulsed
    if energy[i,j] == 0:
        return 0
    #On initial run through, the energy levels have already been increased by 1
    if initial == False:
        energy[i,j] += 1
    #Do nothing if energy is low
    if energy[i,j] <= 9:
        return 0
    #Energy equal to 9
    energy[i,j] = 0
    flash_count = 1
    for a,b in itertools.product([-1,0,1], [-1,0,1]):
        flash_count += pulse(energy, i+a, j+b)
    return flash_count

flash_count = 0
for x in range(100):
    new_flashes = step(inp)
    #print(x, new_flashes)
    flash_count += new_flashes

print("part1", flash_count)

while new_flashes < N*N:
    x += 1
    if x%100 == 0: print("step",x)
    new_flashes = step(inp)
    #print(new_flashes)

print("part2", x + 1)