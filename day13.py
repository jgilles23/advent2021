import re
import numpy as np

dots = set()
instructions_axis = []
instructions_value = []
with open("day13_input.txt") as file:
    mode = "dots"
    for line in file:
        line = line[:-1]
        if line == "":
            mode = "instructions"
            continue
        if mode == "dots":
            x,y = line.split(",")
            dots.add((int(x), int(y)))
        else:
            _,_,axis,value = re.split(" |=", line)
            instructions_axis.append(axis)
            instructions_value.append(int(value))

print("dots",len(dots))
print("instructions_axis", instructions_axis)
print("instructions_value", instructions_value)

def fold(dots, axis, value):
    new_dots = set()
    for dot in dots:
        x,y = dot
        if axis == "y":
            if y < value:
                new_dots.add(dot)
            else:
                new_dots.add((x,value*2-y))
        else:
            if x < value:
                new_dots.add(dot)
            else:
                new_dots.add((value*2-x,y))
    return new_dots

dots = fold(dots, instructions_axis[0], instructions_value[0])
print("part1", len(dots))

for axis, value in zip(instructions_axis[1:], instructions_value[1:]):
    dots = fold(dots, axis, value)
print("num dots", len(dots))
xs, ys = zip(*dots)
max_x = max(xs)
max_y = max(ys)
print(max_x, max_y)

screen = np.full((max_y+1, max_x+1), ".")
for dot in dots:
    x,y = dot
    screen[y,x] = "#"

for row in screen:
    print("".join(row))