import random
from enum import Enum

Direction = Enum("Direction", "forward backward")


def crossover(PA, PB, MARK):
    length = len(PA)
    l = random.randrange(1, length)
    k = PA[l]
    RESULT = [k]

    while length > 1:
        if MARK == Direction.forward:
            x = latterCity(PA, k)
            y = latterCity(PB, k)
        elif MARK == Direction.backward:
            x = formerCity(PA, k)
            y = formerCity(PB, k)

        PA.remove(k)
        PB.remove(k)
        dx = distanceOfTwoCity(k, x)
        dy = distanceOfTwoCity(k, y)

        if dx < dy:
            k = x
        else:
            k = y

        RESULT.append(k)
        length = len(PA)

    return RESULT


# Wrapping
def latterCity(gene, k):
    i = (gene.index(k) + 1) % len(gene)
    return gene[i]


def formerCity(gene, k):
    i = gene.index(k) - 1
    return gene[i]


def distanceOfTwoCity(city1, city2):
    return random.randrange(1, 10)


def child1(A, B, m):
    A_path, A_breakpoints = splitGene(A, m)
    print(f"a_path: {A_path}    a_breakpoints: {A_breakpoints}")

    B_path, B_breakpoints = splitGene(B, m)
    print(f"b_path: {B_path}    b_breakpoints: {B_breakpoints}")

    child_path = crossover(A_path, B_path, Direction.forward)
    print(f"child_path: {child_path}")
    # child_path = crossover(A_path, B_path, Direction.backward)

    child_breakpoints = A_breakpoints if random.randrange(2) else B_breakpoints
    print(f"child_breakpoints: {child_breakpoints}")

    child_path.extend(child_breakpoints)
    return child_path


def child2(A, B, m):
    A_path, A_breakpoints = splitGene(A, m)
    B_path, B_breakpoints = splitGene(B, m)

    Ad = decode(A_path, A_breakpoints)
    Bd = decode(B_path, B_breakpoints)
    Ad.insert(0, 0)
    Bd.insert(0, 0)

    res_crossover = crossover(Ad, Bd, Direction.forward)
    res_rational = rationalize(res_crossover)
    res_encoded = encode(res_rational)

    return res_encoded


def splitGene(gene, m):
    path = gene[: -(m - 1)]
    breakpoints = gene[len(gene) - (m - 1) :]
    return (path, breakpoints)


def decode(path, breakpoints):
    for x in breakpoints:
        path.insert(x, 0)
    return path


def encode(A):
    x = A.index(0)
    A = A[x + 1 :] + A[:x]
    breakpoints = []

    for i, e in enumerate(A):
        if e == 0:
            A.pop(i)
            breakpoints.append(i)

    A.extend(breakpoints)
    return A


# [1, 0, 3, 7, 0, 6, 8, 4, 0, 2, 9, 5]
# [1, 3, 7, 6, 8, 0, 4, 2, 9, 5, 0, 0]
def rationalize(A):
    i = 0
    while i < len(A):
        x = A[i]
        if x == 0 and not isValid(A, i):
            j = (i + 1) % len(A)
            while j != i:
                if wouldBeValid(A, j):
                    if j > i:
                        A.pop(i)
                        i -= 1
                        A.insert(j - 1, 0)
                    else:
                        A.pop(i)
                        A.insert(j, 0)
                    break
                else:
                    j = (j + 1) % len(A)
        i += 1

    return A


def isValid(A, i):
    if i + 2 >= len(A):
        return False

    if A[i + 1] == 0 or A[i + 2] == 0:
        return False

    if i == 0:
        return True

    if A[max(i - 1, 0)] == 0 or A[max(i - 2, 0)] == 0:
        return False

    return True


def wouldBeValid(A, i):
    if i + 1 >= len(A):
        return False

    if A[i] == 0 or A[i + 1] == 0:
        return False

    if i == 0:
        return True

    if A[max(i - 1, 0)] == 0 or A[max(i - 2, 0)] == 0:
        return False

    return True


PA = [1, 2, 3, 4]
PB = [4, 3, 2, 1]
# res = crossover(PA, PB, Direction.forward)
# print(res)

A = [5, 2, 1, 3, 7, 6, 8, 4, 9, 3, 7]
B = [3, 8, 1, 5, 4, 7, 2, 9, 6, 2, 6]
# print(child1(A, B, 2))

# x, y = splitGene(A, 2)
# print(x)
# print(y)

# print(rationalize([1, 0, 3, 7, 6, 8, 0, 0, 4, 2, 9, 5]))
# print(encode([1, 0, 3, 7, 6, 8, 0, 4, 2, 0, 9, 5]))

print(child2(A, B, 3))