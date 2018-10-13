import copy
import random

import numpy as np


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


def calculateFitOfReproduced(child):
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

    print('---------------------')

    j = 1
    allrooms = []
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
    sameDayFre = 0
    for day in range(0, days):
        print('d:', (day + 1))
        sameDayFre = 0

        oneDayTT = []
        slotCounter = 1
        j = 1

        for r in range(0, len(allrooms)):

            for c in range(initSlot, (endSlot)):
                oneDayTT.append(allrooms[r][c])

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


def reproduce(xChromosome, yChromosome):  #

    n = len(xChromosome.getState())
    c = random.randint(0, n - 1)

    # print('====', c)
    # print('xC:', xChromosome.getState())
    # print('yC:', yChromosome.getState())
    sub1 = xChromosome.getState()[0:c]
    sub2 = xChromosome.getState()[c:n]
    sub3 = yChromosome.getState()[0:c]
    sub4 = yChromosome.getState()[c:n]

    c1 = sub1 + sub4
    c2 = sub3 + sub2

    child1 = Chromosome()
    child2 = Chromosome()

    child1.setState(c1)
    child2.setState(c2)

    print('c1:', c1)
    print('c2:', c2)

    return child1, child2


def sorting(population):  #

    for x in range(0, len(population)):
        for y in range(0, len(population)):
            if (population[y].getFitnessValue() < population[x].getFitnessValue()):
                temp1, temp2 = population[y], population[x];
                population[y] = temp2;
                population[x] = temp1;

    return population


def calculateFitness(population):  #

    print('-----------------Fitness----------------------')
    print(len(population))

    global rooms
    global days
    global slots
    global coursesCount
    global interval

    print('interval:', interval)

    # s1 = []
    # s2 = []
    # s3 = []
    totalConflicts = 0
    sliceLength = (days * slots)

    iterCounter = 1
    for k in range(0, len(population)):  # loop of no.of chromosomes

        i = population[k]
        temp = []
        chromosomeConflicts = 0

        # print('iterCounter:', iterCounter, '-->', len(i.getState()))
        iterCounter = iterCounter + 1

        # s1 = copy.deepcopy(i.getState()[0:20])
        # s2 = copy.deepcopy(i.getState()[20:40])
        # s3 = copy.deepcopy(i.getState()[40:60])

        slotsForRooms = []
        slts = []
        j = 1
        for z in range(0, len(i.getState())):
            slts.append(i.getState()[z])
            if (z == (j * interval) - 1):
                slotsForRooms.append(slts)
                slts = []
                j = j + 1

        # print('==========================================')
        # print(s1)
        # print(s2)
        # print(s3)
        #
        # print('-----------')
        # for z in range(0, len(slotsForRooms)):
        #     print(slotsForRooms[z])
        # print('==========================================')

        for r in range(0, len(slotsForRooms) - 1):
            for c in range(0, len(slotsForRooms[r])):

                if (slotsForRooms[r][c] == slotsForRooms[r + 1][c] and slotsForRooms[r][c] != 0):
                    chromosomeConflicts = chromosomeConflicts + 1

        i.setConflicts(chromosomeConflicts)

        # for j in range(0, sliceLength):
        #     if (s1[j] == s2[j] and s1[j] != 0):
        #         chromosomeConflicts = chromosomeConflicts + 1
        #     if (s1[j] == s3[j] and s1[j] != 0):
        #         chromosomeConflicts = chromosomeConflicts + 1
        #     if (s2[j] == s3[j] and s2[j] != 0):
        #         chromosomeConflicts = chromosomeConflicts + 1
        #
        #     i.setConflicts(chromosomeConflicts)

        totalConflicts = totalConflicts + chromosomeConflicts

    for i in population:
        # i.setFitnessValue(i.getConflicts() / (1+totalConflicts))
        i.setFitnessValue(1 / (1 + i.getConflicts()))
    print('-----------------Fitness completed----------------------')
    return population, totalConflicts


def mutation(child):
    global coursesCount
    # print('------------------ Mutation ------------------------')
    # print('in mutation:courseCount-->', coursesCount)
    n = len(child.getState())
    print()
    c = random.randint(0, n - 1)

    # print(child.getState()[c])
    child.getState()[c] = random.randint(0, coursesCount)
    # print(child.getState()[c])
    print('------------------ Mutation completed------------------------')
    return child


# def geneticAlgo(population, fit):
def geneticAlgo(population):
    while (True):

        print('size:', len(population))

        # print('\n\n\n\n\n\n*******************************************************************************')
        #
        # for i in population:
        #     print(i.getState())
        # print('\n\n\n\n\n\n*******************************************************************************')

        population, totalConflicts = calculateFitness(population)

        population = sorting(population)

        tempPopulation = []
        terminated = False
        for z in range(0, 10):
            tempPopulation.append(population[z])

            if (population[z].getFitnessValue() == 1):
                print('\n\nTerminated:', population[z].getFitnessValue())
                print(population[z].getState())
                terminated = True
                return population[z]
                # break
        # if (terminated):
        #     break

        print('tempPopulation Size=========:', len(tempPopulation))
        newPopulation = []
        newPopulation = tempPopulation

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>', len(newPopulation))
        iteration = 1
        for z in range(0, 9):
            for w in range(z + 1, 10):

                x, y = newPopulation[z], newPopulation[w]

                child1, child2 = reproduce(x, y)

                child1 = calculateFitOfReproduced(child1)
                child2 = calculateFitOfReproduced(child2)

                if (child1.getFitnessValue() <= 0.9):
                    child1 = mutation(child1)
                if (child2.getFitnessValue() <= 0.9):
                    child2 = mutation(child2)

                newPopulation.append(child1)
                newPopulation.append(child2)

                print('iteration:', iteration, '>>>', len(newPopulation))
                iteration = iteration + 1

        population = newPopulation


initialPopulation = []

rooms = 3
slots = 4
days = 5
coursesCount = 4
interval = (days * slots)
courseList = []
courseFrequency = 5
for i in range(0, coursesCount):
    courseList.append(i + 1)

print('days:', days, ' slots:', slots, ' rooms:', rooms)
print('for each room:totalSlots: ', (days * slots))
print('for all rooms: total slots: ', (days * slots * rooms))
print('--> length of chromosome: ', (days * slots * rooms))

popSize = 100
for i in range(0, popSize):

    for j in range(0, days):
        gene = []
        for k in range(0, days * slots * rooms):
            digit = random.randint(0, coursesCount)
            gene.append(digit)

    chrom = Chromosome()
    chrom.setState(gene)

    initialPopulation.append(chrom)

counter = 0
# for i in initialPopulation:
#     print('chromosome: ', counter)
#     print(i.getState()[0:20])
#     print(i.getState()[20:40])
#     print(i.getState()[40:60])
#     counter = counter + 1
#     print('-----------')

# initialPopulation, totalConflicts = calculateFitness(initialPopulation)

# geneticAlgo(initialPopulation, fitness)
finalChromosome = geneticAlgo(initialPopulation)

print()

j = 1
for i in range(0, len(finalChromosome.getState())):
    print(finalChromosome.getState()[i], end=' ')

    if (i == (j * interval) - 1):
        j = j + 1;
        print()
print('-----------')
