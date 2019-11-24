from random import randint


time = []
for ele in range(40):
    start = randint(0, 190)
    stop = start + randint(0, 30)

    time.append((start, stop))

time.sort(key=lambda tup: tup[0])

print(time)

time2 = []
sum = 0
earliest = time[0][0]
latest = time[0][1]

for i in range(1, len(time)):
    curr = time[i]
    # update earliest
    if curr[0] > latest:
        # showing
        time2.append((earliest, latest))
        sum += (latest - earliest)
        earliest = curr[0]
        latest = curr[1]

    elif latest < curr[1]:
        latest = curr[1]

print(time2)

