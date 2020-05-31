import random


t = [random.randint(1, 1000) for _ in range(5)]


def main():
    data = [[0, 0], [0, 0]]
    for i in t:
        temp = i
        data[0][0] = temp if temp != data[0][0] and temp > data[0][0] and temp % 19 == 0 and temp % 2 == 0 else data[0][0]
        data[0][1] = temp if temp == data[0][0] and temp > data[0][1] and temp % 19 == 0 and temp % 2 == 0 else data[0][1]
        data[0][1] = temp if temp > data[0][1] and temp % 19 != 0 and temp % 2 == 0 else data[0][1]
        data[1][0] = temp if temp != data[1][0] and temp > data[1][0] and temp % 19 == 0 and temp % 2 != 0 else data[1][0]
        data[1][1] = temp if temp == data[1][0] and temp > data[1][1] and temp % 19 == 0 and temp % 2 != 0 else data[1][1]
        data[1][1] = temp if temp > data[1][1] and temp % 19 != 0 and temp % 2 != 0 else data[1][1]
    data = [[sum(data[0]), data[0][0], data[0][1]], [sum(data[1]), data[1][0], data[1][1]]]
    data.sort()
    print(*data[-1][1:])


main()
