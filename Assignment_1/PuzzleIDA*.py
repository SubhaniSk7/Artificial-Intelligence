import copy
import heapq
import math
import operator
import queue;
import time

# -------------------------------------------------
import apt_pkg


class PuzzleNode:

    # constructor
    def __init__(self, state=None, parent=None, total_cost=None):
        # self.total_cost = self.path_cost + self.heuristic_cost;
        self.state = state;
        self.parent = None;
        self.action = None;
        self.path_cost = 0;  # path cost to reach node
        self.children = None;
        self.heuristic_cost = 0;  # manhattan distance
        self.total_cost = self.path_cost + self.heuristic_cost;

    def setState(self, state):
        self.state = state;

    def getState(self):
        return self.state;

    def setParent(self, parent):
        self.parent = parent;

    def getParent(self):
        return self.parent;

    def setAction(self, action):
        self.action = action;

    def getAction(self):
        return self.action;

    def setPathCost(self, path_cost):
        self.path_cost = path_cost;

    def getPathCost(self):
        return self.path_cost;

    def setChildren(self, children):
        self.children = children;

    def getChildren(self):
        return self.children;

    def setHeuristicCost(self, heuristic_cost):
        self.heuristic_cost = heuristic_cost;

    def getHeuristicCost(self):
        return self.heuristic_cost;

    def setTotalCost(self, total_cost):
        self.total_cost = total_cost;

    def getTotalCost(self):
        return self.total_cost;

    def __lt__(self, other):
        selfPriority = self.total_cost;
        otherPriority = other.total_cost;
        return selfPriority < otherPriority;

    # -------------------------------------------------


def GoalTest(currentState):
    # print('----------------------')
    isGoal = False;
    # count = 1;
    count = 1;
    for i in range(0, len(currentState)):
        # print(currentState[i]);
        for j in range(0, len(currentState)):

            if (i == len(currentState) - 1 and j == len(currentState) - 1):
                continue;
            if (currentState[i][j] == count):
                count += 1;
                isGoal = True;
            else:
                isGoal = False;
                return isGoal;

    return isGoal;


def puzzleAStar(puzzleNode):
    print('In PuzzleA*....');
    node = puzzleNode;
    node.path_cost = 0;

    if (GoalTest(node.getState())):
        print('**********Goal Found.**********');
        return node.getState();

    # frontier = queue.PriorityQueue();
    # frontier = queue.Queue();

    frontier = [];
    frontier.append(node);
    # explored = set();

    explored = [];

    for ele in frontier:
        print(ele.getState());
        print('==');

    while (True):

        listObj = [];

        for x in range(0, len(frontier)):
            for y in range(0, len(frontier)):
                if (frontier[y].getTotalCost() > frontier[x].getTotalCost()):
                    temp1, temp2 = frontier[y], frontier[x];
                    frontier[y] = temp2;
                    frontier[x] = temp1;

        # for obj in frontier:
        #     listObj.append(obj.getState());
        #     print(obj.getTotalCost());
        #
        # print('first listObj:', listObj);

        failure = None;
        if (not frontier):
            print('Goal Not Found..');
            return failure;

        node = frontier[0];
        del frontier[0];

        if (node.getTotalCost() > bound):
            bound+=limit;
            pass

        print('----------------current Node----------------');
        print(node.getState(), '--path_cost:', node.getPathCost(), ',heuristic:', node.getHeuristicCost(), ',total:',
              node.getTotalCost());

        # time.sleep(1);

        if (node.getState() in explored):
            continue;

        # explored.update(node.getState());
        if (node.getState() not in explored):
            explored.append(node.getState());

        print('explored:', explored);

        blankIndexI, blankIndexJ = getBlankIndex(node.getState());

        # print('blankIndex I:', blankIndexI, ' blankIndex J:', blankIndexJ);

        moveLeft(node, blankIndexI, blankIndexJ);
        moveUp(node, blankIndexI, blankIndexJ);
        moveRight(node, blankIndexI, blankIndexJ);
        moveDown(node, blankIndexI, blankIndexJ);

        # print('child Size:', len(children));

        print('----------------children----------------');
        for ele in children:
            print('-->', ele.getState(), '-->', ele.getParent().getState());
            print('--path_cost:', ele.getPathCost(), ',heuristic:', ele.getHeuristicCost(), ',total:',
                  ele.getTotalCost());
        # time.sleep(1);
        print('------------------');

        # listObj = [];
        # for obj in frontier:
        #     listObj.append(obj.getState());
        #
        # print('after listObj:', listObj);

        for ele in children:
            if ((ele.getState() not in listObj) or (ele.getState() not in explored)):
                if (GoalTest(ele.getState())):
                    print('**********Goal Found.**********');
                    print(ele.getState());
                    # return ele.getState();
                    return ele;
                # frontier.put(ele.getTotalCost(), ele);
                frontier.append(ele);

        children.clear();


def moveUp(currentNode, blankIndexI, blankIndexJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (blankIndexI != 0):
        temp = tempNode.getState()[blankIndexI][blankIndexJ];
        tempNode.getState()[blankIndexI][blankIndexJ] = tempNode.getState()[blankIndexI - 1][blankIndexJ];
        tempNode.getState()[blankIndexI - 1][blankIndexJ] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);
        tempNode.setHeuristicCost(heuristic(tempNode.getState()));
        tempNode.setTotalCost(int(tempNode.getPathCost() + tempNode.getHeuristicCost()));

        # print('in Up: path-', tempNode.getPathCost(), ',heuristic:', tempNode.getHeuristicCost(), ',total:',
        #       tempNode.getTotalCost());
        # tempNode.setParent(currentNode.getState());
        tempNode.setParent(currentNode);
        # children.put(tempNode);
        children.append(tempNode);


def moveDown(currentNode, blankIndexI, blankIndexJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (blankIndexI != len(currentNode.getState()) - 1):
        temp = tempNode.getState()[blankIndexI][blankIndexJ];
        tempNode.getState()[blankIndexI][blankIndexJ] = tempNode.getState()[blankIndexI + 1][blankIndexJ];
        tempNode.getState()[blankIndexI + 1][blankIndexJ] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);
        tempNode.setHeuristicCost(heuristic(tempNode.getState()));
        tempNode.setTotalCost(int(tempNode.getPathCost() + tempNode.getHeuristicCost()));

        # print('in Down: path-', tempNode.getPathCost(), ',heuristic:', tempNode.getHeuristicCost(), ',total:',
        # tempNode.getTotalCost());

        # tempNode.setParent(currentNode.getState());
        tempNode.setParent(currentNode);
        # children.put(tempNode);
        children.append(tempNode);


def moveLeft(currentNode, blankIndexI, blankIndexJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (blankIndexJ != 0):
        temp = tempNode.getState()[blankIndexI][blankIndexJ];
        tempNode.getState()[blankIndexI][blankIndexJ] = tempNode.getState()[blankIndexI][blankIndexJ - 1];
        tempNode.getState()[blankIndexI][blankIndexJ - 1] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);
        tempNode.setHeuristicCost(heuristic(tempNode.getState()));
        tempNode.setTotalCost(int(tempNode.getPathCost() + tempNode.getHeuristicCost()));

        # print('in Left: path-', tempNode.getPathCost(), ',heuristic:', tempNode.getHeuristicCost(), ',total:',
        #       tempNode.getTotalCost());

        # tempNode.setParent(currentNode.getState());
        tempNode.setParent(currentNode);
        # children.put(tempNode);
        children.append(tempNode);


def moveRight(currentNode, blankIndexI, blankIndexJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (blankIndexJ != len(currentNode.getState()) - 1):
        temp = tempNode.getState()[blankIndexI][blankIndexJ];
        tempNode.getState()[blankIndexI][blankIndexJ] = tempNode.getState()[blankIndexI][blankIndexJ + 1];
        tempNode.getState()[blankIndexI][blankIndexJ + 1] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);
        tempNode.setHeuristicCost(heuristic(tempNode.getState()));
        tempNode.setTotalCost(int(tempNode.getPathCost() + tempNode.getHeuristicCost()));

        # print('in Right: path-', tempNode.getPathCost(), ',heuristic:', tempNode.getHeuristicCost(), ',total:',
        #       tempNode.getTotalCost());

        # tempNode.setParent(currentNode.getState());
        tempNode.setParent(currentNode);

        # children.put(tempNode);
        children.append(tempNode);


def getBlankIndex(currentState):
    i, j = -1, -1;

    for i in range(0, len(currentState)):
        for j in range(0, len(currentState)):
            if (currentState[i][j] == 0):
                return i, j;
    return i, j;


def getGoalIndex(element):
    i, j = -1, -1;

    # print('element:', element)

    for i in range(0, len(goalState)):
        for j in range(0, len(goalState)):
            if (goalState[i][j] == element):
                return i, j;
            pass
    return i, j;


def heuristic(currentState):
    manhattan = 0;
    count = 1;
    for i in range(0, len(currentState)):
        for j in range(0, len(currentState)):
            k, l = getGoalIndex(currentState[i][j]);  # k=i,l=j
            # print('k:', k, 'l:', l);
            manhattan += math.fabs(k - i) + math.fabs(l - j);
            # print('element:', currentState[i][j], 'manhattan:', manhattan);

    return manhattan;


n = int(input('enter n:'));

# a=[[0 for i in range(n)] for j in range(n)];

# a = [[0] * n for i in range(n)];
# count = 0;
#
# for i in range(0, n):
#     for j in range(0, n):
#         a[i][j] = count;
#         count = count + 1;

# a = [[1, 2, 3], [4, 5, 6], [0, 7, 8]];

# a = [[0, 1], [2, 3]];

# a = [[2, 0, 3, 4], [1, 5, 6, 7], [9, 11, 12, 8], [13, 10, 14, 15]];

a = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]];

# print(a);
print('Initial State:');
for i in range(0, n):
    print(a[i]);

number = 1;
goalState = [[0 for i in range(n)] for j in range(n)];
for i in range(0, len(goalState)):
    for j in range(0, len(goalState)):
        if (i == len(goalState) - 1 and j == len(goalState) - 1):
            continue;
        goalState[i][j] = number;
        number += 1;

print('Goal State:');
for i in range(0, n):
    print(goalState[i]);

# print(heuristic(a));

puzzleNode = PuzzleNode(a);

print('Initial state:');
for i in range(0, n):
    print(puzzleNode.getState()[i]);

# children = queue.Queue();
#
children = [];

result = puzzleAStar(puzzleNode);

if (result != None):
    output = [];
    while (result != None):
        output.append(result.getState());
        # print(result.getState());
        result = result.getParent();

    output.reverse();

    for i in output:
        for j in range(0, len(i)):
            print(i[j]);
        print('---')
