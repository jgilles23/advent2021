import numpy as np

with open("day7_input.txt") as file:
    for line in file:
        crab_positions = [int(x) for x in line[:-1].split(",")]
crab_positions = np.array(crab_positions)
#print(crab_positions)

meeting_positions = np.full(max(crab_positions)+1, 0)

for i in range(len(meeting_positions)):
    meeting_positions[i] = sum(abs(i-crab_positions))
least_fuel = min(meeting_positions)
print("part1", least_fuel)

meeting_positions = np.full(max(crab_positions)+1, 0)
fuel_costs = np.arange(0,max(crab_positions)+1)
for i in range(1,len(fuel_costs)):
    fuel_costs[i] += fuel_costs[i-1]
fuel_costs_reverse = fuel_costs[::-1]
print(fuel_costs, fuel_costs_reverse)

for crab_pos in crab_positions:
    meeting_positions[crab_pos:] += fuel_costs[:(len(meeting_positions)-crab_pos)]
    meeting_positions[:(crab_pos+1)] += fuel_costs_reverse[(len(fuel_costs_reverse)-crab_pos-1):]
print(meeting_positions)
print("part2",min(meeting_positions))
#print(max(crab_positions))