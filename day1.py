depths = []
with open("day1_input.txt") as file:
    for line in file:
        depths.append(int(line[:-1]))



#part 1
previous = depths[0]
count = 0
for a, d in zip(depths[:-1], depths[1:]):
    if d > a:
        count += 1

print("part1", count)

#part 2
windows = []
for a, b, c in zip(depths[:-2], depths[1:-1], depths[2:]):
    windows.append(a+b+c)
count = 0
for p, d in zip(windows[:-1], windows[1:]):
    if d > p:
        count += 1

print("part2", count)