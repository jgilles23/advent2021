from types import new_class
from sortedcontainers import SortedDict
from sortedcontainers import SortedSet

with open("day23_input.txt") as file:
    file.readline()
    file.readline()
    inputs = [x for x in file.readline()[:-1] if x != "#" and x != " "]
    inputs += [x for x in file.readline()[:-1] if x != "#" and x != " "]
# print(inputs)

pack = {}

def print_grid(grid, pack=None, **kwargs):
    s = str_grid(grid, pack=pack, **kwargs)
    print(s[:11])
    for i in range(12,len(grid)+1,5):
        print("  " + " ".join(s[i:i+4]))

def str_grid(grid, mark_x=None, mark_symbols=None, pack=None):
    s = "".join(grid)
    if mark_x is not None:
        # print("mark_x", mark_x)
        for i, x in enumerate(mark_x):
            if s[x] == ".":
                if mark_symbols is not None:
                    sym = mark_symbols[i]
                else:
                    sym = "x"
                s = s[:x] + sym + s[x+1:]
            else:
                if mark_symbols is not None:
                    sym = mark_symbols[i]
                else:
                    sym = "X"
                s = s[:x] + sym + s[x+1:]
    for i in range(2,10,2):
        if s[i] == ".":
            s = s[:i] + "," + s[i+1:]
    new_s = s[:11]
    for i in range(11,len(grid),4):
        new_s += "|" + s[i:i+4]
    return new_s

pack["move cost"] = {"A":1, "B":10, "C":100, "D":1000}

pack["grid_inhabitants"] = ["."]*11 + inputs
pack["grid_types"] = ["h"]*2 + ["e", "h"]*4 + ["h"] + ["A", "B", "C", "D"]*2
pack["grid_goal"] = [x if x in "ABCD" else "." for x in pack["grid_types"]]
pack["grid_goal"] = "".join(pack["grid_goal"])
pack["grid_connections"] = [[1]] + [[i-1, i+1] for i in range(1,10)] + [[9]]
for i,j in zip(range(2,9,2), range(11,15)):
    pack["grid_connections"][i].append(j)
pack["grid_connections"] += [[i, j] for i,j in zip(range(2,9,2), range(15,19))]
pack["grid_connections"] += [[i] for i in range(11,15)]
pack["species_goals"] = {"A":[15,11], "B":[16,12], "C":[17,13], "D":[18,14]}

# print(pack["grid_connections"])
print_grid(pack["grid_inhabitants"])
# print_grid([str(len(x)) for x in pack["grid_connections"]])
# print_grid([x[0] for x in pack["grid_types"]])
# print_grid(pack["grid_goal"])

def classify_type(i, grid, species, pack=None):
    #Returns the type of space: h-hallway, e-entry, X-final resting, W-resting column but not correct space, Y-wrong column
    if pack["grid_types"][i] == "h":
        return "h"
    elif pack["grid_types"][i] == "e":
        return "e"
    elif pack["grid_types"][i] == species:
        if i >= len(grid)-4:
            return "X"
        elif all([grid[j] == species for j in range(i+4,len(grid),4)]):
            return "X"
        else:
            return "W" #Right letter, but too close
    else:
        return "Y"

def get_moves(i, grid, species=None, starting_type=None, previous=None, energy=0, level=0, pack=None):
    if species is None:
        species = grid[i]
        starting_type = classify_type(i, grid, species, pack=pack)
    current_type = classify_type(i, grid, species, pack=pack)
    # print("- "*level, "i", i, "species", species, "grid", grid, "starting_type", starting_type, "current_type", current_type, "previous", previous, "energy", energy)
    if starting_type == "h":
        if current_type in "heW":
            options = []
        elif current_type == "X":
            return [(energy, i)]
        elif current_type == "Y":
            return []
    elif starting_type == "e":
        raise Exception("e not a valid starting type")
    elif starting_type == "X":
        return []
    elif starting_type in "WY":
        if current_type == "h":
            options = [(energy, i)]
        elif current_type in "eWY":
            options = []
        elif current_type == "X":
            return [(energy,i)]
    #(energy, i)
    #If made it here, need to search additonal spaces
    # print(i, pack["grid_connections"][i], pack["grid_connections"][16])
    for j in pack["grid_connections"][i]:
        if j == previous or grid[j] != ".":
            continue
        new_energy = energy + pack["move cost"][species]
        options += get_moves(j, grid, species=species, starting_type=starting_type, previous=i, energy=new_energy, level=level+1, pack=pack)
    return options 

pack["minimum_additional_lookup"] = {
    "A":[3,2,1,2,3,4,5,6,7,8,9,0,4,6,8,0,5,7,9],
    "B":[5,4,3,2,1,2,3,4,5,6,7,4,0,4,6,5,0,5,7],
    "C":[7,6,5,4,3,2,1,2,3,4,5,6,4,0,4,7,5,0,7],
    "D":[9,8,7,6,5,4,3,2,1,2,3,8,6,4,0,9,7,5,0]}
pack["minimum_additional_lookup"] = {k:[v*pack["move cost"][k] for v in lst] for k, lst in pack["minimum_additional_lookup"].items()}
pack["minimum_additional_lookup"]["."] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# print(pack["minimum_additional_lookup"])
pack["discovered_grids"] = {}

pack["best_energy"] = 100000

def min_add_energy(grid, pack=None):
    #Calculate the minimum additonal energy to get the grid to final positon based on current position (consider permanent blocking)
    energy = 0
    for i in range(len(grid)):
        energy += pack["minimum_additional_lookup"][grid[i]][i]
    if grid[15] != "A": energy += 1
    if grid[16] != "B": energy += 10
    if grid[17] != "C": energy += 100
    if grid[18] != "D": energy += 1000
    if len(grid) > 19:
        if grid[19] != "A": energy += 2*1
        if grid[20] != "B": energy += 2*10
        if grid[21] != "C": energy += 2*100
        if grid[22] != "D": energy += 2*1000
        if grid[23] != "A": energy += 3*1
        if grid[24] != "B": energy += 3*10
        if grid[25] != "C": energy += 3*100
        if grid[26] != "D": energy += 3*1000
    return energy
    
def move(i, grid, energy=0, pack=None):
    #Grid should be provided as a string
    options = SortedSet()
    moves = get_moves(i, grid, energy=energy, pack=pack)
    for energy, j in moves:
        new_grid = grid[:i] + "." + grid[i+1:]
        new_grid = new_grid[:j] + grid[i] + new_grid[j+1:]
        min_remaining_energy = min_add_energy(new_grid, pack=pack)
        pack["best_energy"]
        if min_remaining_energy + energy >= pack["best_energy"]:
            #Do nothing as this energy level will never be the winner
            continue
        min_energy = 1.1*min_remaining_energy + energy
        if new_grid == pack["grid_goal"]:
            if energy < pack["best_energy"]:
                pack["best_energy"] = energy
                print("FOUND A WINNING GRID", energy, new_grid)
            #Do nothing if the energy isn't better than discovered before
        if new_grid in pack["discovered_grids"]:
            if energy < pack["discovered_grids"][new_grid]:
                pack["discovered_grids"][new_grid] = energy
                options.add((min_energy, -1*energy, new_grid))
            #Do nothing if the energy isn't better than what has been discovered before

        else:
            pack["discovered_grids"][new_grid] = energy
            options.add((min_energy, -1*energy, new_grid))
    return options

def move_all(grid, energy=0, pack=None):
    #Make all possible moves in the grid
    options = SortedSet()
    for i in range(len(grid)):
        if grid[i] == ".":
            continue
        options.update(move(i,grid,energy=energy, pack=pack))
    return options

def iterate(options, pack=None):
    _, energy, grid = options.pop(0)
    options.update(move_all(grid, -1*energy, pack=pack))
    return options

print("####################")

# grid = ".A..........BBBCBBB"
# print_grid(grid)
# q = get_moves(1, grid)
# print(q)
# print_grid(grid, mark_x=[x[1] for x in q], mark_symbols=[str(x[0])[0] for x in q])
# exit()


grid = "".join(pack["grid_inhabitants"])
options = SortedSet([(0,0,grid)])
for i in range(1,1000):
    options = iterate(options, pack=pack)
    if len(options) == 0:
        break
    x = options[0]
    if i%100 == 0:
        print("BEST after", i, ":", (x[0], x[1], str_grid(x[2])), "num options", len(options))
    # for x in options[:1]:
    #     print((x[0], x[1], str_grid(x[2])))
else:
    print("Made it through all the iterations")

print("part1", pack["best_energy"])



#PART 2
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
pack = {"grid_inhabitants":pack["grid_inhabitants"]}

pack["move cost"] = {"A":1, "B":10, "C":100, "D":1000}
pack["grid_types"] = ["h"]*2 + ["e", "h"]*4 + ["h"] + ["A", "B", "C", "D"]*4
pack["grid_goal"] = "".join([x if x in "ABCD" else "." for x in pack["grid_types"]])
pack["grid_connections"] = [[1]] + [[i-1, i+1] for i in range(1,10)] + [[9]]
for i,j in zip(range(2,9,2), range(11,15)):
    pack["grid_connections"][i].append(j)
pack["grid_connections"] += [[j, i+4] for j,i in zip(range(2,9,2),range(11,15))]
pack["grid_connections"] += [[i-4, i+4] for i in range(15,19)]
pack["grid_connections"] += [[i-4, i+4] for i in range(19,23)]
pack["grid_connections"] += [[i-4] for i in range(23,27)]
pack["species_goals"] = {"A":[23,19,15,11], "B":[24,20,16,12], "C":[25,21,17,13], "D":[26,22,18,14]}

pack["minimum_additional_lookup"] = {
    "A":[3,2,1,2,3,4,5,6,7,8,9, 0,4,6,8, 0,5,7,9, 0,6,8,10, 0,7,9,11],
    "B":[5,4,3,2,1,2,3,4,5,6,7, 4,0,4,6, 5,0,5,7, 6,0,6,8,  7,0,7,9],
    "C":[7,6,5,4,3,2,1,2,3,4,5, 6,4,0,4, 7,5,0,5, 8,6,0,8,  9,7,0,7],
    "D":[9,8,7,6,5,4,3,2,1,2,3, 8,6,4,0, 9,7,5,0, 10,8,6,0, 11,9,7,0]}
pack["minimum_additional_lookup"] = {k:[v*pack["move cost"][k] for v in lst] for k, lst in pack["minimum_additional_lookup"].items()}
pack["minimum_additional_lookup"]["."] = [0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
# print(pack["minimum_additional_lookup"])

grid = "".join(pack["grid_inhabitants"][:15]) + "DCBADBAC" + "".join(pack["grid_inhabitants"][15:])
# print_grid(grid)
pack["discovered_grids"] = {}
pack["best_energy"] = 10000000

# print_grid("".join([str(x[2])[-1] if len(x)>2 else "x" for x in pack["grid_connections"]]))



# grid = ".A........."+"...B"+"...B"+"...B"+".BBB"
# # print(str_grid(grid))
# print_grid(grid)
# i=25
# q = get_moves(i, grid, pack=pack)
# print(q)
# print_grid(grid, mark_x=[x[1] for x in q]+[i], mark_symbols=[str(x[0])[0] for x in q]+["X"])

# print(pack["grid_connections"][15])
# exit()

options = SortedSet([(0,0,grid)])
for i in range(1,100000):
    options = iterate(options, pack=pack)
    if len(options) == 0:
        break
    x = options[0]
    if i%1000 == 0:
        print("BEST after", i, ":", (round(x[0],1), x[1], str_grid(x[2])), "num options", len(options))
    # for x in options[:1]:
    #     print((x[0], x[1], str_grid(x[2])))
else:
    print("Made it through all the iterations")

print("part2", pack["best_energy"])