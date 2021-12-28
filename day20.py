import numpy as np

with open("day20_input.txt") as file:
    algo = file.readline()[:-1]
    file.readline()
    lines = [x[:-1] for x in file]
#print(lines)

grid = np.full((len(lines), len(lines[0])), False)
for y, line in enumerate(lines):
    for x, character in enumerate(line):
        if character == "#":
            grid[y,x] = True

def print_grid(grid):
    print()
    for y in range(grid.shape[0]):
        print("".join(["#" if v else "." for v in grid[y,:]]))

def get_item(y, x, grid, offset, outside):
    y = y - offset
    x = x - offset
    if y<0 or y>=grid.shape[0] or x<0 or x>=grid.shape[1]:
        return outside
    else:
        return grid[y, x]

def iterate(grid, outside):
    offset = 1
    new_grid = np.full((grid.shape[0]+offset*2, grid.shape[1]+offset*2), False)
    for y in range(new_grid.shape[0]):
        for x in range(new_grid.shape[1]):
            a = 0
            a += 256*get_item(y-1, x-1, grid, offset, outside)
            a += 128*get_item(y-1, x, grid, offset, outside)
            a += 64*get_item(y-1, x+1, grid, offset, outside)
            a += 32*get_item(y, x-1, grid, offset, outside)
            a += 16*get_item(y, x, grid, offset, outside)
            a += 8*get_item(y, x+1, grid, offset, outside)
            a += 4*get_item(y+1, x-1, grid, offset, outside)
            a += 2*get_item(y+1, x, grid, offset, outside)
            a += 1*get_item(y+1, x+1, grid, offset, outside)
            if algo[a] == "#":
                new_grid[y,x] = True
    return new_grid


# print_grid(grid)
for i in range(50//2):
    print(i)
    grid = iterate(grid, outside=False)
    # print_grid(grid)
    grid = iterate(grid, outside=True)
    # print_grid(grid)

print("part1", np.sum(grid))

#5705 is too high

exit()

lights = set()
with open("day20_input.txt") as file:
    algo = file.readline()[:-1]
    file.readline()
    for y, line in enumerate(file):
        for x, character in enumerate(line[:-1]):
            if character == "#":
                lights.add((y, x))

def iterate(lights):
    def add_to_sums(y, x, value, sums):
        # if y==0 and x==0:
        #     print((y,x), "gets", value)
        if (y, x) in sums:
            sums[(y,x)] += value
        else:
            sums[(y,x)] = value

    sums = {}
    for y, x in lights:
        # print("from", (y,x))
        add_to_sums(y-1, x-1, 1,sums)
        add_to_sums(y-1, x, 2,sums)
        add_to_sums(y-1, x+1, 4,sums)
        add_to_sums(y, x-1, 8,sums)
        add_to_sums(y, x, 16,sums)
        add_to_sums(y, x+1, 32,sums)
        add_to_sums(y+1, x-1, 64,sums)
        add_to_sums(y+1, x, 128,sums)
        add_to_sums(y+1, x+1, 256,sums)
    
    # print("sample", sums[(0,0)])
    lights = set()
    for pos, value in sums.items():
        if algo[value] == "#":
            lights.add(pos)
    return lights

def print_grid(lights):
    ys, xs = zip(*lights)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    grid = np.full((max_y-min_y+1, max_x-min_x+1), ".")
    for y,x in lights:
        grid[y-min_y, x-min_x] = "#"
    print()
    print("num_lights", len(lights))
    for y in range(grid.shape[0]):
        s = "".join(grid[y, :])
        print(s)

print_grid(lights)
for i in range(2):
    lights = iterate(lights)
    print_grid(lights)

print("part1", len(lights))

#5662 is too low