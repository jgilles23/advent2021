import numpy as np

np.set_printoptions(linewidth=200, threshold=1000)

with open("day21_input.txt") as file:
    p1_pos = int(file.readline().split(" ")[-1][:-1])
    p2_pos = int(file.readline().split(" ")[-1][:-1])
print(p1_pos, p2_pos)

starting_positions = [p1_pos, p2_pos]
positions = [x for x in starting_positions]
scores = [0, 0]
dice_roll = 100
count_rolls = 0
player = 1
while max(scores) < 1000:
    player = (player + 1)%2
    d1 = (dice_roll -1 + 1)%100 + 1
    d2 = (dice_roll -1 + 2)%100 + 1
    d3 = (dice_roll -1 + 3)%100 + 1
    dice_roll = d3
    count_rolls += 3
    positions[player] = (positions[player] + d1 + d2 + d3 - 1)%10 + 1
    scores[player] += positions[player]

print("part1", min(scores)*count_rolls)

state = np.full((2, 11, 21), 0) #2 players, 11 positions (but no one can be on 0), 21 scores
state[0, p1_pos, 0] = 1
state[1, p2_pos, 0] = 1
win_count = [0, 0]
factors = [1, 1]

#while np.sum(state) > 0:
player = 1
i = 0
while np.sum(state) > 0:
    other_player = player
    player = (player + 1)%2
    #Move the pawns
    for roll in range(3):
        new_state = np.full((11,21), 0)
        for pos in range(11):
            for score in range(21):
                v = state[player, pos, score]
                if v > 0:
                    new_state[(pos + 1 - 1)%10 + 1, score] += v
                    new_state[(pos + 2 - 1)%10 + 1, score] += v
                    new_state[(pos + 3 - 1)%10 + 1, score] += v
        state[player, :, :] = new_state
    #Add to the score
    factors[other_player] = factors[other_player]*27
    new_state = np.full((11, 21), 0)
    wins_this_round = 0
    for pos in range(11):
        for score in range(21):
            v = state[player, pos, score]
            if score + pos >= 21:
                wins_this_round += v
                win_count[player] += v*factors[player]
            else:
                new_state[pos, score + pos] = v
    factors[other_player] = factors[other_player]/np.sum(state[player])*np.sum(new_state)
    state[player, :, :] = new_state
    print()
    print("########################################################################")
    print("round", i, ", player", player, ", factors", factors)
    print(state[player, :, :])
    i += 1

print(win_count)
print("part2", int(max(win_count)))
        

