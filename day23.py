with open("day23_input.txt") as file:
    file.readline()
    file.readline()
    inputs = [x for x in file.readline()[:-1] if x != "#" and x != " "]
    inputs += [x for x in file.readline()[:-1] if x != "#" and x != " "]
print(inputs)

def print_grid(grid):
    print("".join(grid[:11]))
    print(" " + " " + grid[11] + " " + grid[12] + " " +grid[13] + " " + grid[14] + " " + " ")
    print(" " + " " + grid[15] + " " + grid[16] + " " +grid[17] + " " + grid[18] + " " + " ")

move_cost = {"A":1, "B":10, "C":100, "D":1000}

grid_inhabitants = ["."]*11 + inputs
grid_types = ["hall"]*2 + ["entry", "hall"]*4 + ["hall"] + ["A", "B", "C", "D"]*2
grid_goal = [x if x in "ABCD" else "." for x in grid_types]
grid_connections = [[1]] + [[i-1, i+1] for i in range(1,10)] + [[10]]
for i,j in zip(range(2,9,2), range(11,15)):
    grid_connections[i].append(j)
grid_connections += [[i, j] for i,j in zip(range(2,9,2), range(15,19))]
grid_connections += [[i] for i in range(11,15)]

print(grid_connections)
print_grid(grid_inhabitants)
print_grid([str(len(x)) for x in grid_connections])
print_grid([x[0] for x in grid_types])
print_grid(grid_goal)

def get_moves(i, grid, previous=None):
    pass


explored_states = {tuple(grid_inhabitants):0}
def expand(grid):
    for i in range(len(grid)):
        if grid[i] not in "ABCD":
            continue
