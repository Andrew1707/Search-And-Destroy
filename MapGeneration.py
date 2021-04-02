import random

# chance is the chance of failing a search
class GridUnit:
    def __init__(self, status, chance, coordinates):
        self.status = status  # 0 for no target, 1 for has target
        self.chance = chance  # 0 to 1 value on probability of false negative
        self.coordinates = coordinates  # tuples (x,y)probability
        # self.terrain = terrain  # string of terrain name, idk if we need this


# makes sure the coordinate is within the grid
def isValid(grid, coordinates):
    # is it out of bounds?
    x = coordinates[0]
    y = coordinates[1]
    gridlength = len(grid)
    if x >= gridlength or x < 0 or y >= gridlength or y < 0:
        return False
    return True


# makes and returns a grid search and destroy
# terrains is a dictionary of terrain and false negative probability  (prob:name)
# no terrians with same prob mkay
def makeMap(gridlength, terrains):

    # pick random terrain out of terrain dictionary
    grid = [
        [GridUnit(0, random.choice(list(terrains)), (i, j)) for j in range(gridlength)]
        for i in range(gridlength)
    ]

    # adds target in random location
    x = random.randint(0, len(grid) - 1)
    y = random.randint(0, len(grid) - 1)
    grid[x][y].status = 1
    return grid


# prints grid out of easy to read emojis
def gridPrint(grid):
    gridlength = len(grid)
    for i in range(gridlength):
        print()
        for j in range(gridlength):
            if grid[i][j].chance == 0.1:
                print("⬜", end=" ")
            elif grid[i][j].chance == 0.3:
                print("🟫", end=" ")
            elif grid[i][j].chance == 0.7:
                print("🟩", end=" ")
            elif grid[i][j].chance == 0.9:
                print("⬛", end=" ")
            # unknown chance in case more terrain added idk
            else:
                print("🟥", end=" ")
