
import numpy as np
with open("day15_input.txt") as file:
    risks = [[int(x) for x in y[:-1]] for y in file]
risks = np.array(risks)
N = risks.shape[0]

def solve(risk_lookup, total_risk):
    to_test = {(0,0):0}

    def add_to_tests(x ,y, risk):
        #Test if position in bounds
        new_risk = risk_lookup(x,y)
        if new_risk is None:
            return
        #Get position and current risk
        pos = (x,y)
        risk += new_risk
        #Don't test position if the total risk is too small
        if total_risk[pos] < risk:
            return
        #If positon alreayd in to_test, only replace the risk if it is lower
        if pos in to_test:
            if risk < to_test[pos]:
                to_test[pos] = risk
            else:
                return
        else:
            to_test[pos] = risk

    while len(to_test) > 0:
        pos = next(iter(to_test))
        risk = to_test[pos]
        #print(pos, risk)
        del to_test[pos]
        if risk < total_risk[pos]:
            total_risk[pos] = risk
            x,y = pos
            add_to_tests(x-1, y, risk)
            add_to_tests(x+1, y, risk)
            add_to_tests(x, y-1, risk)
            add_to_tests(x, y+1, risk)

    return total_risk[-1,-1]


def risk_lookup(x,y):
    if x < 0 or x >= N:
        return None
    if y < 0 or y >= N:
        return None
    return risks[x,y]

total_risk = np.full_like(risks, 10000)
print("part1", solve(risk_lookup, total_risk))


def risk_lookup(x, y):
    if x < 0 or x >= 5*N:
        return None
    if y < 0 or y >= 5*N:
        return None
    return (risks[x%N, y%N] + x//N + y//N - 1)%9 + 1

total_risk = np.full((5*N, 5*N), 5000)
print("part2", solve(risk_lookup, total_risk))