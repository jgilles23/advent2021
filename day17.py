import re
import math

with open("day17_input.txt") as file:
     out = re.split("target area: x=|\.\.|, y=", file.readline()[:-1])
     x_min, x_max, y_min, y_max = [int(i) for i in out[1:]]
print(x_min, x_max, y_min, y_max)

#Step 1, what x values will allow 

def yield_vx():
    vx_initial = 0
    while True:
        vx_initial += 1
        x_final = (vx_initial + 1)/2 * vx_initial
        if x_final >= x_min and x_final <= x_max:
            yield vx_initial
        elif x_final > x_max:
            break
        

i = 0
for x in yield_vx():
    i += 1
    print(x)
    if i == 10:
        break

vxs = [vx for vx in yield_vx()]

#vy = 2
#steps = 9
#y_final = vy*steps - (steps-1)/2 * steps
#print(y_final)

#vy*steps - (steps-1)/2 * steps == (min_y or max_y)
#-1/2*steps**2 + 1/2*steps + vy*steps - y == 0
#steps**2 - (1 + 2*vy)*steps + 2*y == 0
# (1 + 2*vy) +- sqrt((1 + 2vy)**2 - 4*2*y)  /  2

def calc_steps(vy, y):
    steps_plus = ((1+2*vy) + ((1+2*vy)**2 - 4*2*y)**0.5)/2 - 1
    #steps_minus = ((1+2*vy) - ((1+2*vy)**2 - 4*2*y)**0.5)/2 - 1
    return steps_plus#, steps_minus 

def yield_vy():
    vy = -1000
    while True:
        vy += 1
        steps_top = calc_steps(vy, y_max)
        steps_bottom = calc_steps(vy, y_min)
        delta_int = int(steps_bottom) - int(steps_top)
        delta_true = steps_bottom - steps_top
        #print("vy", vy, "top", steps_top, "bottom", steps_bottom, "delta", delta_int)
        if delta_int >= 1:
            yield vy, delta_int
        elif delta_true <= 0.01:
            return
        else:
            pass

def max_height(vy):
    return (vy+1)/2 * vy

i = 0
vys = []
for vy, delta in yield_vy():
    vys.append(vy)
    i += 1
    if i == 400:
        break

print("vxs", vxs)
print("vys", vys)

try:
    vy_max = vy
    print("part1", max_height(vy), vy)
except:
    print("In the except clause")
    vy_max = 50

#Just do this the quick and dirty way
print(x_max, y_min, vy_max)
count = 0
for vx_init in range(1, x_max+1):
    #print(vx)
    for vy_init in range(y_min, vy_max+1):
        vx = vx_init
        vy = vy_init
        #print((vx,vy), "v")
        x, y = 0, 0
        while True:
            x += vx
            y += vy
            #print((vx,vy), (x,y),)
            if x_min<=x and x<=x_max and y_min<=y and y<=y_max:
                count += 1
                #print((vx_init, vy_init), "solved")
                #print("Solved")
                break
            if x>x_max or y<y_min:
                #print("Doesn't work")
                break
            if vx > 0:
                vx -= 1
            vy -= 1
print("part2", count)


