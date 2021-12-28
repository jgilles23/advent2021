import numpy as np
from numpy import matmul as mm
from math import sin
from math import cos

from numpy.core.fromnumeric import transpose
from numpy.linalg.linalg import _matrix_rank_dispatcher

np.set_printoptions(linewidth=200, threshold=2000)

scanners_detections = []
with open("day19_input.txt") as file:
    file.readline()
    detections = []
    for line in file:
        if line[:-1] == "":
            file.readline()
            scanners_detections.append(detections)
            detections = []
            continue
        detections.append([int(x) for x in line[:-1].split(",")])
scanners_detections.append(detections)
scanners_detections = [np.transpose(np.array(x)) for x in scanners_detections]
#for i, d in enumerate(scanners_detections): print(i,"\n",d)

R = {}
t = np.pi/2
Rn = np.array([[1,0,0],[0,1,0],[0,0,1]])
Rx = np.array([[1,0,0],[0,0,-1],[0,1,0]])
Ry = np.array([[0,0,1],[0,1,0],[-1,0,0]])
Rz = np.array([[0,-1,0],[1,0,0],[0,0,1]])
R_xs = [Rn, Rx, Rx@Rx, Rx@Rx@Rx]
#Establish the 24 rotations
R = [r for r in R_xs]
R += [mm(r,Ry) for r in R_xs]
R += [mm(mm(r,Ry),Ry) for r in R_xs]
R += [mm(mm(mm(r,Ry),Ry),Ry) for r in R_xs]
R += [mm(r,Rz) for r in R_xs]
R += [mm(mm(mm(r,Rz),Rz),Rz) for r in R_xs]
mirror_z = np.array([[1,0,0],[0,1,0],[0,0,-1]])
R += [r@mirror_z for r in R]


# p = np.array([[9,1,2],[8,1,2],[7,1,2]]).transpose()
# for r in R:
#     q = R@p
#     print(q)

# exit()

# p = np.transpose(np.array([[498, 1542, -378]]))
# for r in R:
#     q = np.dot(r, p)
#     print(q[:,0])
# exit()

def count_common_points(d0, d1):
    count = 0
    for i in range(d0.shape[1]):
        for j in range(d1.shape[1]):
            if np.all(d0[:,i] == d1[:,j]):
                count += 1
    return count


def get_distance_matrix(d):
    dm = np.array([[np.linalg.norm(d[:,i] - d[:,j]) if i>j else 0 for i in range(d.shape[1])] for j in range(d.shape[1])])
    return np.round(dm, 5)

#dm_a = get_distance_matrix(scanners_detections[0])
#dm_b = get_distance_matrix(scanners_detections[2])

def get_connections(dm_a, dm_b):
    #dm_a = get_distance_matrix(scanners_detections[0])
    #dm_b = get_distance_matrix(scanners_detections[2])
    dm_b_set = set(float(x) for x in np.nditer(dm_b) if x!=0)
    #Count all of the distances that are the same
    a_to_b_connections = np.full((dm_a.shape[0], dm_b.shape[0]), 0)
    for a_i in range(dm_a.shape[0]):
        for a_j in range(a_i+1, dm_a.shape[0]):
            if dm_a[a_i, a_j] in dm_b_set:
                d_0, d_1 = np.argwhere(dm_a[a_i, a_j] == dm_b)[0]
                a_to_b_connections[a_i, d_0] += 1
                a_to_b_connections[a_i, d_1] += 1
                a_to_b_connections[a_j, d_0] += 1
                a_to_b_connections[a_j, d_1] += 1
    #print(a_to_b_connections)
    #print(np.argwhere(a_to_b_connections >= 11))
    #Based on count of distances that are the same, derive the connections between the scans
    a_to_b_map = {}
    for a_i, b_i in np.argwhere(a_to_b_connections >= 11):
        a_to_b_map[a_i] = b_i
    #print(a_to_b_map)
    return a_to_b_map

#calculate distance matrices
dms = [get_distance_matrix(d) for d in scanners_detections]

num_scanners = len(scanners_detections)
connections = np.full((num_scanners, num_scanners), {})
connections_count = np.full_like(connections, 0)
for i in range(num_scanners):
    #print(i)
    for j in range(i+1, num_scanners):
        c = get_connections(dms[i], dms[j])
        connections[i,j] = c
        connections_count[i,j] = len(c)

print("Connections counted")
print(connections_count)

def count_unique(beacons):
    beacons_set = set([tuple(beacons[:,i]) for i in range(beacons.shape[1])])
    return len(beacons_set)

def rotate_b_to_a(d_a_ind, d_b_ind):
    d_a = scanners_detections[d_a_ind]
    d_b = scanners_detections[d_b_ind]

    connects = list(connections[d_a_ind, d_b_ind].items()) #list of tuples (a_ind, b_ind)
    for r in R:
        d_b_rotated = r@d_b
        delta = d_b_rotated[:,[connects[0][1]]] - d_a[:, [connects[0][0]]]
        d_b_rotated -= delta
        #print(0, d_a[:,connects[0][0]], d_b_rotated[:, connects[0][1]])
        #print(1, d_a[:,connects[1][0]], d_b_rotated[:, connects[1][1]])
        for i in range(len(connects)):
            if not np.all(d_a[:,connects[i][0]] == d_b_rotated[:, connects[i][1]]):
                break
        else:
            previous_count = d_a.shape[1] + d_b.shape[1]
            new_count = count_unique(np.concatenate([d_a, r@d_b - delta], 1))
            print("rotate", d_b_ind, "to", d_a_ind, "Found it.", "previously", previous_count, "newly", new_count) 
            #If you multiply b by r and then add delta you get into the same symetry as a
            return r, delta
    else:
        pass
        print((d_a_ind, d_b_ind), "Nope")

#Get all the transformations that can be made
transform_x_to_y = {} #(x,y):(r, delta)
for a in range(num_scanners):
    for b in range(a+1, num_scanners):
        if connections_count[a,b] >= 11:
            ret = rotate_b_to_a(a, b)
            if ret: #(r, delta) a = r.b + delta
                transform_x_to_y[(b,a)] = ret
                transform_x_to_y[(a,b)] = (ret[0].transpose(), -1*ret[0].transpose()@ret[1])
print(transform_x_to_y.keys())


transform_x_to_y_backup = {k:v for k,v in transform_x_to_y.items()}

def transform_to_x_rec(x):
    #print("transform", x)
    sub_problems = {}
    for i in range(num_scanners):
        if i == x:
            continue
        if (i,x) in transform_x_to_y:
            sub_problems[i] = transform_x_to_y.pop((i,x))
    for i in range(num_scanners):
        if (x,i) in transform_x_to_y:
            del transform_x_to_y[(x,i)]
    sub_detections = [scanners_detections[x]]
    for i in sub_problems:
        rotation, translation = sub_problems[i]
        sub_detections.append(rotation@transform_to_x_rec(i) - translation)
    sub_detections = np.concatenate(sub_detections, 1)
    return sub_detections

def transform_to_x_rec_scanners(x):
    sub_problems = {}
    for i in range(num_scanners):
        if i == x:
            continue
        if (i,x) in transform_x_to_y_backup:
            sub_problems[i] = transform_x_to_y_backup.pop((i,x))
    for i in range(num_scanners):
        if (x,i) in transform_x_to_y_backup:
            del transform_x_to_y_backup[(x,i)]
    sub_detections = [np.array([[0,0,0]]).transpose()]
    for i in sub_problems:
        rotation, translation = sub_problems[i]
        sub_detections.append(rotation@transform_to_x_rec_scanners(i) - translation)
    sub_detections = np.concatenate(sub_detections, 1)
    return sub_detections


print("Initial beacons count", sum([d.shape[1] for d in scanners_detections]))
q = transform_to_x_rec(0)
print("part1", count_unique(q))

#Calculate the farthest distance
w = transform_to_x_rec_scanners(0)
print(w)
print(w.shape)

max_distance = 0
for i in range(w.shape[1]):
    for j in range(i+1, w.shape[1]):
        dist = np.sum(np.abs(w[:,i] - w[:,j]))
        if dist > max_distance:
            max_distance = dist
print("part2", max_distance)
#16098 is too high

# print("1 & 0 #", scanners_detections[0].shape[1] + scanners_detections[1].shape[1])
# r, d = transform_x_to_y[(1,0)]
# q = [scanners_detections[0], r@scanners_detections[1] + d]
# q = np.concatenate(q,1)
# print("reduced", count_unique(q))

exit()

q = transform_to_x_rec(0)
detetors_set = set([tuple(q[:,i]) for i in range(q.shape[1])])
print(q)
print("New beacons count", len(detetors_set))


exit()


#Determine the transformations that will put everthing into the same reference space as the 0 scanner
untransformed = set(range(1, num_scanners))
i = 0
while len(untransformed) > 0:
    for a in range(num_scanners):
        if (a,0) in transform_x_to_y:
            if a in untransformed:
                untransformed.remove(a)
            r_a0, delta_a0 = transform_x_to_y[(a,0)]
            for b in range(num_scanners):
                if ((b,a) in transform_x_to_y) and ((b,0) not in transform_x_to_y):
                    r_ba, delta_ba = transform_x_to_y[(b,a)]
                    transform_x_to_y[(b,0)] = (mm(r_ba, r_a0), delta_ba + delta_a0)

# print(transform_x_to_y.keys())

# rotate_b_to_a(2, 4)

detectors_rotated = [scanners_detections[0]]
for i in range(1, num_scanners):
    r, delta = transform_x_to_y[(i,0)]
    detectors_rotated.append(r@scanners_detections[i] - delta)
detectors_0 = np.concatenate(detectors_rotated, 1)
# print(detectors_0)

print("Initial beacons count", detectors_0.shape[1])
detetors_set = set([tuple(detectors_0[:,i]) for i in range(detectors_0.shape[1])])
#print(detetors_set)
print("New beacons count", len(detetors_set))

print("part1", detectors_0.shape[1] - np.sum(connections_count))
# print(transform_x_to_y[(0,0)])
