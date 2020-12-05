#%%
# Importing required modules
from genetic import child1, child2, decode, splitGene, distanceOfTwoCity
from helpers import function1, function2, fast_non_dominated_sort

import math
import random
import matplotlib.pyplot as plt
import time


def mutation1(parent, m):
    # mutation_prob = random.random()
    # if mutation_prob <0.5:
    n = len(parent)
    j = random.randint(1, n - (m - 1) - 1)  # m-1 split points
    i = random.randint(0, j - 1)
    # print(i,j)
    # part 1 (0,i) part 2 (i,j) part 3(j,n) reverse part 2 only
    result = parent[0:i] + parent[i:j][::-1] + parent[j : n - (m - 1)]

    randomBreakpoints = [
        i + x for i, x in enumerate(sorted(random.sample(range(2, n - 3), m - 1)))
    ]
    # print(parent[0:i],parent[i:j][::-1],parent[j:n-(m-1)])
    return result + randomBreakpoints


# return parent


def mutation2(parent, m):
    n = len(parent)
    j = random.randint(1, n - (m - 1) - 1)
    i = random.randint(0, j - 1)
    # print(i,j)
    # part 1 (0,i) part 2 (i,j) part 3(j,n) restitch as part 2,1,3
    result = parent[i:j] + parent[0:i] + parent[j : n - (m - 1)]
    splits = random.sample(range(1, n - m), m - 1)
    # print(splits)
    return result + splits

    # Program Name: NSGA-II.py


# Description: This is a python implementation of Prof. Kalyanmoy Deb's popular NSGA-II algorithm
# Author: Haris Ali Khan
# Supervisor: Prof. Manoj Kumar Tiwari

# Function to find index of list
def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


# Function to sort by values
def sort_by_values(list1, values):
    sorted_list = []
    while len(sorted_list) != len(list1):
        if index_of(min(values), values) in list1:
            sorted_list.append(index_of(min(values), values))
        values[index_of(min(values), values)] = math.inf
    return sorted_list


# Function to calculate crowding distance
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0, len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (
            values1[sorted1[k + 1]] - values2[sorted1[k - 1]]
        ) / (max(values1) - min(values1))
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (
            values1[sorted2[k + 1]] - values2[sorted2[k - 1]]
        ) / (max(values2) - min(values2))
    return distance


# Function to carry out the crossover
def crossover_git(a, b, m):
    r = random.random()
    child = child1(a, b, m)
    if r > 0.5:
        return mutation1(child, m)
    else:
        return mutation2(child, m)


# Generate random chromosome for population
def generateRandom(n, m):
    randomPath = random.sample(range(1, n), n - 1)
    randomBreakpoints = [
        i + x for i, x in enumerate(sorted(random.sample(range(2, n - 3), m - 1)))
    ]

    return randomPath + randomBreakpoints


def main(m, n):
    print(f"------------- m = {m}, n = {n} -------------")
    startTime = time.time()
    pop_size = 20
    max_gen = 921

    # Initialization
    solution = [generateRandom(n, m) for i in range(0, pop_size)]

    gen_no = 0
    while gen_no < max_gen:
        function1_values = [function1(solution[i], m) for i in range(0, pop_size)]
        function2_values = [function2(solution[i], m) for i in range(0, pop_size)]
        non_dominated_sorted_solution = fast_non_dominated_sort(
            function1_values[:], function2_values[:]
        )
        bestSolution = [solution[i] for i in non_dominated_sorted_solution[0]]
        crowding_distance_values = []
        for i in range(0, len(non_dominated_sorted_solution)):
            crowding_distance_values.append(
                crowding_distance(
                    function1_values[:],
                    function2_values[:],
                    non_dominated_sorted_solution[i][:],
                )
            )
        solution2 = solution[:]
        # Generating offsprings
        while len(solution2) != 2 * pop_size:
            a1 = random.randint(0, pop_size - 1)
            b1 = random.randint(0, pop_size - 1)
            solution2.append(crossover_git(solution[a1], solution[b1], m))
        function1_values2 = [function1(solution2[i], m) for i in range(0, 2 * pop_size)]
        function2_values2 = [function2(solution2[i], m) for i in range(0, 2 * pop_size)]
        non_dominated_sorted_solution2 = fast_non_dominated_sort(
            function1_values2[:], function2_values2[:]
        )
        crowding_distance_values2 = []
        for i in range(0, len(non_dominated_sorted_solution2)):
            crowding_distance_values2.append(
                crowding_distance(
                    function1_values2[:],
                    function2_values2[:],
                    non_dominated_sorted_solution2[i][:],
                )
            )
        new_solution = []
        for i in range(0, len(non_dominated_sorted_solution2)):
            non_dominated_sorted_solution2_1 = [
                index_of(
                    non_dominated_sorted_solution2[i][j],
                    non_dominated_sorted_solution2[i],
                )
                for j in range(0, len(non_dominated_sorted_solution2[i]))
            ]
            front22 = sort_by_values(
                non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:]
            )
            front = [
                non_dominated_sorted_solution2[i][front22[j]]
                for j in range(0, len(non_dominated_sorted_solution2[i]))
            ]
            front.reverse()
            for value in front:
                new_solution.append(value)
                if len(new_solution) == pop_size:
                    break
            if len(new_solution) == pop_size:
                break
        solution = [solution2[i] for i in new_solution]
        gen_no = gen_no + 1

    endTime = time.time()

    print(f"The best path(s) for Generation number {gen_no} is:")
    print(bestSolution)

    function1_values = [
        function1(bestSolution[i], m) for i in range(0, len(bestSolution))
    ]
    function2_values = [
        function2(bestSolution[i], m) for i in range(0, len(bestSolution))
    ]

    runtime = endTime - startTime
    print(f"Runtime: {runtime}")

    fileName = "MTSP-Timings.csv"
    file = open(fileName, "a+")
    file.write(
        str(runtime)
        + ","
        + str(n)
        + ","
        + str(m)
        + ","
        + str(bestSolution)
        + ","
        + "\n"
    )  # write data with a newline
    file.close()

    function1_res = [i for i in function1_values]
    function2_res = [j for j in function2_values]

    fileName = "MTSP.csv"
    file = open(fileName, "a+")
    file.write(
        f"n: {n}, m: {m}, runtime: {runtime}, # of solutions: {len(function1_res)}, function1: {function1_res[0]}, function2: {function2_res[0]}, best: {bestSolution}\n"
    )
    file.close()

    print(f"Number of solutions: {len(function1_res)}")
    print(f"function1: {function1_res[0]}")
    print(f"function2: {function2_res[0]}")
    print()

    # Lets plot the final front now
    # fig = plt.figure()
    # plt.xlabel("Function 1", fontsize=15)
    # plt.ylabel("Function 2", fontsize=15)
    # plt.scatter(function1_res, function2_res)
    # fig.savefig("./solutions")
    # # plt.show()


# for n in [9, 10, 11, 20, 30]:
#     for m in range(2, 4):
#         main(m, n)

for n in [60, 100, 120]:
    for m in [2, 5, 10, 15, 20]:
        main(m, n)
