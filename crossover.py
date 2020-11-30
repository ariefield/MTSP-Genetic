import random
import numpy as np
from enum import Enum
from consts import locations

Direction = Enum("Direction", "forward backward")

# Public
def child1(A, B, m):
    A_path, A_breakpoints = splitGene(A, m)
    B_path, B_breakpoints = splitGene(B, m)
    child_path = crossover(A_path, B_path, Direction.forward)
    child_breakpoints = A_breakpoints if random.randrange(2) else B_breakpoints

    # Debugging
    # print(f"child_path: {child_path}")
    # print(f"a_path: {A_path}    a_breakpoints: {A_breakpoints}")
    # print(f"b_path: {B_path}    b_breakpoints: {B_breakpoints}")
    # print(f"child_breakpoints: {child_breakpoints}")

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


# Private
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


def latterCity(gene, k):
    i = (gene.index(k) + 1) % len(gene)
    return gene[i]


def formerCity(gene, k):
    i = gene.index(k) - 1
    return gene[i]


def distanceOfTwoCity(l1, l2):
    city1 = locations[l1]
    city2 = locations[l2]
    rad_conv = 2 * np.pi / 360
    Distance = 6378.8 * np.arccos(
        (np.sin(city1[1] * rad_conv) * (np.sin(city2[1] * rad_conv)))
        + np.cos(city1[1] * rad_conv)
        * np.cos(city2[1] * rad_conv)
        * np.cos((city2[0] * rad_conv) - (city1[0] * rad_conv))
    )
    return Distance


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
