import copy
import queue;

# -------------------------------------------------
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

def GoalTest(currentState):
    # print('----------------------')
    goal = False;
    # count = 1;
    count = 1;
    for i in range(0, len(currentState)):
        # print(currentState[i]);
        for j in range(0, len(currentState)):
            # print(currentState[i][j], end=' ');

            if (i == len(currentState) - 1 and j == len(currentState) - 1):
                continue;
            if (currentState[i][j] == count):
                count += 1;
                goal = True;
            else:
                # print('--', currentState[i][j]);
                goal = False;
                # print('else goal:', goal, ' count:', count);
                return goal;

    return goal;


def puzzleBFS(puzzleNode):
    print('In PuzzleBFS....');
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

        listObj = [];
        # for obj in frontier.queue:
        #     listObj.append(obj.getState());
        #
        # print('first listObj:', listObj);

        failure = None;
        if (frontier.empty()):
            print('Goal Not Found..');
            return failure;

        # node = frontier.get(frontier);
        node = frontier.get();
        # print('size:', frontier.qsize());
        print('----------------current Node----------------');
        print(node.getState());

        # time.sleep(1);

        if (node.getState() in explored):
            continue;

        # explored.update(node.getState());
        if (node.getState() not in explored):
            explored.append(node.getState());

        print('explored:', explored);

        blankIndexI, blankIndexJ = getBlankIndex(node.getState());

        # print('blankIndex I:', blankIndexI, ' blankIndex J:', blankIndexJ);

        moveRight(node, blankIndexI, blankIndexJ);
        moveLeft(node, blankIndexI, blankIndexJ);
        moveUp(node, blankIndexI, blankIndexJ);
        moveDown(node, blankIndexI, blankIndexJ);

        # print('child Size:', len(children));

        print('----------------children----------------');
        for ele in children:
            print('-->', ele.getState(), '-->', ele.getParent().getState());
        # time.sleep(1);
        print('------------------');

        listObj = [];
        for obj in frontier.queue:
            listObj.append(obj.getState());

        print('listObj:', listObj);

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


def moveUp(currentNode, blankIndexI, blankIndexJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (blankIndexI != 0):
        temp = tempNode.getState()[blankIndexI][blankIndexJ];
        tempNode.getState()[blankIndexI][blankIndexJ] = tempNode.getState()[blankIndexI - 1][blankIndexJ];
        tempNode.getState()[blankIndexI - 1][blankIndexJ] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);
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

a = [[2, 0, 3, 4], [1, 5, 6, 7], [9, 11, 12, 8], [13, 10, 14, 15]];

print(a);

for i in range(0, n):
    print(a[i]);

puzzleNode = PuzzleNode(a);

print('Initial state:');
for i in range(0, n):
    print(puzzleNode.getState()[i]);

# children = queue.Queue();

children = [];

result = puzzleBFS(puzzleNode);

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
