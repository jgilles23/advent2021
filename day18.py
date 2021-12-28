with open("day18_input.txt") as file:
    lines = [x[:-1] for x in file]

class Branch:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"

    def assign_parent(self,parent, side):
        self.parent = parent
        self.side = side
        self.left.assign_parent(self, "left")
        self.right.assign_parent(self, "right")

    def up_until_split_left(self, leaf, child_side):
        #print("up left", self)
        if child_side == "left":
            if self.parent is not None:
                self.parent.up_until_split_left(leaf, self.side)
        else:
            self.left.down_right_until_leaf(leaf)
    
    def up_until_split_right(self, leaf, child_side):
        #print("up right", self, "my_side", self.side)
        #print("child_side", child_side)
        if child_side == "right":
            if self.parent is not None:
                self.parent.up_until_split_right(leaf, self.side)
        else:
            self.right.down_left_until_leaf(leaf)
    
    def down_right_until_leaf(self, leaf):
        #print("down right", self)
        self.right.down_right_until_leaf(leaf)
    
    def down_left_until_leaf(self, leaf):
        #print("down left", self)
        self.left.down_left_until_leaf(leaf)
    
    def replace(self, x, side):
        if side == "left":
            self.left = x
            self.left.assign_parent(self, "left")
        else:
            self.right = x
            self.right.assign_parent(self, "right")

    def reduce(self):
        #print("reduce", level, self)
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break
    
    def explode(self, level=0):
        if level == 4:
            self.parent.up_until_split_left(self.left, self.side)
            self.parent.up_until_split_right(self.right, self.side)
            self.parent.replace(Leaf(0), self.side)
            return True
        else:
            if self.left.explode(level=level+1):
                return True
            if self.right.explode(level=level+1):
                return True
            return False
    
    def split(self):
        if self.left.split():
                return True
        if self.right.split():
            return True
        return False
    
    def add(self, right):
        self.replace(Branch(self.left, self.right), "left")
        self.replace(right, "right")
    
    def magnitude(self):
        return 3*self.left.magnitude() + 2*self.right.magnitude()


class Leaf:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def assign_parent(self, parent, side):
        self.parent = parent
        self.side = side
    
    def down_right_until_leaf(self, leaf):
        #print("down right", self)
        self.value += leaf.value
    
    def down_left_until_leaf(self, leaf):
        #print("down left", self)
        self.value += leaf.value
    
    def explode(self, level=0):
        return False
    
    def split(self):
        if self.value > 9:
            left_value = self.value//2
            right_value = self.value - left_value
            new_branch = Branch(Leaf(left_value), Leaf(right_value))
            self.parent.replace(new_branch, self.side)
            return True
        return False

    def magnitude(self):
        return self.value

def compose_tree_rec(s):
    if s[0] == ",":
        s = s[1:]
    if s[0] in "0123456789":
        return s[1:], Leaf(int(s[0]))
    if s[0] == "[":
        s, left = compose_tree_rec(s[1:])
        s, right = compose_tree_rec(s[0:])
        return s[1:], Branch(left, right)
    raise Exception("Did not expect this. "+s)

def compose_tree(s):
    _, t = compose_tree_rec(s)
    t.assign_parent(parent=None, side=None)
    return t



t = compose_tree(lines[0])
#print(t)
for line in lines[1:]:
    new_tree = compose_tree(line)
    t.add(new_tree)
    t.reduce()
    #print(t)
print("part1", t.magnitude())

max_magnitude = 0
for i in range(len(lines)):
    for j in range(len(lines)):
        if i == j:
            continue
        t = compose_tree(lines[i])
        t2 = compose_tree(lines[j])
        t.add(t2)
        t.reduce()
        m = t.magnitude()
        if m > max_magnitude:
            max_magnitude = m
print("part2", max_magnitude)


"""
def convert(s):
    snail = [int(x) if x in "01234567689" else x for x in s if x!=","]
    return snail

def reduce(snail):
    pointer = -1
    level = 0
    while pointer + 1 < len(snail):
        pointer += 1
        #print(pointer, level, snail)
        c = snail[pointer]
        if c == "[":
            level += 1
            if level > 4:
                back_pointer = pointer - 1
                left_value = snail[pointer + 1]
                right_value = snail[pointer + 2]
                forward_pointer = pointer + 4
                #Distribute value left
                while back_pointer > 0:
                    if isinstance(snail[back_pointer], int):
                        snail[back_pointer] += left_value
                        break
                    back_pointer -= 1
                #Distribute value right
                while forward_pointer < len(snail):
                    if isinstance(snail[forward_pointer], int):
                        snail[forward_pointer] += right_value
                        break
                    forward_pointer += 1
                #Remove pair and replace with zero
                snail[pointer] = 0
                del snail[pointer+1:pointer+4]
                #Reset the pointer
                ps(snail)
                pointer = -1
                level = 0
        elif c == "]":
            level -= 1
        else:
            #print(snail)
            if c > 9:
                v = snail[pointer]
                snail = snail[:pointer] + ["[", v//2, v-v//2, "]"] + snail[pointer+1:]
                #Reset the pointer
                ps(snail)
                pointer = -1
                level = 0
    return snail

def add(snail_0, snail_1):
    snail = ["["] + snail_0 + snail_1 + ["]"]
    ps(snail)
    snail = reduce(snail)
    return snail

def ps(snail):
    s = [str(x) for x in snail]
    print("".join(s))

#print(lines[0])
snail_0 = convert("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
snail_1 = convert("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
snail = add(snail_0, snail_1)
ps(snail)
"""