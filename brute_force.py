#%%
from consts import locations
from crossover import decode, distanceOfTwoCity, splitGene

# from main import function1
import itertools
import sys
import math
import time

# houses: house locations in lat/lon
# m: number of salesmen
# n: number of cities
def brute_force(houses, m):
    a = list(range(1, len(houses)))

    breakpoint_sets = generate_breakpoints(a, m - 1)
    print(f"breakpoints: {breakpoint_sets}")

    paths = itertools.permutations(a)
    print(f"# of permutations: {math.factorial(len(houses))}")

    results = {}
    best = (sys.maxsize, None)
    start = time.time()
    for i, path in enumerate(paths):
        path = list(path)
        for bp_set in breakpoint_sets:
            gene = path + bp_set
            distance = function1(gene, m)
            # results[tuple(gene)] = distance

            if distance <= best[0]:
                best = (distance, tuple(gene))
    end = time.time()
    print(
        f"\nTook {end-start} seconds for {m} salesmen, {len(breakpoint_sets)} breakpoints, and {len(houses)} houses"
    )

    return {"results": results, "best": best}


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


def function1(x, m):
    decoded = decode(*splitGene(x, m))
    decoded.append(0)

    totalDistance = 0.0
    previousLocation = 0

    # We don't need to prepend 0 because previousLocation starts at 0
    for location in decoded:
        totalDistance += distanceOfTwoCity(location, previousLocation)
        previousLocation = location
    return totalDistance


n = 8
m = 3
houses = locations[:n]
print(brute_force(houses, m))
