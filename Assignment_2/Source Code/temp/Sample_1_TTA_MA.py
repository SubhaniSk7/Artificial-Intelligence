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
    # print('-----------------Fitness for Reproduced----------------------')

    global rooms
    global days
    global slots
    global coursesCount

    s1 = []
    s2 = []
    s3 = []
    totalConflicts = 0

    chromosomeConflicts = 0

    slotsForRooms = []

    global interval

    print('interval:', interval)

    s1 = copy.deepcopy(child.getState()[0:20])
    s2 = copy.deepcopy(child.getState()[20:40])
    s3 = copy.deepcopy(child.getState()[40:60])

    slts = []
    j = 1
    for i in range(0, len(child.getState())):
        slts.append(child.getState()[i])
        if (i == (j * interval) - 1):
            print('-----')
            slotsForRooms.append(slts)
            slts = []
            j = j + 1

    print('==========================================rep fit')
    print(s1)
    print(s2)
    print(s3)

    print('-----------')
    for i in range(0, len(slotsForRooms)):
        print(slotsForRooms[i])
    print('==========================================')

    for i in range(0, len(slotsForRooms) - 1):
        for j in range(0, len(slotsForRooms[i])):

            if (slotsForRooms[i][j] == slotsForRooms[i + 1][j] and slotsForRooms[i][j] != 0):
                chromosomeConflicts = chromosomeConflicts + 1

    child.setConflicts(chromosomeConflicts)

    # for j in range(0, sliceLength):
    #     if (s1[j] == s2[j] and s1[j] != 0):
    #         chromosomeConflicts = chromosomeConflicts + 1
    #     if (s1[j] == s3[j] and s1[j] != 0):
    #         chromosomeConflicts = chromosomeConflicts + 1
    #     if (s2[j] == s3[j] and s2[j] != 0):
    #         chromosomeConflicts = chromosomeConflicts + 1
    #
    #     child.setConflicts(chromosomeConflicts)

    child.setFitnessValue(1 / (1 + child.getConflicts()))
    # print('-----------------Fitness completed----------------------')
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

    # print('c1:', c1)
    # print('c2:', c2)

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
    print('mutation:', child.getFitnessValue())
    c = random.randint(0, n - 1)

    child.getState()[c] = random.randint(0, coursesCount)
    # print('------------------ Mutation completed------------------------')
    return child


def localSearch(child):
    # print('----->local:child:',child.getFitnessValue())
    n = len(child.getState())
    currentChild = copy.deepcopy(child)

    for i in range(0, 3):
        print(i)
        mutatedChild = mutation(currentChild)
        mutatedChild = calculateFitOfReproduced(mutatedChild)
        if (mutatedChild.getFitnessValue() > currentChild.getFitnessValue()):
            print('local -->if:', currentChild.getFitnessValue(), '  :', mutatedChild.getFitnessValue())
            currentChild = mutatedChild
            print('local if after:', currentChild.getFitnessValue(), '  :', mutatedChild.getFitnessValue())
            return currentChild

    child = currentChild
    return child


def geneticAlgo(population):
    while (True):

        print('size:', len(population))

        population, totalConflicts = calculateFitness(population)

        population = sorting(population)

        tempPopulation = []

        for z in range(0, 10):
            tempPopulation.append(population[z])

            if (population[z].getFitnessValue() == 1):
                print('\n\nTerminated:', population[z].getFitnessValue())
                print(population[z].getState())
                return population[z]

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

                child1Optimized = copy.deepcopy(child1)
                child2Optimized = copy.deepcopy(child2)

                child1Optimized = localSearch(child1Optimized)
                child2Optimized = localSearch(child2Optimized)

                if (child1Optimized.getFitnessValue() > child1.getFitnessValue()):
                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    print('child1Optimized:', child1Optimized.getFitnessValue(), ' child1:', child1.getFitnessValue())
                    child1 = child1Optimized

                if (child2Optimized.getFitnessValue() > child2.getFitnessValue()):
                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    print('child2Optimized:', child2Optimized.getFitnessValue(), ' child2:', child2.getFitnessValue())

                    child2 = child2Optimized

                newPopulation.append(child1)
                newPopulation.append(child2)

                # print('iteration:', iteration, '>>>', len(newPopulation))
                iteration = iteration + 1

        population = newPopulation


initialPopulation = []

rooms = 3
slots = 4
days = 5
coursesCount = 4
interval = (days * slots)
courseList=[]
for i in range(0,coursesCount):
    courseList.append(i+1)

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

finalChromosome = geneticAlgo(initialPopulation)

# print(finalChromosome.getState()[0:20])
# print(finalChromosome.getState()[20:40])
# print(finalChromosome.getState()[40:60])
# print('-----------')

print()


j = 1
for i in range(0, len(finalChromosome.getState())):
    print(finalChromosome.getState()[i], end=' ')

    if (i == (j * interval) - 1):
        j = j + 1;
        print()
print('-----------')
