import numpy as np

inp = []
with open("day9_input.txt") as file:
    inp = [[int(y) for y in x[:-1]] for x in file]
A = np.array(inp)

lower_than = np.full_like(A,0)
lower_than[1:,:] += A[1:,:] < A[:-1,:] #above
lower_than[:-1,:] += A[:-1,:] < A[1:,:] #below
lower_than[:,1:] += A[:,1:] < A[:,:-1] #left
lower_than[:,:-1] += A[:,:-1] < A[:,1:] #right
lower_than[0,:] += 1
lower_than[-1,:] += 1
lower_than[:,0] += 1
lower_than[:,-1] += 1

risk_level = 0
low_points = []
for i in range(lower_than.shape[0]):
    for j in range(lower_than.shape[1]):
        if lower_than[i,j] == 4:
            risk_level += A[i,j] + 1
            low_points.append((i,j))
print("part1", risk_level)

basin_sizes = []
for low_point in low_points:
    flood = np.full_like(A, False, dtype=np.bool_)
    flood[low_point] = True
    previous_sum = 0
    while np.sum(flood) > previous_sum:
        previous_sum = np.sum(flood)
        for i in range(100):
            for j in range(100):
                if flood[i,j] == False:
                    continue
                if i-1 >= 0 and A[i-1,j] != 9:
                    flood[i-1,j] = True
                if i+1 < 100 and A[i+1,j] != 9:
                    flood[i+1,j] = True
                if j-1 >= 0 and A[i,j-1] != 9:
                    flood[i,j-1] = True
                if j+1 < 100 and A[i,j+1] != 9:
                    flood[i,j+1] = True
    basin_sizes.append(previous_sum)
basin_sizes.sort()
print("part2", basin_sizes[-1]*basin_sizes[-2]*basin_sizes[-3])
