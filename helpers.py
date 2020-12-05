from genetic import child1, child2, decode, splitGene, distanceOfTwoCity

# First function to optimize. Input is encoded chromasome array and the output is the total distance
def function1(x, m):
    decoded = decode(*splitGene(x, m))
    decoded.append(0)

    totalDistance = 0.0
    previousLocation = 0

    # We don't need to prepend 0 because previousLocation starts at 0
    for location in decoded:
        # print(
        #     f"prev: {previousLocation}  location: {location}   distance: {distanceOfTwoCity(location, previousLocation)}"
        # )
        totalDistance += distanceOfTwoCity(location, previousLocation)
        previousLocation = location

    return totalDistance


# Second function to optimize
def function2(x, m):
    decoded = decode(*splitGene(x, m))
    decoded.append(0)

    # find total distance for every salesman
    salesmanDistances = []
    totalDistance = 0
    prevLocation = 0

    for location in decoded:
        totalDistance += distanceOfTwoCity(location, prevLocation)
        prevLocation = location
        if location == 0:
            salesmanDistances.append(totalDistance)
            totalDistance = 0

    return max(salesmanDistances) - min(salesmanDistances)


# Function to carry out NSGA-II's fast non dominated sort
# We should reverse the greater than signs instead of reversing the list!!!!
def fast_non_dominated_sort(values1, values2):
    S = [[] for i in range(0, len(values1))]
    front = [[]]
    n = [0 for i in range(0, len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(values1)):
            if (
                (values1[p] > values1[q] and values2[p] > values2[q])
                or (values1[p] >= values1[q] and values2[p] > values2[q])
                or (values1[p] > values1[q] and values2[p] >= values2[q])
            ):
                if q not in S[p]:
                    S[p].append(q)
            elif (
                (values1[q] > values1[p] and values2[q] > values2[p])
                or (values1[q] >= values1[p] and values2[q] > values2[p])
                or (values1[q] > values1[p] and values2[q] >= values2[p])
            ):
                n[p] = n[p] + 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while front[i] != []:
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i = i + 1
        front.append(Q)

    del front[len(front) - 1]

    front.reverse()
    return front