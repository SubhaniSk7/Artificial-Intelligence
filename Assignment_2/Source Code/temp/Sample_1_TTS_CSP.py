import copy
import random
import time


class Course:

    # constructor
    def __init__(self, professor=None, count=None):
        self.professor = professor
        self.count = count

    def setProfessor(self, professor):
        self.professor = professor

    def getProfessor(self):
        return self.professor

    def setCount(self, count):
        self.professor = count

    def getCount(self):
        return self.count


class Chromosome:

    # constructor
    def __init__(self, state=[], parent=None, conflicts=None, courseList=[], fitnessValue=0):
        self.state = state
        self.parent = parent
        self.conflicts = 0
        self.courseList = courseList

        self.fitnessValue = fitnessValue

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def setConflicts(self, conflicts):
        self.conflicts = conflicts

    def getConflicts(self):
        return self.conflicts

    def setCourseList(self, courseList):
        self.courseList = courseList

    def getCourseList(self):
        return self.courseList

    def setFitnessValue(self, fitnessValue):
        self.fitnessValue = fitnessValue

    def getFitnessValue(self):
        return self.fitnessValue


def display(node):
    pass


def calculateFitness(child):
    # print('-----------------Fitness----------------------')

    global rooms
    global days
    global slots
    global coursesCount
    global interval

    chromosomeConflicts = 0

    slotsForRooms = []

    # print('interval:', interval)

    slts = []
    j = 1
    for i in range(0, len(child.getState())):
        slts.append(child.getState()[i])
        if (i == (j * interval) - 1):
            # print('-----')
            slotsForRooms.append(slts)
            slts = []
            j = j + 1

    # print('==========================================fit')
    #
    # for i in range(0, len(slotsForRooms)):
    #     print(slotsForRooms[i])
    # print('==========================================')

    for i in range(0, len(slotsForRooms) - 1):
        for j in range(0, len(slotsForRooms[i])):

            if (slotsForRooms[i][j] == slotsForRooms[i + 1][j] and slotsForRooms[i][j] != 0):
                chromosomeConflicts = chromosomeConflicts + 1

    cfreq = 0
    for subject in range(0, len(courseList)):
        cfreq = 0
        cfreq = child.getState().count(courseList[subject])

        if (cfreq < courseFrequency):
            chromosomeConflicts = chromosomeConflicts + (courseFrequency - cfreq)
            # print(child.getState())
            # print('-->in cfreq:', chromosomeConflicts)

    sameDayFre = 0
    allrooms = []
    print('---------------------')

    slotCounter = 0
    j = 1
    # for r in range(0, rooms):
    #     print('r:', (r + 1))
    rm = []
    for g in range(0, len(child.getState())):

        rm.append(child.getState()[g])

        if (g == (j * interval) - 1):
            allrooms.append(rm)
            print('r:', j)
            print(rm)
            j = j + 1
            rm = []

    print('')

    s = 1
    initSlot = 0
    endSlot = s * slots
    for day in range(0, days):
        print('d:', (day + 1))
        sameDayFre = 0

        oneDayTT = []
        slotCounter = 1
        j = 1

        for r in range(0, len(allrooms)):
            oneDayTT = allrooms[r][initSlot:(endSlot + 1)]

            print('day:', (day + 1))
            print(oneDayTT)

        initSlot = endSlot
        s = s + 1
        endSlot = slots * s

        for subject in range(0, len(courseList)):

            sameDayFre = oneDayTT.count(courseList[subject])
            if (sameDayFre > 1):
                print('in sameDayFre')
                print(child.getState())
                chromosomeConflicts = chromosomeConflicts + sameDayFre

    child.setConflicts(chromosomeConflicts)
    child.setFitnessValue(1 / (1 + child.getConflicts()))

    return child


def getBlankIndex(currentNode):
    zeroIndex = -1
    for i in range(0, len(currentNode.getState())):
        if (currentNode.getState()[i] == -1):
            print('index:', i)
            zeroIndex = i
            return i
            # return zeroIndex
    return zeroIndex


def displayChildren():
    for i in children:
        print(i.getState())


def generate(currentNode, zeroIndex):
    tempNode = copy.deepcopy(currentNode);

    for i in range(0, coursesCount + 1):
        tempNode.getState()[zeroIndex] = i

        tempNode = calculateFitness(tempNode)
        if (tempNode.getFitnessValue() == 1):
            print('\n\n\n\n\n\n')
            print('-->', tempNode.getFitnessValue())

        if (tempNode.getState() == [1, 2, 0, 0, 0, 0, 1, 2]):
            exit(1)
        children.append(tempNode);
        tempNode = copy.deepcopy(currentNode)
    displayChildren()


def backtrackingCSP(chromosome):
    print('------------------------------------')
    print('In backtrackingCSP....');
    node = chromosome

    if (node.getFitnessValue() == 1):
        print('**********Goal Found.**********');
        return node;

    frontier = [];
    frontier.append(node);

    explored = [];

    # for ele in frontier:
    #     print(ele.getState());
    #     print('==');

    while (True):

        listObj = [];
        # for x in range(0, len(frontier)):
        #     for y in range(x, len(frontier)):
        #         if (frontier[y].getFitnessValue() > frontier[x].getFitnessValue()):
        #             temp1, temp2 = frontier[y], frontier[x];
        #             frontier[y] = temp2;
        #             frontier[x] = temp1;

        failure = None;
        if (not frontier):
            print('Goal Not Found..');
            return failure;

        node = frontier[0];
        del frontier[0];

        # print('----------------current Node----------------');
        # display(node)

        if (node.getState() in explored):
            continue;

        if (node.getState() not in explored):
            explored.append(node.getState());

            # print('explored:', explored);

        zeroIndex = getBlankIndex(node)

        generate(node, zeroIndex);

        for ele in children:
            if ((ele.getState() not in listObj) or (ele.getState() not in explored)):
                if (ele.getFitnessValue() == 1):
                    print('\n**********Goal Found.**********');
                    print(ele.getState());

                    return ele;
                frontier.append(ele);

        children.clear();
        print()
        # print('\n');


rooms = 2
slots = 2
days = 2
coursesCount = 2
interval = (days * slots)
courseList = []
courseFrequency = 2
for i in range(0, coursesCount):
    courseList.append(i + 1)

print('days:', days, ' slots:', slots, ' rooms:', rooms)
print('for each room:totalSlots: ', (days * slots))
print('courses count:', coursesCount)
print('for all rooms: total slots: ', (days * slots * rooms))

print('--> length of chromosome: ', (days * slots * rooms))
time.sleep(1)
a = [-1 for i in range(days * slots * rooms)]

# a = []
# j = 1
# freq = 0
# for i in range(0, (days * slots * rooms)):
#     if (i > (coursesCount * courseFrequency) - 1):
#         a.append(0)
#     else:
#         a.append(j)
#         freq = freq + 1
#     if (freq == courseFrequency):
#         j = j + 1
#         freq = 0


initialTT = Chromosome()
# initialTT.setState(gene)
initialTT.setState(a)
initialTT = calculateFitness(initialTT)

children = [];
zeroCheck = True
finalChromosome = backtrackingCSP(initialTT)

j = 1

if (finalChromosome != None):
    for i in range(0, len(finalChromosome.getState())):
        print(finalChromosome.getState()[i], end=' ')

    if (i == (j * interval) - 1):
        j = j + 1;
        print()
    print('-----------')

    print('c 0', finalChromosome.getState().count(0))
    for i in range(0, len(courseList)):
        print('c', (i + 1), finalChromosome.getState().count(courseList[i]))
