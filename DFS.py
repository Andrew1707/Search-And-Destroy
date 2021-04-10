import MapGeneration as MapGen


class Node:
    def __init__(self, coords, parent=None, child=set()):
        self.coords = coords
        self.parent = parent
        self.child = child


# limited area
def isValid(grid, curr, start, end):
    low = min([start[0], end[0]])
    high = max([start[0], end[0]])
    left = min([start[1], end[1]])
    right = max([start[1], end[1]])
    x = curr[0]
    y = curr[1]
    if x > high or x < low or y > right or y < left:  # is it out of bounds?
        return False
    return True


# finds the shortest path with highest sum(probs) to traverse
# if you want to get to point b, why travel over deep caves when you can travel
# over flat and search on the way

# DFS execution starting at (sx,sy) reaching (gx,gy), returns goal node if success, returns None if not
def DFS(grid, start, end):
    # gridlength = len(grid)
    # sx = start[0]
    # sy = start[1]
    # gx = end[0]
    # gy = end[1]
    startNode = Node(start)
    # stack = []
    # stack.append(startNode)
    visited = {start}
    curr = {startNode}

    while True:
        next_move = set()

        for x in curr:
            # print(x.coords)
            if x.coords == end:
                return startNode
            if isValid(grid, (x.coords[0] + 1, x.coords[1]), start, end):
                if (x.coords[0] + 1, x.coords[1]) not in visited:
                    empty = set()
                    new = Node((x.coords[0] + 1, x.coords[1]), x, empty)
                    next_move.add(new)
                    x.child = {new} | x.child
            if isValid(grid, (x.coords[0] - 1, x.coords[1]), start, end):
                if (x.coords[0] - 1, x.coords[1]) not in visited:
                    empty = set()
                    new = Node((x.coords[0] - 1, x.coords[1]), x, empty)
                    next_move.add(new)
                    x.child = {new} | x.child
            if isValid(grid, (x.coords[0], x.coords[1] + 1), start, end):
                if (x.coords[0], x.coords[1] + 1) not in visited:
                    empty = set()
                    new = Node((x.coords[0], x.coords[1] + 1), x, empty)
                    next_move.add(new)
                    x.child = {new} | x.child
            if isValid(grid, (x.coords[0], x.coords[1] - 1), start, end):
                if (x.coords[0], x.coords[1] - 1) not in visited:
                    empty = set()
                    new = Node((x.coords[0], x.coords[1] - 1), x, empty)
                    next_move.add(new)
                    x.child = {new} | x.child
        for v in curr:
            visited.add(v.coords)
        # print("visited", visited)
        curr = next_move
    # return startNode


# turns the non binary tree created by DFS into
def get_paths(startNode, path_list=[]):
    # print("start", startNode.coords, path_list)
    if len(startNode.child) == 0:
        curr = startNode
        path = []
        while curr.parent:
            path.insert(0, curr.coords)
            curr = curr.parent
        path.insert(0, curr.coords)
        # print(path)
        path_list.append(path)
        return path_list

    for child in startNode.child:
        # print("child", child.coords)
        path_list = get_paths(child, path_list)
    return path_list


# picks the path with the highest sum utility to traverse
def best_path(grid, probs, start, end):
    tree = DFS(grid, start, end)
    empty_list = []
    path_list = get_paths(tree, empty_list)

    best_utility = 0
    best_path = []
    for path in path_list:
        utility = 0
        for coord in path:
            x = coord[0]
            y = coord[1]
            utility += probs[x][y].utility
        if utility > best_utility:
            best_path = path
            best_utility = utility
    return best_path


# start = (4, 1)
# end = (5, 2)
# terrains = {0.1: "flat", 0.3: "hilly", 0.7: "forested", 0.9: "grid of caverns"}
# grid = MapGen.makeMap(10, terrains)
# tree = DFS(grid, start, end)
# path = get_paths(tree)
# for x in path:
#     print(x)
#     print()


# a = Node((0, 0))
# b = Node((1, 1), a)
# c = Node((2, 2), b)
# d = Node((3, 3), b)
# e = Node((4, 4), b)
# f = Node((5, 5), a)
# a.child = {b, f}
# b.child = {c, d}
# b.child.add(e)
# path_list = get_paths(a)
# # print(path_list)
# for x in path_list:
#     print(x)
#     print()
