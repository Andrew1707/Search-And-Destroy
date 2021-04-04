import MapGeneration as MapGen
import random
import numpy as np


class probability:
    def __init__(self, prob, coordinates, chance):
        self.prob = prob
        self.coords = coordinates
        self.chance = chance
        self.utility = prob * chance


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


# Finds highest probability(s) in probs grid
def most_likely_container(probs, gridlen):
    highest_probs_set = set()
    highest_probs_set.add((0,0))
    highest_prob = probs[0][0]
    for i in range(gridlen):
        for j in range(gridlen):
            if probs[i][j] > highest_prob:
                highest_probs_set.clear
                highest_probs_set.add((i, j))
            if probs[i][j] == highest_prob:
                highest_probs_set.add((i, j))
    return highest_probs_set


# return set of coords that have the easiest chance to find target
def easiest_find():
    pass


# takes set of tuples and returns set of tuples that are closest to agent
# location is a tuple
def nearest_search(location, searchables, grid):
    minimum = len(grid) + len(grid)
    closest_searchables = set()
    for x in searchables:
        print(f'x: {x}') #!rem
        manhattan = abs(location[0] - x[0]) + abs(location[1] - x[1])
        if manhattan < minimum:
            minimum = manhattan
            closest_searchables = {x}
        elif manhattan == minimum:
            closest_searchables = closest_searchables | {x}
    return closest_searchables


# finds the shortest path with highest sum(probs) to traverse
# if you want to get to point b, why travel over deep caves when you can travel
# over flat and search on the way
def smart_pathing(location, searchables, grid):
    pass


# Basic Agent 1: Iteratively travel to the cell with highest prob of containing target
def fool1(grid, probs):
    # Start at random location
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)

    target_found = False
    number_of_searches = 0
    distance_traveled = 0

    while not target_found:
        # Find highest probability square to move to
        highest_probs_set = most_likely_container(probs, gridlen)
        print(highest_probs_set) #!rem
        highest_probs_set = nearest_search((x,y), highest_probs_set, grid)
        new_loc = highest_probs_set.pop

        print(f'new_loc: {new_loc}')
        
        # "Teleport" to new_loc and add distance covered to distance_traveled
        deltaX = abs(new_loc[0] - x)
        deltaY = abs(new_loc[1] - y)
        distance_traveled = distance_traveled + deltaX + deltaY

        # Search new_loc cell
        target_found = searching(new_loc, grid)
        number_of_searches += 1

        # Update x and y to current location
        x = new_loc[0]
        y = new_loc[1]

    return number_of_searches, distance_traveled


# Basic Agent 2: Iteratively travel to the cell with the highest prob of finding target
def fool2(grid):
    # Start at random location
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)

    return None  # * filler line


def play():

    terrains = {0.1: "flat", 0.3: "hilly", 0.7: "forested", 0.9: "grid of caverns"}
    # make 50
    gridlen = 10
    grid = MapGen.makeMap(gridlen, terrains)
    MapGen.gridPrint(grid)

    found = False
    probs = np.full((gridlen, gridlen), (1 / (gridlen ** 2)), dtype=float)

    num_searches, dist_traveled = fool1(grid, probs)
    print(f'num_searches: {num_searches}')
    print(f'dist_traveled: {dist_traveled}')
    pass
    while found == False:
        pass


play()
