import random
import copy


def get_number(i, j):
    return i * 4 + j + 1


def get_index(num):
    num -= 1
    x, y = num // 4, num % 4
    return x, y


def insert24(mas, x, y):
    if random.random() <= 0.75:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


def zero_in_mas(mas):
    for row in mas:
        if 0 in row:
            return True
    return False


def get_empty(mas):
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                num = get_number(i, j)
                empty.append(num)
    return empty


def move_left(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j + 1)
                mas[i].append(0)
    return mas, delta, not origin == mas


def move_right(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if mas[i][j] == mas[i][j - 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j - 1)
                mas[i].insert(0, 0)
    return mas, delta, not origin == mas


def move_up(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for j in range(4):
        column = []
        for i in range(4):
            if mas[i][j] != 0:
                column.append(mas[i][j])
        while len(column) != 4:
            column.append(0)
        for i in range(3):
            if column[i] == column[i + 1] and column[i] != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i + 1)
                column.append(0)
        for i in range(4):
            mas[i][j] = column[i]
    return mas, delta, not origin == mas


def move_down(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for j in range(4):
        column = []
        for i in range(4):
            if mas[i][j] != 0:
                column.append(mas[i][j])
        while len(column) != 4:
            column.insert(0, 0)
        for i in range(3, 0, -1):
            if column[i] == column[i - 1] and column[i] != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i - 1)
                column.insert(0, 0)
        for i in range(4):
            mas[i][j] = column[i]
    return mas, delta, not origin == mas


def can_move(mas):
    for i in range(3):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] or mas[i][j] == mas[i + 1][j]:
                return True
    for i in range(1, 4):
        for j in range(1, 4):
            if mas[i][j] == mas[i - 1][j] or mas[i][j] == mas[i][j - 1]:
                return True
    return False
