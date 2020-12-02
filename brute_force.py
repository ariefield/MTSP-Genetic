#%%
from crossover import distanceOfTwoCity
from consts import locations
from main import function1, function2
import itertools
import sys
import time

# locations: city locations in lat/lon
# m: number of salesmen
# n: number of cities
loc = [(1, 2), (3, 4), (2, 3), (1, 4), (1, 5), (2, 4), (1, 1), (3, 3), (5, 5)]

def validate3(cities):
    a = list(range(len(cities)))

    breakpoint_sets = generate2breakpoints(a)
    paths = list(itertools.permutations(a))

    print(len(paths))
    print(len(breakpoint_sets))

    results = {}
    best = (sys.maxsize, None)
    for path in paths:
        path = list(path)
        for bp_set in breakpoint_sets:
            min_val = sys.maxsize
            max_val = 0
            total_distance = 0
            prev = 0
            for bp in bp_set:
                distance = calcDistance(path[prev:bp])
                min_val = min(min_val, distance)
                max_val = max(max_val, distance)
                total_distance += distance
                prev = bp
            # Last iteration
            distance = calcDistance(path[prev:])
            min_val = min(min_val, distance)
            max_val = max(max_val, distance)
            total_distance += distance

            gene = tuple(path + bp_set)
            results[gene] = total_distance

            if total_distance < best[0]:
                best = (total_distance, [gene])
            elif total_distance == best:
                best[1].append(gene)

    return {"results": results, "best": best}


def generate2breakpoints(a):
    all_breakpoints = [[x, y] for x in a for y in a]
    for bp in all_breakpoints:
        bp.sort()
    all_breakpoints.sort()
    all_breakpoints = list(k for k, _ in itertools.groupby(all_breakpoints))

    breakpoints = []

    for bp_set in all_breakpoints:
        valid = True

        if list(set(bp_set)) != bp_set:
            valid = False

        for x in bp_set:
            if x < 2 or x > len(a) - 2:
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


def calcDistance(path):
    total = 0
    firstCityIndex = path[0]
    lastCityIndex = path[-1]
    distanceOfTwoCity()
    for i, city in enumerate(path):
        if i == 0:
        
        else if i == len(path)

    return 10


# def brute_force(locations, m):
#     initial_breakpoints = []
#     for x in range(1, m + 1):
#         initial_breakpoints.append(x * 2)
#     breakpoints = copy.copy(initial_breakpoints)
#     breakpoints.append(1)

#     print(initial_breakpoints)
#     return 1

# def brute_force(locations, m):
#     length = len(locations)
#     breakpoints = []
#     for _ in range(m):
#         breakpoints.append(0)
#     for bp in range(m):
#         for x in range(length):
#             for bp2 in range(m):
#                 # if bp2 == bp:
#                 #     break
#                 for y in range(length):
#                     breakpoints[bp] = x
#                     breakpoints[bp2] = y
#                     print(breakpoints)

#     return 1

validate3(locations)