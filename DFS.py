class Node:
    def __init__(self, start, parent=None, child=None, movesTaken=0, movesLeft=0.0):
        self.x = start[0]
        self.y = start[1]
        self.parent = parent
        self.child = {child}
        self.movesTaken = movesTaken
        self.movesLeft = movesLeft


# limited area
def isValid(grid, curr, start, end):
    low = min([start[0], end[0]])
    high = max([start[0], end[0]])
    left = min([start[1], end[1]])
    right = min([start[1], end[1]])
    x = curr[0]
    y = curr[1]
    if x >= high or x < low or y >= right or y < left:  # is it out of bounds?
        return False
    return True


# # Returns array of up/down/left/right in priority search order
# def directionPrio(start, end):

#     sx = start[0]
#     sy = start[1]
#     gx = end[0]
#     gy = end[1]
#     deltaX = gx - sx
#     deltaY = gy - sy
#     if deltaX > 0:  # right
#         if deltaY > 0:
#             if abs(deltaX) > abs(deltaY):
#                 return ["r", "d", "u", "l"]
#             else:
#                 return ["d", "r", "l", "u"]
#         else:
#             if abs(deltaX) > abs(deltaY):
#                 return ["r", "u", "d", "l"]
#             else:
#                 return ["u", "r", "l", "d"]
#     else:  # left (and if deltaX = 0)
#         if deltaY > 0:
#             if abs(deltaX) > abs(deltaY):
#                 return ["l", "d", "u", "r"]
#             else:
#                 return ["d", "l", "r", "u"]
#         else:
#             if abs(deltaX) > abs(deltaY):
#                 return ["l", "u", "d", "r"]
#             else:
#                 return ["u", "l", "r", "d"]


# DFS execution starting at (sx,sy) reaching (gx,gy), returns goal node if success, returns None if not
def DFS(grid, start, end):
    # gridlength = len(grid)
    # sx = start[0]
    # sy = start[1]
    # gx = end[0]
    # gy = end[1]
    startNode = Node(start, None, None)
    stack = []
    stack.append(startNode)
    visited = {start}
    curr = {startNode}

    while start not in curr:
        next_move = set()
        for x in curr:
            if isValid(grid, (x[0] + 1, x[1]), start, end):
                if (x[0] + 1, x[1]) not in visited:
                    new = Node((x[0] + 1, x[1]), x, None)
                    next_move.add((x[0] + 1, x[1]))
                    x.child.add(new)
            if isValid(grid, (x[0] - 1, x[1]), start, end):
                if (x[0] - 1, x[1]) not in visited:
                    new = Node((x[0] - 1, x[1]), x, None)
                    next_move.add((x[0] - 1, x[1]))
                    x.child.add(new)
            if isValid(grid, (x[0], x[1] + 1), start, end):
                if (x[0], x[1] + 1) not in visited:
                    new = Node((x[0], x[1] + 1), x, None)
                    next_move.add((x[0], x[1] + 1))
                    x.child.add(new)
            if isValid(grid, (x[0], x[1] - 1), start, end):
                if (x[0], x[1] - 1) not in visited:
                    new = Node((x[0], x[1] - 1), x, None)
                    next_move.add((x[0], x[1] - 1))
                    x.child.add(new)
        curr = next_move
    return startNode

    # Recognize which direction we want to travel farthest and look there first
    # prioQ = directionPrio(start, end)

    # while len(stack) != 0:  # While stack isn't empty
    #     node = stack.pop()
    #     if node.x == gx and node.y == gy:
    #         return node
    #     for i in reversed(
    #         prioQ
    #     ):  # Append new nodes to stack in (reverse) order, lower prio appended first
    #         if i == "r":
    #             if isValid(grid, (node.x + 1, node.y), start, end):
    #                 stack.append(Node(node.x + 1, node.y, node, None))
    #                 grid[node.x + 1][node.y].visit = "yes"
    #         elif i == "l":
    #             if isValid(grid, (node.x - 1, node.y), start, end):
    #                 stack.append(Node(node.x - 1, node.y, node, None))
    #                 grid[node.x - 1][node.y].visit = "yes"
    #         elif i == "u":
    #             if isValid(grid, (node.x, node.y - 1), start, end):
    #                 stack.append(Node(node.x, node.y - 1, node, None))
    #                 grid[node.x][node.y - 1].visit = "yes"
    #         else:
    #             if isValid(grid, (node.x, node.y + 1), start, end):
    #                 stack.append(Node(node.x, node.y + 1, node, None))
    #                 grid[node.x][node.y + 1].visit = "yes"
    # return None
