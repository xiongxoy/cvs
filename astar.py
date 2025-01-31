#!/usr/bin/python
# Copyright (c) 2010 Brandon Sterne
# Licensed under the MIT license.
# http://brandon.sternefamily.net/files/mit-license.txt
# Python A-Star (A*) Implementation

import sys
import heapq
import copy

class Node:
    def __init__(self, contents, cost, hcost=0):
        self.contents = contents  # representation of the game board
        self.cost = cost          # cost to get to this node
        self.hcost = hcost        # estimated heuristic cost to goal
        self.parent = None        # link to parent node in tree
    def setParent(self, parent):
        self.parent = parent
    # return a list of child nodes according to the set of legal moves
    def getChildNodes(self, moves):
        children = []
        board = self.contents
        for cell in board.keys():
            if board[cell] != None:  # there is a piece that can be moved
                for move in moves[cell]:  # examine legal moves for piece
                    if board[move] == None:  # position is available
                        temp = board.copy()
                        # place the piece in its new position
                        temp[cell] = board[move]
                        temp[move] = board[cell]
                        # create node containing the new configuration
                        child = Node(temp, self.cost+1)
                        child.hcost = distance(child)
                        children.append(child)
        return children
    # evaluate if this node meets the goal criteria
    def isGoal(self):
        if (self.contents[1] == "black") and \
           (self.contents[6] == "black") and \
           (self.contents[5] == "white") and \
           (self.contents[7] == "white"):
            return True
        else:
            return False
    # return a minified, static copy of the board representation so we
    # can keep track of visited nodes (dictionaries require static keys)
    def staticCast(self):
        # return a tuple only containing filled cells
        return tuple([(cell, self.contents[cell]) for cell in
                      self.contents.keys() if self.contents[cell] is not None])

# comparison function for keeping our priority queue in order
# keep less costly nodes toward the front of the queue (explore first)
def compare(a,b):
    if (a.cost+a.hcost) < (b.cost+b.hcost): return -1
    elif (a.cost+a.hcost) == (b.cost+b.hcost): return 0
    else: return 1

# return a list of nodes from the start position to the goal position
def getPath(goal, start):
    current = copy.copy(goal)
    path = []
    # start at the goal and follow the parent chain to the beginning
    path.append(goal)
    while current.contents != start.contents:
        up = current.parent
        path.append(up)
        current = up
    # reverse the list to give the start-to-goal ordering
    path.reverse()
    return path

# print a representation of a game board
def showDiagram(board):
    for i in range(1, 11):
        # line breaks
        if i in [2, 6, 9]: print "\n"
        if board[i] != None:
            print board[i][0],
        else: print "_",
    print "\n"

# dist[i] is the minimum distance to a correct position for a piece of color
# (black, white).  E.g., dist[5][1] is 0 because a white piece in square 5
# is already correctly positioned.
dist = {1: (0, 1), 2: (3, 4), 3: (6, 7), 4: (1, 2), 5: (2, 0),
        6: (0, 3), 7: (1, 0), 8: (4, 5), 9: (5, 6), 10: (2, 3)}

# Heuristic function to estimate how far from the solution a given node is.
# In this problem, we always know the minimum distance from one square to
# via knight's moves.  Uses dist (above) to lookup distances and sum them.
def distance(node):
    distance = 0
    for cell in [c for c in node.contents.keys()
                 if node.contents[c] is not None]:
        if node.contents[cell] == "black":
            distance += dist[cell][0]
        else:
            distance += dist[cell][1]
    return distance

# driver function for the A-Star tree search
# takes a starting board configuration and a dictionary of legal moves
def aStarSearch(board, moves):
    # priority queue to store nodes
    pq = []
    heapq.heapify(pq)

    #dictionary to store previously visited nodes
    visited = {}

    # put the initial node on the queue
    start = Node(board, 0)
    heapq.heappush(pq, start)

    while (len(pq) > 0):
        node = heapq.heappop(pq)
        visNode = node.staticCast()
        if visNode not in visited:
            if node.isGoal():
                return "We've got a winner.", node
            else:
                children = node.getChildNodes(moves)
                for child in children:
                    child.setParent(node)
                    heapq.heappush(pq, child)
                    visited[visNode] = True
                    pq.sort(compare)  # keep less costly nodes at the front
    # entire tree searched, no goal state found
    return "No solution.", None

def printHelp():
    print "-p\tPath: reconstruct full path to goal"
    sys.exit()
     
def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        printHelp()

    # dictionary to store board state
    # cells contain one of ["black", "white", None]
    board = {}
    for i in range(1, 11, 1): board[i] = None
    board[1] = "white"
    board[6] = "white"
    board[5] = "black"
    board[7] = "black"

    # dictionary defines valid operators (legal moves)
    moves = { 1: [4, 7],
              2: [8, 10],
              3: [9],
              4: [1, 6, 10],
              5: [7],
              6: [4],
              7: [1, 5],
              8: [2, 9],
              9: [8, 3],
              10: [2, 4] }

    ans, goal = aStarSearch(board, moves)
    print ans

    # reconstruct path
    if "-p" in sys.argv:
        if ans == "We've got a winner.":
            start = Node(board, 0)
            path = getPath(goal, start)
            i = 0
            for node in path:
                print "step ", i, ":"
                showDiagram(node.contents)
                i += 1
        
if __name__ == "__main__":
    main()
