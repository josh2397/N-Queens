from random import random
import numpy as np
from random import randint
from random import randrange
import time
import matplotlib.pyplot as plt
import operator

class Genetic:
    def __init__(self, n):



        # run genetic algorithm
        self.n = n
        start = time.time()
        self.genetic(n)
        end = time.time()
        runtime = (end-start)

        print("Runtime:", end - start, "(seconds)")

    def genetic(self, n):
        # Initialise algorithm parameters
        populationSize = int(15*n/10)
        # The point within the population where
        cutoff = int(populationSize/3)
        mutationProbability = 75

        self.population = self.initPopulation(n, populationSize)
        print(self.population)
        self.sortPopulation(self.population, n, 0, populationSize)
        self.printBoard(self.population[0], n)
        generation = 1
        while self.fitness(self.population[0], n) != 0:

            self.population = self.parentSelection(self.population, populationSize, cutoff, mutationProbability)
            self.sortPopulation(self.population, n, 0, populationSize)
            print("\r", "Generation:", generation, " cost:", self.fitness(self.population[0], n), self.population[0], end="",flush=True)
            generation += 1

        print("\r", "Generation:", generation, " cost:", self.fitness(self.population[0], n), self.population[0], end="", flush=True)
        self.printBoard(self.population[0], n)

    def initPopulation(self, n, populationSize):
        populationSize += 1
        population = []

        # produce the initial population
        for p in range(populationSize):
            population.append([])
            population[p] = ([randint(0, n - 1) for x in range(n)])

        return population

    def parentSelection(self, population, populationSize, cutoff, mutationProbability):
        x = []
        y = []

        newPopulation = []
        # create a new population from the parents
        for i in range(0, populationSize + 1):
            # randomly select parents
            p = randint(0, cutoff)
            q = randint(0, cutoff)
            # check that parents are not the same
            while q == p:
                q = randint(0, cutoff)

            x = population[p]
            y = population[q]
            # create child from parents
            child = self.crossover(x, y, mutationProbability)
            # add child to population
            newPopulation.append(child)
        population = newPopulation[:]

        return population

    def crossover(self, x, y, mutationProbability):
        child = []
        # select a random point to merge both configurations
        crossOverPoint = int(self.n/2)

        for i in range(crossOverPoint):

            child.append(x[i])

        for i in range(crossOverPoint, self.n):

            child.append(y[i])


        self.mutation(child, mutationProbability)

        return child

    def mutation(self, child, mutationProbability):
        # TODO - mutate child using a probability
        # mutationPosition = [randint(0, self.n-1) for i in range(mutations)]
        if mutationProbability > randrange(0, 100):
            i = randint(0, self.n - 1)
            child[i] = randint(0, self.n - 1)

        return child

    def sortPopulation(self, population, n, low, high):

        if low < high:
            partition = self.quickSort(population, low, high)

            self.sortPopulation(population, n, low, partition - 1)
            self.sortPopulation(population, n, partition + 1, high)

    def quickSort(self, population, low, high):


        i = low - 1
        pivot = self.fitness(population[high - 1], self.n)
        for j in range(low, high):

            if self.fitness(population[j], self.n) <= pivot:
                i += 1
                population[i], population[j] = population[j], population[i]
        population[i+1], population[high] = population[high], population[i+1]

        return i + 1

    def fitness(self, queens, n):
        """
        Calculates the cost/fitness by counting the number of queen conflicts
        """

        conflicts = 0

        for i in range(n):
            for j in range(i + 1, n):
                if i != j:
                    # Horizontal axis
                    if queens[i] == queens[j]:
                        conflicts = conflicts + 1
                    # Diagonal Axis Positive
                    if abs(queens[i] - queens[j]) == abs(i - j):
                        conflicts = conflicts + 1
        return int(conflicts)


    def printBoard(self, queens, n):
        """
        Prints out the board with the queens array.
        """
        print("\n")
        for i in range(n):

            print("|", end='')
            for j in range(n):

                if queens[j] == i:
                    print(" x |", end='')

                else:
                    print("   |", end='')

            print("\n")