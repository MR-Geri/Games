t = [0, 0]
t1 = [0, 0]
for i in range(int(input())):
    temp = int(input())
    if temp % 19 == 0 and temp % 2 == 0 and temp >= t[0]:
        if temp != t[0]:
            t[0] = temp
        else:
            t1[0] = temp
    elif (temp % 19 == 0) and (temp % 2 != 0) and (temp >= t[1]):
        if temp != t[1]:
            t[1] = temp
        else:
            t1[1] = temp
    elif (temp % 19 != 0) and (temp % 2 == 0) and (temp > t1[0]):
        t1[0] = temp
    elif (temp % 19 != 0) and (temp % 2 != 0) and (temp > t1[1]):
        t1[1] = temp
if (t[0] + t1[0]) > (t[1] + t1[1]):
    print(t[0], t1[0])
else:
    print(t[1], t1[1])
