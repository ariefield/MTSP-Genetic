#%%
from consts import locations
from helpers import function1, function2, fast_non_dominated_sort

import itertools
import sys
import math
import time

# houses: house locations in lat/lon
# m: number of salesmen
# n: number of cities (including depot)
def brute_force(houses, m):
    print(
        f"---------------------------- {m} salesmen, and {len(houses)} houses (m = {3}, n = {len(houses)}) ----------------------------"
    )
    a = list(range(1, len(houses)))

    breakpoint_sets = generate_breakpoints(a, m - 1)
    print(f"breakpoints: {breakpoint_sets}")

    paths = itertools.permutations(a)
    print(f"# of permutations: {math.factorial(len(houses)-1)}")

    solutions = []
    function1_values = []
    function2_values = []
    start = time.time()
    for path in paths:
        path = list(path)
        for bp_set in breakpoint_sets:
            gene = path + bp_set
            solutions.append(gene)
            function1_values.append((function1(gene, m), gene))
            function2_values.append((function2(gene, m), gene))

    end = time.time()
    print(f"Main loop took {end-start} seconds")

    return (function1_values, function2_values)


def generate_breakpoints(indices, x):
    a = [indices] * x
    all_breakpoints_tuples = itertools.product(*a)
    all_breakpoints = []

    for bp in all_breakpoints_tuples:
        bp = list(bp)
        bp.sort()
        all_breakpoints.append(bp)
    all_breakpoints.sort()
    all_breakpoints = list(k for k, _ in itertools.groupby(all_breakpoints))

    breakpoints = validate_breakpoints(all_breakpoints, len(indices))
    return breakpoints


def validate_breakpoints(all_breakpoints, n):
    breakpoints = []

    for bp_set in all_breakpoints:
        valid = True

        if len(set(bp_set)) != len(bp_set):
            valid = False

        for x in bp_set:
            if x < 2 or x > n - 2:
                valid = False
                break
            for y in bp_set:
                if x == y:
                    continue
                if abs(x - y) < 2:
                    valid = False
                    break

        if valid:
            breakpoints.append(bp_set)

    return breakpoints


# Run multiple
for n in range(4, 15):
    for m in range(1, 5):
        if m * 2 + 1 > n:
            break
        houses = locations[:n]
        f1, f2 = brute_force(houses, m)
        f1.sort()
        f2.sort()
        print(
            f"Best function1 - {f1[0][1]} f1: {f1[0][0]}  f2: {function2(f1[0][1], m)}"
        )
        print(
            f"Best function2 - {f2[0][1]} f1: {function1(f2[0][1], m)} f2: {f2[0][0]}"
        )
        print(f"Top 5 function 1 - {list(f1[x][1] for x in range(5))}")
        print(f"Top 5 function 2 - {list(f2[x][1] for x in range(5))}")
        print(
            f"Worst function1 - {f1[-1][1]} f1: {f1[-1][0]}  f2: {function2(f1[-1][1], m)}"
        )
        print(
            f"Worst function2 - {f2[-1][1]} f1: {function1(f2[-1][1], m)} f2: {f2[-1][0]}"
        )
        print(
            "------------------------------------------------------------------------------------------------"
        )
        print()
        print()
