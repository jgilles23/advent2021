with open("day6_input.txt") as file:
    for line in file:
        remaining = [int(x) for x in line[:-1].split(",")]

week = [0]*7
for r in remaining:
    week[r] += 1

def age(week, time):
    today = 0
    seven = 0
    eight = 0
    for i in range(time):
        six = seven
        seven = eight
        eight = week[today]
        week[today] += six
        today = (today + 1)%7
        #print("day",i+1,"week", week, "six", six, "seven", seven,"eight", eight,"sum",sum(week)+seven+eight,"tomorrow",today)
    return week, seven, eight, today

res = age(week, 80)
print(res)
print("part1", sum(res[0])+res[1]+res[2])

week = [0]*7
for r in remaining:
    week[r] += 1
res = age(week,256)
print("part2", sum(res[0])+res[1]+res[2])
