import copy
import datetime
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

    # print('---------------------')

    j = 1
    allrooms = []
    rm = []
    for g in range(0, len(child.getState())):

        rm.append(child.getState()[g])

        if (g == (j * interval) - 1):
            allrooms.append(rm)
            # print('r:', j)
            # print(rm)
            j = j + 1
            rm = []

    s = 1
    initSlot = 0
    endSlot = s * slots
    sameDayFre = 0
    for day in range(0, days):
        # print('d:', (day + 1))
        sameDayFre = 0

        oneDayTT = []
        slotCounter = 1
        j = 1

        for r in range(0, len(allrooms)):

            for c in range(initSlot, (endSlot)):
                oneDayTT.append(allrooms[r][c])

            # print('day:', (day + 1))
            # print(oneDayTT)

        initSlot = endSlot
        s = s + 1
        endSlot = slots * s

        for subject in range(0, len(courseList)):

            sameDayFre = oneDayTT.count(courseList[subject])
            if (sameDayFre > 1):
                # print('in sameDayFre')
                # print(child.getState())
                chromosomeConflicts = chromosomeConflicts + sameDayFre

    child.setConflicts(chromosomeConflicts)
    child.setFitnessValue(1 / (1 + child.getConflicts()))

    return child


def getBlankIndex(currentNode):
    zeroIndex = -1
    for i in range(0, len(currentNode.getState())):
        if (currentNode.getState()[i] == -1):
            # print('index:', i)
            zeroIndex = i
            return i
    return zeroIndex


def displayChildren():
    print('in dd')
    for i in children:
        print(i.getState())


def generate(currentNode, zeroIndex):
    tempNode = copy.deepcopy(currentNode);

    for i in range(0, coursesCount + 1):
        tempNode.getState()[zeroIndex] = i

        tempNode = calculateFitness(tempNode)
        if (tempNode.getFitnessValue() == 1):
            print('-->', tempNode.getFitnessValue())

        children.append(tempNode);
        tempNode = copy.deepcopy(currentNode)

    # displayChildren()
    # print('---')


def backtrackingCSP(chromosome):
    print('------------------------------------')

    global maxIterations
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

        # print('======')
        generate(node, zeroIndex);

        for ele in children:
            if ((ele.getState() not in listObj) or (ele.getState() not in explored)):
                if (ele.getFitnessValue() == 1):
                    print('\n**********Goal Found.**********');
                    print(ele.getState());

                    return ele;
                frontier.append(ele);

        children.clear();
        maxIterations += 1
        print('running..')
        # print()
        # print('\n');


rooms = 4
slots = 5
days = 5
coursesCount = 5
interval = (days * slots)
courseList = []
courseFrequency = 3
for i in range(0, coursesCount):
    courseList.append(i + 1)

print('days:', days, ' slots:', slots, ' rooms:', rooms)
print('for each room:totalSlots: ', (days * slots))
print('courses count:', coursesCount)
print('for all rooms: total slots: ', (days * slots * rooms))

print('--> length of chromosome: ', (days * slots * rooms))
time.sleep(1)
a = [-1 for i in range(days * slots * rooms)]

initialTT = Chromosome()
# initialTT.setState(gene)
initialTT.setState(a)
initialTT = calculateFitness(initialTT)

children = [];
zeroCheck = True

start_time = time.time();
print('start_time:', start_time);

maxIterations = 0

finalChromosome = backtrackingCSP(initialTT)

j = 1

print('end time:', time.time());
print(time.time() - start_time);
elapsed_time_secs = time.time() - start_time;
print('%s sec' % datetime.timedelta(seconds=round(elapsed_time_secs)));
print('Iterations:', maxIterations)

if (finalChromosome != None):

    for n, i in enumerate(finalChromosome.getState()):
        if (i == -1):
            finalChromosome.getState()[n] = 0

    j = 1
    k = 1
    for i in range(0, len(finalChromosome.getState())):
        print(finalChromosome.getState()[i], end=' ')
        if (i == (slots * k) - 1):
            print(' | ', end=' ')
            k += 1
        if (i == (interval * j) - 1):
            print()
            j += 1

    if (i == (j * interval) - 1):
        j = j + 1;
        print()
    print('\n-----------')

    print('c 0', finalChromosome.getState().count(0))
    for i in range(0, len(courseList)):
        print('c', (i + 1), finalChromosome.getState().count(courseList[i]))
