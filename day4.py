inp = []
with open("day4_input.txt") as file:
    for line in file:
        inp.append(line[:-1])

calls = [int(x) for x in inp[0].split(",")]
#print(calls)
boards = []
for start_line in range(2,len(inp),6):
    board = []
    for line_num in range(start_line, start_line+5):
        line = inp[line_num]
        for char_num in range(0,len(line),3):
            board.append(int(line[char_num:char_num+3]))
    boards.append(board)
boards_save = [[y for y in x] for x in boards]

#part1
#
scores = [[0 for _ in range(10)] for _ in boards]

def apply(pick, boards, scores, ret_winner=True):
    for board, score, board_num in zip(boards,scores,range(len(boards))):
        if pick in board:
            loc = board.index(pick)
            row = loc//5
            col = loc%5
            score[row] += 1
            score[col + 5] += 1
            board[loc] = None #remove numbers that have been found
            if 5 in score and ret_winner:
                #print(score)
                return board, pick, board_num
    return None

for pick in calls:
    #print(pick)
    ret = apply(pick, boards, scores)
    if ret:
        #print(ret)
        board, pick, board_num = ret
        break

print(board,"pick",pick,"board_num",board_num)
print("part1", sum([x for x in board if x])*pick)

boards = boards_save
scores = [[0 for _ in range(10)] for _ in boards]
for pick in calls:
    #print(len(boards), len(scores))
    apply(pick, boards, scores, ret_winner=False)
    removals = []
    for i, score in enumerate(scores):
        if 5 in score:
            removals.append(i)
    for i in removals[::-1]:
        most_recent_removal = boards[i]
        del scores[i]
        del boards[i]
    if len(boards) <= 0:
        break

print(len(boards))
board = most_recent_removal
print(board, pick)
print("part2", sum([x for x in board if x])*pick)