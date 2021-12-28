import re

class Prism:
    def __init__(self, mins, maxes, state):
        #Values in form [x_min, x_max, y_min y_max, z_min, z_max]
        self.mins = mins
        self.maxes = maxes
        self.state = state

    def __repr__(self):
        s = "x=" + str((self.mins[0], self.maxes[0])) +\
            ", y=" + str((self.mins[1], self.maxes[1])) +\
            ", z=" + str((self.mins[2], self.maxes[2])) +\
            ", state=" + str(self.state)
        return "<" + s +">"
    
    def equals(self, prism):
        return all([(a==b and c==d) for a,b,c,d in zip(self.mins, prism.mins, self.maxes, prism.maxes)])

    def less_than_50(self):
        return all([a>=-50 and b<=50 for a,b in zip(self.mins, self.maxes)])

    def quick_intersect(self, prism):
        for i in range(3):
            a_min, a_max = self.mins[i], self.maxes[i]
            b_min, b_max = prism.mins[i], prism.maxes[i]
            if a_min > b_max:
                return False
            if a_max < b_min:
                return False
        return True
    
    def count(self):
        if not self.state=="on":
            return 0
            #raise Exception("Attempting to count off")
        dims = [b-a+1 for a,b in zip(self.mins, self.maxes)]
        return dims[0]*dims[1]*dims[2]

    def intersect(self, prism, level=0):
        #test if one prism intersects with another
        types = []
        intersects = True
        for i in range(3):
            #test along axis i for inside, outside(top/bottom), one(top/bottom), or both
            a_min, a_max = self.mins[i], self.maxes[i]
            b_min, b_max = prism.mins[i], prism.maxes[i]
            if a_max > b_max:
                if a_min > b_max: type = "outside top"
                elif a_min >= b_min: type = "split at b_max"
                elif a_min < b_min: type = "split at both"
            elif a_max >= b_min:
                if a_min >= b_min: type = "inside no split"
                elif a_min < b_min: type = "split at b_min"
            elif a_max < b_min:
                if a_min < b_min: type = "outside bottom"
            types.append(type)
            if "outside" in type:
                intersects = False
        #print("- "*level, self, types, "intersects", intersects)
        #Check if intersections occur
        if intersects == False:
            return [self]
        #Splits are required
        for i in range(3):
            if "split at" in types[i]:
                a_min, a_max = self.mins[i], self.maxes[i]
                b_min, b_max = prism.mins[i], prism.maxes[i]
                if "b_max" in types[i]:
                    p0 = Prism(
                        self.mins[:i]+[b_max+1]+self.mins[i+1:],
                        self.maxes[:i]+[a_max]+self.maxes[i+1:],
                        self.state)
                    p1 = Prism(
                        self.mins[:i]+[a_min]+self.mins[i+1:],
                        self.maxes[:i]+[b_max]+self.maxes[i+1:],
                        self.state)
                    new_self = p0.intersect(prism, level+1) + p1.intersect(prism, level+1)
                elif "b_min" in types[i]:
                    p0 = Prism(
                        self.mins[:i]+[b_min]+self.mins[i+1:],
                        self.maxes[:i]+[a_max]+self.maxes[i+1:],
                        self.state)
                    p1 = Prism(
                        self.mins[:i]+[a_min]+self.mins[i+1:],
                        self.maxes[:i]+[b_min-1]+self.maxes[i+1:],
                        self.state)
                    new_self = p0.intersect(prism, level+1) + p1.intersect(prism, level+1)
                elif "both" in types[i]: #Split into 3
                    p0 = Prism(
                        self.mins[:i]+[b_max+1]+self.mins[i+1:],
                        self.maxes[:i]+[a_max]+self.maxes[i+1:],
                        self.state)
                    p1 = Prism(
                        self.mins[:i]+[b_min]+self.mins[i+1:],
                        self.maxes[:i]+[b_max]+self.maxes[i+1:],
                        self.state)
                    p2 = Prism(
                        self.mins[:i]+[a_min]+self.mins[i+1:],
                        self.maxes[:i]+[b_min-1]+self.maxes[i+1:],
                        self.state)
                    new_self = p0.intersect(prism, level+1) + p1.intersect(prism, level+1) + p2.intersect(prism, level+1)
                else:
                    raise Exception("unexpected split")
                #Now that we have finished a split in one axis
                #Need to potentially split in the other axis
                return new_self
        #Splits were not required
        return [self]

def add_prism(new, existing):
    news = new.intersect(existing)
    existings = existing.intersect(new)
    removal_inds = []
    for i, e in enumerate(existings):
        for n in news:
            if n.equals(e):
                removal_inds.append(i)
    for i in removal_inds[::-1]:
        del existings[i]
    if len(existings) == 0:
        return [new], []
    else:
        return news, existings


# p0 = Prism([-10,-10,-10], [20,20,20], "on")
# p1 = Prism([-5,-5,-5], [10,10, 10], "off")
# q = add_prism(new=p1, existing=p0)
# print("##################")
# for prism in q:
#     print("-", prism)

prisms = []
with open("day22_input.txt") as file:
    for line in file:
        values = re.split(" x=|\.\.|,y=|,z=", line[:-1])
        state = values[0]
        values = [int(x) for x in values[1:]]
        mins = values[::2]
        maxes = values[1::2]
        p = Prism(mins, maxes, state)
        prisms.append(p)
        # print(p)

def run_procedure(prisms):
    grid = []
    for j, prism in enumerate(prisms):
        print(j, prism)
        intersecting_inds = []
        for i, existing in enumerate(grid):
            if prism.quick_intersect(existing):
                intersecting_inds.append(i)
        intersecting_existing = [grid.pop(i) for i in intersecting_inds[::-1]]
        prisms_new = [prism]
        while len(prisms_new) > 0:
            p = prisms_new.pop(0)
            for i,existing in enumerate(intersecting_existing):
                if not p.quick_intersect(existing):
                    continue
                news, existings = add_prism(new=p, existing=existing)
                prisms_new.extend(news)
                break
            else:
                #Intersected nothing
                intersecting_existing.append(p)
                continue
            #Broke the for statement
            del intersecting_existing[i] #Remove the existing
            intersecting_existing.extend(existings)
        #cleanup the grid
        grid.extend(intersecting_existing)
        grid = [x for x in grid if x.state=="on"]
    return grid

small_prisms = [x for x in prisms if x.less_than_50()]
small_result = run_procedure(small_prisms)
print("num prisims", len(small_result))
print("part1", sum([x.count() for x in small_result]))

full_result = run_procedure(prisms)
print("num prisims", len(full_result))
print("part2", sum([x.count() for x in full_result]))