num3 = []
num4 = []
num5 = []

i = 0
while True:
    num3.append(3+(6*i))
    num4.append(4+(8*i))
    num5.append(5+(10*i))



    if i % 1000000 == 0:
        if (set(num3).intersection(set(num4))).intersection(num5):
            break

        print(num5[-1])
        num3.clear()
        num4.clear()
        num5.clear()

    i += 1

total = (set(num3).intersection(set(num4))).intersection(num5)

print(num3)
print(num4)
print(num5)
print(total)

