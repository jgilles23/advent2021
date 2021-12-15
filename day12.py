graph = {}
with open("day12_input.txt") as file:
    for line in file:
        left, right = line[:-1].split("-")
        if left not in graph: graph[left] = set()
        graph[left].add(right)
        if right not in graph: graph[right] = set()
        graph[right].add(left)
print(graph)
cave_type = {}
for key in graph:
    if key.upper() == key:
        cave_type[key] = "big"
    else:
        cave_type[key] = "small"
print(cave_type)


def iterate(visited, position, allow_twice=False, visited_twice=None):
    if position == "end":
        return 1
    if position in visited:
        if allow_twice and visited_twice is None and position != "start":
            visited_twice = position
        else:
            return 0
    #Add positon to the list of visited places
    new_visited = visited.copy()
    if cave_type[position] == "small":
        new_visited.add(position)
    num_paths = 0
    for new_position in graph[position]:
        num_paths += iterate(new_visited, new_position, allow_twice, visited_twice)
    return num_paths

q = iterate(set(), "start")
print("part1", q)

q = iterate(set(), "start", allow_twice=True)
print("part2", q)

