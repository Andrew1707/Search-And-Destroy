import MapGeneration as MapGen
import random
import DFS as DFS


class probability:
    def __init__(self, prob, coordinates, chance):
        self.prob = prob
        self.coords = coordinates
        self.chance = chance

    @property
    def utility(self):
        return self.prob * (1 - self.chance)


# Probability object matrix setter
def probSet(grid):
    gridlen = len(grid)
    init_prob = float(1 / (gridlen ** 2))
    probs = list()
    for i in range(gridlen):
        temp = list()
        for j in range(gridlen):
            temp.append(probability(init_prob, (i, j), grid[i][j].chance))
        probs.append(temp)
    return probs


# Debugging support method: prints probs matrix
def probsPrint(probs):
    print("probs:")
    for i in range(len(probs)):
        for j in range(len(probs)):
            print(probs[i][j].prob, end=" ")
        print("\n")


# computes total likelihood of returning a fail in the entire grid
def computeFail(probs, coords):
    total_fail_chance = 0.0
    gridlen = len(probs)
    x = coords[0]
    y = coords[1]
    for i in range(gridlen):
        for j in range(gridlen):
            if i == x and j == y:
                total_fail_chance += probs[1][j].prob * probs[i][j].chance
            else:
                total_fail_chance += probs[i][j].prob
    return total_fail_chance


# when u check a unit and fail whats its new prob
def update(coordinates, grid, probs):
    x = coordinates[0]
    y = coordinates[1]
    total_fail_chance = computeFail(probs, (x, y))

    for i in range(len(grid)):
        for j in range(len(grid)):
            if i != x or j != y:
                probs[i][j].prob = probs[i][j].prob / total_fail_chance
            else:
                probs[i][j].prob = probs[i][j].prob * probs[i][j].chance / total_fail_chance
    return probs


# when you want to search a unit, returns if search failed or not
def searching(coordinates, grid):
    x = coordinates[0]
    y = coordinates[1]
    if grid[x][y].status == 1:
        if random.random() >= grid[x][y].chance:
            return True
    return False


# Finds highest probability(s) in probs grid
def most_likely_container(probs):
    gridlen = len(probs)
    highest_probs_set = set()
    highest_prob = 0
    for i in range(gridlen):
        for j in range(gridlen):
            if probs[i][j].prob > highest_prob:
                highest_probs_set = {(i, j)}
                highest_prob = probs[i][j].prob
            elif probs[i][j].prob == highest_prob:
                highest_probs_set.add((i, j))
    return highest_probs_set


# return set of coords that have the easiest chance to find target
def easiest_find(probs):
    gridlen = len(probs)
    highest_utility_set = set()
    highest_util = 0
    for i in range(gridlen):
        for j in range(gridlen):
            if probs[i][j].utility > highest_util:
                highest_utility_set = {(i, j)}
                highest_util = probs[i][j].utility
            elif probs[i][j].utility == highest_util:
                highest_utility_set.add((i, j))
    return highest_utility_set


# takes set of tuples and returns set of tuples that are closest to agent
# location is a tuple
def nearest_search(location, searchables, grid):
    minimum = len(grid) + len(grid)
    closest_searchables = set()
    for x in searchables:
        manhattan = abs(location[0] - x[0]) + abs(location[1] - x[1])
        if manhattan < minimum:
            minimum = manhattan
            closest_searchables = {x}
        elif manhattan == minimum:
            closest_searchables = closest_searchables | {x}
    return closest_searchables


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
        highest_probs_set = most_likely_container(probs)
        highest_probs_set = nearest_search((x, y), highest_probs_set, grid)
        new_loc = highest_probs_set.pop()

        # "Teleport" to new_loc and add distance covered to distance_traveled
        deltaX = abs(new_loc[0] - x)
        deltaY = abs(new_loc[1] - y)
        distance_traveled = distance_traveled + deltaX + deltaY

        # Search new_loc cell
        target_found = searching(new_loc, grid)
        probs = update(new_loc, grid, probs)
        number_of_searches += 1

        # Update x and y to current location
        x = new_loc[0]
        y = new_loc[1]

    return number_of_searches, distance_traveled


# Basic Agent 2: Iteratively travel to the cell with the highest prob of finding target
def fool2(grid, probs):
    # Start at random location
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)

    target_found = False
    number_of_searches = 0
    distance_traveled = 0

    while not target_found:
        # Find easiest square to search for target
        highest_util_set = easiest_find(probs)
        highest_util_set = nearest_search((x, y), highest_util_set, grid)
        new_loc = highest_util_set.pop()

        # "Teleport" to new_loc and add distance covered to distance_traveled
        deltaX = abs(new_loc[0] - x)
        deltaY = abs(new_loc[1] - y)
        distance_traveled = distance_traveled + deltaX + deltaY

        # Search new_loc cell
        target_found = searching(new_loc, grid)
        probs = update(new_loc, grid, probs)
        number_of_searches += 1

        # Update x and y to current location
        x = new_loc[0]
        y = new_loc[1]

    return number_of_searches, distance_traveled


def smart(grid, probs):
    # Start at random location
    gridlen = len(grid)
    x = random.randint(0, gridlen - 1)
    y = random.randint(0, gridlen - 1)

    target_found = False
    number_of_searches = 0
    distance_traveled = 0

    # print(f'start_loc: ({x},{y})') #!rem
    while not target_found:
        # Find easiest square to search for target
        highest_probs_set = easiest_find(probs)
        # print(highest_probs_set) #!rem
        highest_probs_set = nearest_search((x, y), highest_probs_set, grid)
        new_loc = highest_probs_set.pop()

        deltaX = abs(new_loc[0] - x)
        deltaY = abs(new_loc[1] - y)
        distance_to = deltaX + deltaY

        destination_utility = probs[new_loc[0]][new_loc[1]].utility
        worth_checking_util = 0.5 * destination_utility

        # if short enough to calculate the best path
        if distance_to <= 10:
            # print(f'new_loc: {new_loc}') #!rem
            best_path = DFS.best_path(grid, probs, (x, y), new_loc)

            for coord in best_path:
                distance_traveled += 1
                if probs[coord[0]][coord[1]].utility >= worth_checking_util:
                    target_found = searching(coord, grid)
                    probs = update(coord, grid, probs)
                    number_of_searches += 1
                    if target_found:
                        return number_of_searches, distance_traveled
        # make a random path`
        else:
            xinc = 0
            yinc = 0
            if new_loc[0] > x:
                xinc = 1
            else:
                xinc = -1
            if new_loc[1] > y:
                yinc = 1
            else:
                yinc = -1

            while x != new_loc[0] and y != new_loc[1]:
                if x == new_loc[0]:
                    y += yinc
                elif y == new_loc[1]:
                    x += xinc
                else:
                    if random.random() >= 0.5:
                        y += yinc
                    else:
                        x += xinc
                distance_traveled += 1
                if probs[x][y].utility >= worth_checking_util:
                    target_found = searching((x, y), grid)
                    probs = update((x, y), grid, probs)
                    number_of_searches += 1
                    if target_found:
                        return number_of_searches, distance_traveled

        # Update x and y to current location
        x = new_loc[0]
        y = new_loc[1]

    return number_of_searches, distance_traveled


def agentComparator():
    terrains = {0.1: "flat", 0.3: "hilly", 0.7: "forested", 0.9: "grid of caverns"}
    gridlen = 50
    num_maps = 10
    map_repeats = 10
    avg_fool1_search, avg_fool2_search, avg_smart_search = 0, 0, 0
    avg_fool1_dist, avg_fool2_dist, avg_smart_dist = 0, 0, 0

    # Generating maps
    for n in range(num_maps):
        print(n)  #!
        grid = MapGen.makeMap(gridlen, terrains)

        # Repeated agent runs on each map
        for i in range(map_repeats):
            print(f"i: {i}")  #!
            # Set up probability matrix for each agent
            probs = probSet(grid)
            num_searches1, dist_traveled1 = fool1(grid, probs)
            probs = probSet(grid)
            num_searches2, dist_traveled2 = fool2(grid, probs)
            probs = probSet(grid)
            num_searches_smart, dist_traveled_smart = smart(grid, probs)

            avg_fool1_search += num_searches1
            avg_fool1_dist += dist_traveled1
            avg_fool2_search += num_searches2
            avg_fool2_dist += dist_traveled2
            avg_smart_search += num_searches_smart
            avg_smart_dist += dist_traveled_smart

    # Average out the map searches/distances for each agent
    avg_fool1_search /= num_maps * map_repeats
    avg_fool1_dist /= num_maps * map_repeats
    avg_fool2_search /= num_maps * map_repeats
    avg_fool2_dist /= num_maps * map_repeats
    avg_smart_search /= num_maps * map_repeats
    avg_smart_dist /= num_maps * map_repeats

    print(f"fool1:  search={avg_fool1_search}\tdist={avg_fool1_dist}")
    print(f"fool2:  search={avg_fool2_search}\tdist={avg_fool2_dist}")
    print(f"smart:  search={avg_smart_search}\tdist={avg_smart_dist}")


def play():

    terrains = {0.1: "flat", 0.3: "hilly", 0.7: "forested", 0.9: "grid of caverns"}
    # make 50
    gridlen = 10
    grid = MapGen.makeMap(gridlen, terrains)
    MapGen.gridPrint(grid)

    probs = probSet(grid)

    # num_searches, dist_traveled = fool2(grid, probs) #!rem
    # print(f'num_searches: {num_searches}') #!rem
    # print(f'dist_traveled: {dist_traveled}') #!rem
    # num_searches, dist_traveled = fool2(grid, probs) #!rem
    # print(f'num_searches: {num_searches}') #!rem
    # print(f'dist_traveled: {dist_traveled}') #!rem
    num_searches, dist_traveled = smart(grid, probs)  #!rem
    print(f"num_searches: {num_searches}")  #!rem
    print(f"dist_traveled: {dist_traveled}")  #!rem


# start = (6, 7)
# end = (6, 7)
# terrains = {0.1: "flat", 0.3: "hilly", 0.7: "forested", 0.9: "grid of caverns"}
# grid = MapGen.makeMap(10, terrains)
# gridlen = 10
# init_prob = float(1 / (gridlen ** 2))
# probs = list()
# for i in range(gridlen):
#     temp = list()
#     for j in range(gridlen):
#         temp.append(probability(init_prob, (i, j), grid[i][j].chance))
#     probs.append(temp)
# best_path = DFS.best_path(grid, probs, start, end)
# print(best_path)
# play()

agentComparator()