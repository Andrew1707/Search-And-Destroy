import MapGeneration as MapGen
import random
import numpy as np


# computes total likelihood of returning a fail in the entire grid
def computeFail(grid, probs):
    total_fail_chance = 0.0
    for i in probs:
        for j in probs:
            total_fail_chance += probs[i][j] * grid[i][j].chance
    return total_fail_chance


# when u check a unit and fail whats its new prob
def update(coordinates, grid, probs):
    x = coordinates[0]
    y = coordinates[1]
    oldProb = probs[x][y].prob
    chance = grid[x][y].chance
    total_fail_chance = computeFail(grid, probs)

    probs[x][y].prob = oldProb * chance / total_fail_chance

    # distribute diff to other values
    difference = probs[x][y].prob - oldProb
    addToAll = difference / ((len(grid) ** 2) - 1)
    for i in range(len(grid)):
        for j in range(len(grid)):
            if not (i == x or j == y):
                probs[i][j] += addToAll
    return probs, difference


# when you want to search a unit, returns if search failed or not
def searching(coordinates, grid):
    x = coordinates[0]
    y = coordinates[1]
    if grid[x][y].status == 1:
        if random.random() >= grid[x][y].chance:
            return True
    return False


# return set of coords that have the easiest chance to find target
def easiest_find():
    pass


# takes set of tuples and returns set of tuples that are closest to agent
# location is a tuple
def nearest_search(location, searchables, grid):
    minimum = len(grid) + len(grid)
    closest_searchables = set()
    for x in searchables:
        manhattan = abs(location[0] - x[0]) + abs(location[1] - x[1])
        if manhattan < minimum:
            minimum = manhattan
            closest_searchables = x
        elif manhattan == minimum:
            closest_searchables = closest_searchables | x
    return closest_searchables


# Basic Agent 1: Iteratively travel to the cell with highest prob of containing target
def fool1(grid):
    # Start at random location
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)

    target_found = False
    number_of_searches = 0
    distance_traveled = 0

    while not target_found:
        # Either search current cell or move up/down/left/right

        # If decide to search current cell
        target_found = searching((x, y), grid)
        number_of_searches += 1

        # If decide to move
        # set new x and y
        # compare adjacent cells for prob of containing target

    return None  # * filler line


# Basic Agent 2: Iteratively travel to the cell with the highest prob of finding target
def fool2(grid):
    # Start at random location
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)

    return None  # * filler line


def play():

    terrains = {0.1: "flat", 0.3: "hilly", 0.7: "forested", 0.9: "maze of caverns"}
    # make 50
    gridlen = 10
    grid = MapGen.makeMap(gridlen, terrains)
    MapGen.gridPrint(grid)

    found = False
    probs = np.full((gridlen, gridlen), (1 / (gridlen ** 2)), dtype=float)

    pass
    while found == False:
        pass


play()