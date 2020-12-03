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