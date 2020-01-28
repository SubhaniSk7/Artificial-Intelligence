import copy
import queue
import numpy as np
import math

# -------------------------------------------------

children = []
movesLeft = 0


class TicTacToeNode:

    # constructor
    def __init__(self, state=None, name=None, isMax=False, utilityValue=None, childrenList=[]):
        self.name = name
        self.isMax = isMax
        self.utilityValue = utilityValue
        self.state = state
        self.action = None
        self.move = []
        # self.path_cost = 0
        # self.children = None
        # self.childrenList = []
        self.childrenList = childrenList
        self.gameOver = False

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setGameOver(self, gameOver):
        self.gameOver = gameOver

    def getGameOver(self):
        return self.gameOver

    def setMove(self, move):
        self.move = move;

    def getMove(self):
        return self.move

    def setIsMax(self, isMax):
        self.isMax = isMax

    def getIsMax(self):
        return self.isMax

    def setUtilityValue(self, utilityValue):
        self.utilityValue = utilityValue

    def getUtilityValue(self):
        return self.utilityValue

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setAction(self, action):
        self.action = action

    def getAction(self):
        return self.action

    def setChildren(self, children):
        self.children = children

    def getChildren(self):
        return self.children

    def setChildrenList(self, childrenList):
        self.childrenList = childrenList;

    def getChildrenList(self):
        return self.childrenList;

    # -------------------------------------------------


def display(currentState):
    for i in range(0, len(currentState)):
        print(currentState[i])

    # terminalTest(currentState)
    # print('movesLeft:', movesLeft)



def getMAXAvailableState(currentNode):
    node = currentNode
    state = node.getState()

    maxChildren = []

    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if (state[i][j] == 0):
                tempState = copy.deepcopy(state)
                tempState[i][j] = 1
                tempNode = TicTacToeNode(tempState)
                maxChildren.append(tempNode)

    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # for i in maxChildren:
    #     display(i.getState())
    #     print()
    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%')

    return maxChildren


def getMINAvailableState(currentNode):
    node = currentNode
    state = node.getState()

    minChildren = []

    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if (state[i][j] == 0):
                tempState = copy.deepcopy(state)
                tempState[i][j] = 2
                tempNode = TicTacToeNode(tempState)
                minChildren.append(tempNode)

    # print('#######################')
    # for i in minChildren:
    #     display(i.getState())
    #     print()
    # print('#######################')

    return minChildren


def terminalTest(currentState):
    count = 0

    for i in range(0, len(currentState)):
        for j in range(0, len(currentState[i])):
            if (currentState[i][j] == 0):
                count = count + 1
                # print('count:' ,count)

    global movesLeft
    movesLeft = count

    if (movesLeft != 0):
        return True
    else:
        return False


def checkRows(currentState, isMaxPlayer):
    firstRow = (currentState[0][0] == currentState[0][1] and currentState[0][0] == currentState[0][2] and
                currentState[0][1] == currentState[0][2])
    secondRow = (currentState[1][0] == currentState[1][1] and currentState[1][0] == currentState[1][2] and
                 currentState[1][1] == currentState[1][2])
    thirdRow = (currentState[2][0] == currentState[2][1] and currentState[2][0] == currentState[2][2] and
                currentState[2][1] == currentState[2][2])

    status = False
    winner = None

    # if (isMaxPlayer):

    if ((currentState[0][0] == 1 and firstRow) or (currentState[1][0] == 1 and secondRow) or (
            currentState[2][0] == 1 and thirdRow)):
        status = True
        winner = 1
        return status, winner
    # else:
    if ((currentState[0][0] == 2 and firstRow) or (currentState[1][0] == 2 and secondRow) or (
            currentState[2][0] == 2 and thirdRow)):
        status = True
        winner = 2
        return status, winner

    # print('in checkRows:status:', status, ' winner:', winner)
    return status, winner


def checkColumns(currentState, isMaxPlayer):
    firstColumn = (currentState[0][0] == currentState[1][0] and currentState[0][0] == currentState[2][0] and
                   currentState[1][0] == currentState[2][0])
    secondColumn = (currentState[0][1] == currentState[1][1] and currentState[0][1] == currentState[2][1] and
                    currentState[1][1] == currentState[2][1])
    thirdColumn = (currentState[0][2] == currentState[1][2] and currentState[0][2] == currentState[2][2] and
                   currentState[1][2] == currentState[2][2])

    # display(currentState)
    # print('-->', firstColumn, '-->', secondColumn, '-->', thirdColumn)
    status = False
    winner = None
    # if (isMaxPlayer):
    if ((currentState[0][0] == 1 and firstColumn) or (currentState[0][1] == 1 and secondColumn) or (
            currentState[0][2] == 1 and thirdColumn)):
        status = True
        winner = 1
        return status, winner
    # else:
    if ((currentState[0][0] == 2 and firstColumn) or (currentState[0][1] == 2 and secondColumn) or (
            currentState[0][2] == 2 and thirdColumn)):
        status = True
        winner = 2
        # print('if in checkColumns:status:', status, ' winner:', winner)
        return status, winner

    # print('in checkColumns:status:', status, ' winner:', winner)
    return status, winner


def checkLeftToRightDiagonal(currentState, isMaxPlayer):
    leftLine = (currentState[0][0] == currentState[1][1] and currentState[0][0] == currentState[2][2] and
                currentState[1][1] == currentState[2][2])

    status = False
    winner = None
    # if (isMaxPlayer):
    if (currentState[0][0] == 1 and leftLine):
        status = True
        winner = 1
        return status, winner
    # else:
    if (currentState[0][0] == 2 and leftLine):
        status = True
        winner = 2
        return status, winner

    # print('in LeftLine:status:', status, ' winner:', winner)
    return status, winner


def checkRightToLeftDiagonal(currentState, isMaxPlayer):
    rightLine = (currentState[0][2] == currentState[1][1] and currentState[0][2] == currentState[2][0] and
                 currentState[1][1] == currentState[2][0])

    status = False
    winner = None

    # if (isMaxPlayer):
    if (currentState[0][2] == 1 and rightLine):
        status = True
        winner = 1
        return status, winner
    # else:
    if (currentState[0][2] == 2 and rightLine):
        status = True
        winner = 2
        return status, winner

    # print('in RightLine:status:', status, ' winner:', winner)
    return status, winner


def calculateUtility(currentState, isMaxPlayer):
    if (isMaxPlayer):
        rowLine, winner = checkRows(currentState, isMaxPlayer)

        if (rowLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner

        columnLine, winner = checkColumns(currentState, isMaxPlayer)
        if (columnLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner
        leftLine, winner = checkLeftToRightDiagonal(currentState, isMaxPlayer)
        if (leftLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner
        rightLine, winner = checkRightToLeftDiagonal(currentState, isMaxPlayer)
        if (rightLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner
    else:
        NotMaxPlayer = not isMaxPlayer
        rowLine, winner = checkRows(currentState, NotMaxPlayer)

        if (rowLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner

        columnLine, winner = checkColumns(currentState, NotMaxPlayer)
        if (columnLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner
        leftLine, winner = checkLeftToRightDiagonal(currentState, NotMaxPlayer)
        if (leftLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner
        rightLine, winner = checkRightToLeftDiagonal(currentState, NotMaxPlayer)
        if (rightLine):
            if (winner == 1):
                return 1, winner
            else:
                return -1, winner

    return 0, None


def MAX_VALUE(puzzleNode, isMaxPlayer):
    # print('in Max_value')
    node = puzzleNode

    currentState = node.getState()
    if (not terminalTest(currentState)):
        score, winner = calculateUtility(currentState, isMaxPlayer)
        # node.setUtilityValue(score)
        # print('--->in terminal test:', score, ' winner:', winner)

        return node, score

    # if(terminalTest(currentState)):
    #     score,winner=calculateUtility(currentState,isMaxPlayer)
    #     return score

    maxChildren = getMAXAvailableState(node)
    # print('max size:', len(maxChildren))
    bestScore = float('-Inf')

    bestNode = node
    for childNode in maxChildren:
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        # display(childNode.getState())

        isMaxPlayer = False
        if (isGameOver(childNode.getState(), isMaxPlayer)):
            bestScore=1
            return childNode, bestScore

        returnedNode, score = getMax(childNode, isMaxPlayer)

        childNode.setUtilityValue(score)

        # print('in MAX_Value:todisplay', score)
        # display(returnedNode.getState())
        if (score >= bestScore):
            bestScore = score
            bestNode = childNode
        # print('-----------------Max_value for -----------------------')

    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # for childNode in maxChildren:
    #     display(childNode.getState())
    #     print('-->',childNode.getUtilityValue())
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    node = bestNode
    return node, bestScore


def MIN_VALUE(puzzleNode, isMaxPlayer):
    # print('in Min_value')
    node = puzzleNode

    currentState = node.getState()
    if (not terminalTest(currentState)):
        score, winner = calculateUtility(currentState, isMaxPlayer)
        # node.setUtilityValue(score)
        # print('--->in terminal test:', score, ' winner:', winner)
        return node, score

    # if (terminalTest(currentState)):
    #     score, winner = calculateUtility(currentState, isMaxPlayer)
    #     return score

    minChildren = getMINAvailableState(node)


    # print('min size:', len(minChildren))
    bestScore = float('Inf')
    bestNode = node

    for childNode in minChildren:
        # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # display(childNode.getState())
        isMaxPlayer = True

        if (isGameOver(childNode.getState(), isMaxPlayer)):
            bestScore = -1
            return childNode, bestScore

        returnedNode, score = getMax(childNode, isMaxPlayer)

        childNode.setUtilityValue(score)

        # print('in MIN_Value:todisplay', score)
        # display(returnedNode.getState())
        if (score <= bestScore):
            bestScore = score
            bestNode = childNode
        # print('-----------------min_value for -----------------------')

    # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    # for childNode in minChildren:
    #     display(childNode.getState())
    #     print('-->',childNode.getUtilityValue())
    # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    node = bestNode
    return node, bestScore


def getMax(puzzleNode, isMaxPlayer):
    # print('in getMax:', isMaxPlayer, " ", terminalTest(puzzleNode.getState()))
    node = puzzleNode

    if (not terminalTest(node.getState())):
        score, winner = calculateUtility(node.getState(), isMaxPlayer)
        # node.setUtilityValue(score)
        # print('in terminal:', score)
        # print('--->in terminal test:', score, ' winner:', winner)
        # display(node.getState())
        # if (isMaxPlayer):
        #     print('returning to Min_value')
        # else:
        #     print('returning to Max_value')
        # print('----------------------------------')
        return node, score

    if (isMaxPlayer):
        # print('=============================in getMax Max')
        isMaxPlayer = True
        node, bestScore = MAX_VALUE(node, isMaxPlayer)
        # print('max:bestscore:', bestScore)
        # display(node.getState())

        # print('returning')
        return node, bestScore
        print('-----------------------------')

    else:
        # print('=============================in getMax Min')
        isMaxPlayer = False
        node, bestScore = MIN_VALUE(node, isMaxPlayer)

        # print('return MIN:', bestScore)
        # display(node.getState())
        # print('returning')
        return node, bestScore
        # print('-----------------------------')


def isGameOver(currentState, isMaxPlayer):
    # print('isMaxPlayer', isMaxPlayer)
    rowLine, winner = checkRows(currentState, isMaxPlayer)

    if (rowLine):
        # print('in rowLine', winner)
        return True
    columnLine, winner = checkColumns(currentState, isMaxPlayer)
    if (columnLine):
        # print('in columnLine', winner)
        return True
    leftLine, winner = checkLeftToRightDiagonal(currentState, isMaxPlayer)
    if (leftLine):
        # print('in leftLine', winner)
        return True
    rightLine, winner = checkRightToLeftDiagonal(currentState, isMaxPlayer)
    if (rightLine):
        # print('in rightLine', winner)
        return True

    return False


def miniMax(puzzleNode, isMaxPlayer):  # returns
    print('In fillTicTacToe....')
    node = puzzleNode

    while (True):
        if(not terminalTest(node.getState())):
            print('Draw',0)
            break
        if (isMaxPlayer):
            # print(
            #     'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            # print(
            #     'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            # print(
            #     'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            print('---------------your turn---------------')
            i = int(input('enter i:'))
            j = int(input('enter j:'))

            node.getState()[i][j] = 1
            display(node.getState())

            if (isGameOver(node.getState(), isMaxPlayer)):
                print('You Won')
                break

            isMaxPlayer = False

            # print('-----------------------------')

        else:
            # print('=============================')
            print('---------------Computer\'s turn---------------')

            bestNode, bestScore = getMax(node, isMaxPlayer)

            node = bestNode
            # print('in minimax min:', bestScore)

            display(bestNode.getState())

            if (isGameOver(node.getState(), isMaxPlayer)):
                print('Computer Won')
                break
            isMaxPlayer = True
            node = bestNode

            print()
            # print('closing AI Player')
            # print('=============================')


# n = int(input('enter n:'))
n = 3

a = [[0] * n for i in range(n)]

# a = [[2, 0, 1], [0, 1, 0], [0, 0, 0]]
# a = [[2, 0, 1], [0, 1, 0], [0, 0, 2]]
# a = [[2, 0, 1], [0, 1, 0], [2, 0, 1]]
# a = [[0, 0, 1], [0, 1, 0], [0, 0, 2]]

tttNode = TicTacToeNode(a)

print('Initial state:')
for i in range(0, n):
    print(tttNode.getState()[i])

isMax = True
# isMax = False
miniMax(tttNode, isMax)
