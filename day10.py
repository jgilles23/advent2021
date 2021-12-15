with open("day10_input.txt") as file:
    inp = [[y for y in x[:-1]] for x in file]
#print(inp[0])

close_to_open_map = {")":"(", "]":"[", "}":"{", ">":"<"}
open_to_close_map = {value:key for key,value in zip(close_to_open_map, close_to_open_map.values())}
close_to_score = {")":3, "]":57, "}":1197, ">":25137}

incomplete_lines = []
score = 0
for base in inp:
    line = [x for x in base]
    i = 0
    while i < len(line):
        c = line[i]
        if c in [x for x in ")]}>"]:
            #print(line, "i",i)
            prev = line[i-1]
            if close_to_open_map[c] == prev:
                del line[i]
                del line[i-1]
                i -= 2
            else:
                #print("base", "".join(base))
                #print("i", i, "c", c, "prev", prev, "line", line)
                #print("score", close_to_score[c])
                score += close_to_score[c]
                break
        i += 1
    else:
        incomplete_lines.append(base)
print("part1", score)


print("num incomplete_lines",len(incomplete_lines))
open_to_score = {"(":1, "[":2, "{":3, "<":4}

scores = []
for base in incomplete_lines:
    #print("base ", "".join(base))
    line = [x for x in base]
    #print("line", "".join(base))
    i = 0
    while i < len(line):
        c = line[i]
        if c in [x for x in ")]}>"]:
            #print(line, "i",i)
            prev = line[i-1]
            if close_to_open_map[c] == prev:
                del line[i]
                del line[i-1]
                i -= 2
            else:
                raise Exception("Unexpected Character")
        i += 1
    line_score = 0
    for c in line[::-1]:
        line_score = line_score*5 + open_to_score[c]
    #print(line_score)
    scores.append(line_score)
#sort scores
scores.sort()
#print(scores)
print("part2", scores[len(scores)//2])