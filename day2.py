commands = []
values = []
with open('day2_input.txt') as file:
    for line in file:
        line = line.split(" ")
        commands.append(line[0])
        values.append(int(line[1][:-1]))

#print(commands[:10], values[:10])

#part1
depth = 0
pos = 0
for command, value in zip(commands, values):
    if command == "down":
        depth += value
    elif command == "up":
        depth -= value
    elif command == "forward":
        pos += value
    else:
        raise Exception()
print("part1", depth*pos)

#part2
depth = 0
pos = 0
aim = 0
for command, value in zip(commands, values):
    if command == "down":
        aim += value
    elif command == "up":
        aim -= value
    elif command == "forward":
        pos += value
        depth += aim*value
print("part2", depth*pos)