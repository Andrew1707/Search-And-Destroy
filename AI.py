import MapGeneration as MapGen
import random

# in case we want more variables
# prob is prob the target is in unit
class ProbUnit:
    def __init__(self, prob, coordinates):
        self.prob = prob  # 0 to 1 value on probability of false negative
        self.coordinates = coordinates  # tuples (x,y)probability


def basicProbs(gridlength):
    probs = [
        [ProbUnit((1 / (gridlength ** 2)), (i, j)) for j in range(gridlength)]
        for i in range(gridlength)
    ]
    return probs


# when u check a unit and fail whats its new prob
# benton u check teh math pls in progress
def update(coordinates, grid, probs):
    x = coordinates[0]
    y = coordinates[1]
    oldProb = probs[x][y].prob
    chance = grid[x][y].chance
    probs[x][y].prob = oldProb * (1 - chance)
    difference = probs[x][y].prob - oldProb
    # distribute diff to other values
    return probs


# when you want to search a unit, returns if search failed or not
def searching(coordinates, grid):
    x = coordinates[0]
    y = coordinates[1]
    if grid[x][y].status == 1:
        # benton or should it be less than or equal to
        if random.random() > grid[x][y].chance:
            return True
    return False


def play():

    terrains = {0.1: "flat", 0.3: "hilly", 0.7: "forested", 0.9: "maze of caverns"}
    # make 50
    grid = MapGen.makeMap(10, terrains)
    MapGen.gridPrint(grid)

    found = False
    probs = basicProbs(len(grid))

    pass
    while found == False:
        pass


play()
