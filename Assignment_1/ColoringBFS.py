import copy
import datetime
import queue;

# -------------------------------------------------
import random
import time


class PuzzleNode:

    # constructor
    def __init__(self, state=None, parent=None):
        self.state = state;
        self.parent = None;
        self.action = None;
        self.path_cost = 0;
        self.children = None;

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


# -------------------------------------------------

def compareLeft(currentState, k, l):  # k=i,l=j

    if (l != 0):
        return not (currentState[k][l] == currentState[k][l - 1]);
    return True;


def compareRight(currentState, k, l):  # k=i,l=j
    if (l != len(currentState) - 1):
        return not (currentState[k][l] == currentState[k][l + 1]);
    return True;


def compareUp(currentState, k, l):  # k=i,l=j
    if (k != 0):
        return not (currentState[k][l] == currentState[k - 1][l]);
    return True;


def compareDown(currentState, k, l):  # k=i,l=j # returns True if not equal or ok..else false(equal)
    if (k != len(currentState) - 1):
        return not (currentState[k][l] == currentState[k + 1][l]);
    return True;


def GoalTest(currentState):
    goal = True;
    for i in range(0, len(currentState)):
        for j in range(0, len(currentState)):

            goal = compareLeft(currentState, i, j);
            if (goal == False):
                return goal;

            goal = compareRight(currentState, i, j);
            if (goal == False):
                return goal;

            goal = compareUp(currentState, i, j);
            if (goal == False):
                return goal;

            goal = compareDown(currentState, i, j);
            if (goal == False):
                return goal;
    return goal;


def coloringBFS(puzzleNode):
    print('In ColoringBFS....');
    node = puzzleNode;
    node.path_cost = 0;

    if (GoalTest(node.getState())):
        print('**********Goal Found.**********');
        return node;

    frontier = queue.Queue();
    frontier.put(node);
    # explored = set();

    explored = [];

    for ele in frontier.queue:
        print(ele.getState());
        print('==');

    # explored.add(node.getState());

    while (True):

        failure = None;
        if (frontier.empty()):
            print('Goal Not Found..');
            return failure;

        print('--->frontier:', frontier.qsize());
        node = frontier.get();
        # print('----------------current Node----------------');
        # print(node.getState());

        # time.sleep(1);

        if (node.getState() in explored):
            continue;

        if (node.getState() not in explored):
            explored.append(node.getState());

        # print('explored:', explored);
        print('-->explored:', len(explored));
        colorI, colorJ = getIndexOfSameColor(node.getState());

        # print('colorI:', colorI, ' colorJ:', colorJ);

        colorOne(node, colorI, colorJ);
        colorTwo(node, colorI, colorJ);
        colorThree(node, colorI, colorJ);
        colorFour(node, colorI, colorJ);

        # print('child Size:', len(children));
        #
        # print('----------------children----------------');
        # for ele in children:
        #     print('-->', ele.getState(), '-->', ele.getParent().getState());
        # # time.sleep(1);
        # print('------------------');

        listObj = [];
        for obj in frontier.queue:
            listObj.append(obj.getState());

        # print('listObj:', listObj);

        print();
        print();

        for ele in children:
            # print('parent:', ele.getParent());
            # time.sleep(1);
            if ((ele.getState() not in listObj) or (ele.getState() not in explored)):
                if (GoalTest(ele.getState())):
                    print('**********Goal Found.**********');
                    print(ele.getState());
                    # return ele.getState();
                    return ele;
                frontier.put(ele);

        children.clear();


def colorOne(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (tempNode.getState()[colorI][colorJ] != 1):
        tempNode.getState()[colorI][colorJ] = 1;

        tempNode.setParent(currentNode);
        children.append(tempNode);


def colorTwo(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (tempNode.getState()[colorI][colorJ] != 2):
        tempNode.getState()[colorI][colorJ] = 2;

        tempNode.setParent(currentNode);
        children.append(tempNode);


def colorThree(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (tempNode.getState()[colorI][colorJ] != 3):
        tempNode.getState()[colorI][colorJ] = 3;

        tempNode.setParent(currentNode);
        children.append(tempNode);


def colorFour(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (tempNode.getState()[colorI][colorJ] != 4):
        tempNode.getState()[colorI][colorJ] = 4;

        tempNode.setParent(currentNode);
        children.append(tempNode);


def getIndexOfSameColor(currentState):
    # print('--------------getIndexOfSameColor--------------')
    i, j = None, None;

    for i in range(0, len(currentState)):
        for j in range(0, len(currentState)):
            if (not compareDown(currentState, i, j) or not compareUp(currentState, i, j) or not compareRight(
                    currentState, i,
                    j) or not compareLeft(
                currentState, i, j)):
                return i, j;
    return i, j;


start_time = time.time();
print('start_time:', start_time);

n = int(input('enter n:'));

a = [[0] * n for i in range(n)];

for i in range(0, n):
    for j in range(0, n):
        a[i][j] = random.randint(1, 4);

# a = [[2, 1], [4, 4]];

# a = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]];
a = [[1, 1, 1], [1, 1, 1], [1, 1, 1]];
# a = [[1, 2, 3, 4], [1, 1, 1, 1], [1, 2, 3, 4], [1, 1, 1, 1]];
# a = [[1, 1], [1, 1]];
# a = [[1, 2, 3], [2, 3, 1], [3, 1, 2]];
# a = [[1, 2, 3], [2, 3, 1], [1, 1, 1]];

for i in range(0, n):
    print(a[i]);

puzzleNode = PuzzleNode(a);

print('Initial state:');
for i in range(0, n):
    print(puzzleNode.getState()[i]);

children = [];

result = coloringBFS(puzzleNode);

if (result != None):
    output = [];
    while (result != None):
        output.append(result.getState());
        result = result.getParent();
    output.reverse();
    for i in output:
        for j in range(0, len(i)):
            print(i[j]);
        print('---')

print('end time:', time.time());
print(time.time() - start_time);
elapsed_time_secs = time.time() - start_time;
print('%s sec' % datetime.timedelta(seconds=round(elapsed_time_secs)));
