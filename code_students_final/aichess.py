#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""
import queue

import chess
import numpy as np
import sys

from itertools import permutations
from queue import PriorityQueue


class Aichess():

    """
    A class to represent the game of chess.

    ...

     Attributes:
    -----------
    chess : Chess
        Represents the current state of the chess game.
    listNextStates : list
        A list to store the next possible states in the game.
    listVisitedStates : list
        A list to store visited states during search.
    pathToTarget : list
        A list to store the path to the target state.
    currentStateW : list
        Represents the current state of the white pieces.
    depthMax : int
        The maximum depth to search in the game tree.
    checkMate : bool
        A boolean indicating whether the game is in a checkmate state.
    dictVisitedStates : dict
        A dictionary to keep track of visited states and their depths.
    dictPath : dict
        A dictionary to reconstruct the path during search.

    Methods:
    --------
    getCurrentState() -> list
        Returns the current state for the whites.

    getListNextStatesW(myState) -> list
        Retrieves a list of possible next states for the white pieces.

    isSameState(a, b) -> bool
        Checks whether two states are the same.

    isVisited(mystate) -> bool
        Checks if a state has been visited.

    isCheckMate(mystate) -> bool
        Checks if a state represents a checkmate.

    DepthFirstSearch(currentState, depth) -> bool
        Depth-first search algorithm.

    worthExploring(state, depth) -> bool
        Checks if a state is worth exploring during search using the optimised DFS algorithm.

    DepthFirstSearchOptimized(currentState, depth) -> bool
        Optimized depth-first search algorithm.

    reconstructPath(state, depth) -> None
        Reconstructs the path to the target state. Updates pathToTarget attribute.

    canviarEstat(start, to) -> None
        Moves a piece from one state to another.

    movePieces(start, depthStart, to, depthTo) -> None
        Moves all pieces between states.

    BreadthFirstSearch(currentState, depth) -> None
        Breadth-first search algorithm.

    h(state) -> int
        Calculates a heuristic value for a state using Manhattan distance.

    AStarSearch(currentState) 
        A* search algorithm -> To be implemented by you

    translate(s) -> tuple
        Translates traditional chess coordinates to list indices.

    """

    def __init__(self, TA, myinit=True):

        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        self.listNextStates = []
        self.listVisitedStates = []
        self.pathToTarget = []
        self.currentStateW = self.chess.boardSim.currentStateW
        self.depthMax = 8
        self.checkMate = False

        # Prepare a dictionary to control the visited state and at which
        # depth they were found
        self.dictVisitedStates = {}
        # Dictionary to reconstruct the BFS path
        self.dictPath = {}


    def getCurrentState(self):
        # Changed name from myCurrentStateW as if was a non-existent attribute
        return self.currentStateW

    def getListNextStatesW(self, myState):

        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    def isSameState(self, a, b):

        isSameState1 = True
        # a and b are lists
        for k in range(len(a)):

            if a[k] not in b:
                isSameState1 = False

        isSameState2 = True
        # a and b are lists
        for k in range(len(b)):

            if b[k] not in a:
                isSameState2 = False

        isSameState = isSameState1 and isSameState2
        return isSameState

    def isVisited(self, mystate):

        if (len(self.listVisitedStates) > 0):
            perm_state = list(permutations(mystate))

            isVisited = False
            for j in range(len(perm_state)):

                for k in range(len(self.listVisitedStates)):

                    if self.isSameState(list(perm_state[j]), self.listVisitedStates[k]):
                        isVisited = True

            return isVisited
        else:
            return False


    def isCheckMate(self, mystate):

        # list of possible check mate states
        listCheckMateStates = [[[0,0,2],[2,4,6]],[[0,1,2],[2,4,6]],[[0,2,2],[2,4,6]],[[0,6,2],[2,4,6]],[[0,7,2],[2,4,6]]]

        # Check all state permuations and if they coincide with a list of CheckMates
        for permState in list(permutations(mystate)):
            if list(permState) in listCheckMateStates:
                return True

        return False

    def DepthFirstSearch(self, currentState, depth):

        # We visited the node, therefore we add it to the list
        # In DF, when we add a node to the list of visited, and when we have
        # visited all noes, we eliminate it from the list of visited ones
        self.listVisitedStates.append(currentState)

        # is it checkmate?
        if self.isCheckMate(currentState):
            self.pathToTarget.append(currentState)
            return True

        if depth + 1 <= self.depthMax:
            for son in self.getListNextStatesW(currentState):
                if not self.isVisited(son):
                    # in the state son, the first piece is the one just moved
                    # We check the position of currentState
                    # matched by the piece moved
                    if son[0][2] == currentState[0][2]:
                        fitxaMoguda = 0
                    else:
                        fitxaMoguda = 1

                    # we move the piece to the new position
                    self.chess.moveSim(currentState[fitxaMoguda],son[0])
                    # We call again the method with the son, 
                    # increasing depth
                    if self.DepthFirstSearch(son,depth+1):
                        #If the method returns True, this means that there has
                        # been a checkmate
                        # We add the state to the list pathToTarget
                        self.pathToTarget.insert(0,currentState)
                        return True
                    # we reset the board to the previous state
                    self.chess.moveSim(son[0],currentState[fitxaMoguda])

        # We eliminate the node from the list of visited nodes
        # since we explored all successors
        self.listVisitedStates.remove(currentState)

    def worthExploring(self, state, depth):

        # First of all, we check that the depth is bigger than depthMax
        if depth > self.depthMax: return False
        visited = False
        # check if the state has been visited
        for perm in list(permutations(state)):
            permStr = str(perm)
            if permStr in list(self.dictVisitedStates.keys()):
                visited = True
                # If there state has been visited at a epth bigger than 
                # the current one, we are interestted in visiting it again
                if depth < self.dictVisitedStates[perm]:
                    # We update the depth associated to the state
                    self.dictVisitedStates[permStr] = depth
                    return True
        # Whenever not visited, we add it to the dictionary 
        # at the current depth
        if not visited:
            permStr = str(state)
            self.dictVisitedStates[permStr] = depth
            return True

    def DepthFirstSearchOptimized(self, currentState, depth):
        # is it checkmate?
        if self.isCheckMate(currentState):
            self.pathToTarget.append(currentState)
            return True

        for son in self.getListNextStatesW(currentState):
            if self.worthExploring(son,depth+1):

                # in state 'son', the first piece is the one just moved
                # we check which position of currentstate matche
                # the piece just moved
                if son[0][2] == currentState[0][2]:
                    fitxaMoguda = 0
                else:
                    fitxaMoguda = 1

                # we move the piece to the novel position
                self.chess.moveSim(currentState[fitxaMoguda], son[0])
                # we call the method with the son again, increasing depth
                if self.DepthFirstSearchOptimized(son, depth + 1):
                    # If the method returns true, this means there was a checkmate
                    # we add the state to the list pathToTarget
                    self.pathToTarget.insert(0, currentState)
                    return True
                # we return the board to its previous state
                self.chess.moveSim(son[0], currentState[fitxaMoguda])

    def reconstructPath(self, state, depth):
        # When we found the solution, we obtain the path followed to get to this        
        for i in range(depth):
            self.pathToTarget.insert(0,state)
            #Per cada node, mirem quin és el seu pare
            key = self.reorder_dict_key(state[0], state[1])
            state = self.dictVisitedStates[key][2]

        self.pathToTarget.insert(0,state)

    def canviarEstat(self, start, to):
        # We check which piece has been moved from one state to the next
        if start[0] == to[0]:
            fitxaMogudaStart=1
            fitxaMogudaTo = 1
        elif start[0] == to[1]:
            fitxaMogudaStart = 1
            fitxaMogudaTo = 0
        elif start[1] == to[0]:
            fitxaMogudaStart = 0
            fitxaMogudaTo = 1
        else:
            fitxaMogudaStart = 0
            fitxaMogudaTo = 0
        # move the piece changed
        self.chess.moveSim(start[fitxaMogudaStart], to[fitxaMogudaTo])

    def movePieces(self, start, depthStart, to, depthTo):

        # To move from one state to the next for BFS we will need to find
        # the state in common, and then move until the node 'to'
        moveList = []
        # We want that the depths are equal to find a common ancestor
        nodeTo = to
        nodeStart = start
        # if the depth of the node To is larger than that of start, 
        # we pick the ancesters of the node until being at the same
        # depth
        while(depthTo > depthStart):
            moveList.insert(0,to)
            nodeTo = self.dictPath[str(nodeTo)][0]
            depthTo-=1
        # Analogous to the previous case, but we trace back the ancestors
        #until the node 'start'
        while(depthStart > depthTo):
            ancestreStart = self.dictPath[str(nodeStart)][0]
            # We move the piece the the parerent state of nodeStart
            self.canviarEstat(nodeStart, ancestreStart)
            nodeStart = ancestreStart
            depthStart -= 1

        moveList.insert(0,nodeTo)
        # We seek for common node
        while nodeStart != nodeTo:
            ancestreStart = self.dictPath[str(nodeStart)][0]
            # Move the piece the the parerent state of nodeStart
            self.canviarEstat(nodeStart,ancestreStart)
            # pick the parent of nodeTo
            nodeTo = self.dictPath[str(nodeTo)][0]
            # store in the list
            moveList.insert(0,nodeTo)
            nodeStart = ancestreStart
        # Move the pieces from the node in common
        # until the node 'to'
        for i in range(len(moveList)):
            if i < len(moveList) - 1:
                self.canviarEstat(moveList[i],moveList[i+1])


    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """
        BFSQueue = queue.Queue()
        # The node root has no parent, thus we add None, and -1, which would be the depth of the 'parent node'
        self.dictPath[str(currentState)] = (None, -1)
        depthCurrentState = 0
        BFSQueue.put(currentState)
        self.listVisitedStates.append(currentState)
        # iterate until there is no more candidate nodes
        while BFSQueue.qsize() > 0:
            # Find the optimal configuration
            node = BFSQueue.get()
            depthNode = self.dictPath[str(node)][1] + 1
            if depthNode > self.depthMax:
                break
            # If it not the root node, we move the pieces from the previous to the current state
            if depthNode > 0:
                self.movePieces(currentState, depthCurrentState, node, depthNode)

            if self.isCheckMate(node):
                # Si és checkmate, construïm el camí que hem trobat més òptim
                self.reconstructPath(node, depthNode)
                break

            for son in self.getListNextStatesW(node):
                if not self.isVisited(son):
                    self.listVisitedStates.append(son)
                    BFSQueue.put(son)
                    self.dictPath[str(son)] = (node, depthNode)
            currentState = node
            depthCurrentState = depthNode


    def h(self,state):

        if state[0][2] == 2:
            posicioRei = state[1]
            posicioTorre = state[0]
        else:
            posicioRei = state[0]
            posicioTorre = state[1]
        # With the king we wish to reach configuration (2,4), calculate Manhattan distance
        fila = abs(posicioRei[0] - 2)
        columna = abs(posicioRei[1]-4)
        # Pick the minimum for the row and column, this is when the king has to move in diagonal
        # We calculate the difference between row an colum, to calculate the remaining movements
        # which it shoudl go going straight        
        hRei = min(fila, columna) + abs(fila-columna)
        # with the tower we have 3 different cases
        if posicioTorre[0] == 0 and (posicioTorre[1] < 3 or posicioTorre[1] > 5):
            hTorre = 0
        elif posicioTorre[0] != 0 and posicioTorre[1] >= 3 and posicioTorre[1] <= 5:
            hTorre = 2
        else:
            hTorre = 1
        # In our case, the heuristics is the real cost of movements
        return hRei + hTorre

    def AStarSearch(self, currentState):
        # Priority queue based on heuristic value
        frontera = PriorityQueue()
        frontera.put((self.h(currentState), currentState))

        # Method added below to order key by piece
        dict_key = self.reorder_dict_key(currentState[0], currentState[1])
        # Dict of states saves (in order): (g, h, parent, depth)
        self.dictVisitedStates[dict_key] = (0, self.h(currentState), None, -1)

        # While possible states left to explore
        while not frontera.empty():
            current_node_f, node = frontera.get()
            self.listVisitedStates.append(node)
            # Update current state
            self.canviarEstat(currentState, node)
            currentState = self.getCurrentState()

            current_dict_key = self.reorder_dict_key(node[0], node[1])
            # Depth of state in the data tree
            depth_of_node = self.dictVisitedStates[current_dict_key][3] + 1

            # Find all next states possible
            for child_state in self.getListNextStatesW(node):
                # g + 1 to previous as each movement made has a cost of 1
                g = self.dictVisitedStates[current_dict_key][0] + 1
                h = self.h(child_state)
                f = g + h

                # While it is not a state previously explored, code will continue if state is previously explored
                # but current f value is smaller
                child_dict_key = self.reorder_dict_key(child_state[0], child_state[1])
                if self.isVisited(child_state):
                    # Finds f value of previously saved state to compare
                    old_state_f = self.dictVisitedStates[child_dict_key][0] + self.dictVisitedStates[child_dict_key][1]
                    # If old f is smaller, then we will no longer continue searching this child state
                    if old_state_f <= f:
                        continue

                frontera.put((f, child_state))
                self.dictVisitedStates[child_dict_key] = (g, h, node, depth_of_node)

            # Finds the next possible movement that could be made
            next_node_f = frontera.queue[0][0]
            # If the current position is checkmate AND the next position has a higher or equal heuristic value,
            # then solution has been found
            if self.isCheckMate(node) and (next_node_f >= current_node_f):
                self.reconstructPath(node, depth_of_node)
                # Change made to return depth of solution, printed later on
                # Other change made in reconstructPath method to use dictVisitedStates instead of dictPath
                return depth_of_node

    # Method has been created so that all dictionary keys have the following format: [king, rook]
    def reorder_dict_key(self, piece_1, piece_2):
        if piece_1[2] == 6:
            return f"[{piece_1}, {piece_2}]"
        return f"[{piece_2}, {piece_1}]"

def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """

    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 8:
            print(s[0] + "is not in the range from 1 - 8")
            return None
        if col < 'a' or col > 'h':
            print(s[1] + "is not in the range from a - h")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dict[col])
    except:
        print(s + "is not in the format '[number][letter]'")
        return None






if __name__ == "__main__":

    if len(sys.argv) < 1:
        sys.exit(1)

    # intiialize board
    TA = np.zeros((8, 8))
    # load initial state
    # white pieces
    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][4] = 12

    # initialise bord
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()
    print("printing board")
    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State",currentState,"\n")

    depth = aichess.AStarSearch(currentState)
    print("#A* move sequence...  ", aichess.pathToTarget)
    print("A* End\n")
    print("Depth of Solution:", depth)
    print("A* printing end state")
    aichess.chess.boardSim.print_board()


