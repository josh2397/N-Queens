from __future__ import division
from random import random
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import time


class SimulatedAnnealingExperiment:
    ''''''
    def __init__(self, queens, n):

        self.queens = queens
        self.n = n
        runtimeStat = []
        iterations = 30
        minimum = []
        maximum = []

        for i in range(0.5, 0.999, 0.05):
            sum = 0
            average = 0
            alpha = i
            runtime = []
            self.queens[:] = list([randint(0, n - 1) for x in range(n)])
            for j in range(20):

                # print initial board state
                #self.printBoard(self.queens, n)
                # start timer
                start = time.time()
                self.anneal(n)
                end = time.time()
                runtime.append((end - start))
                #self.printBoard(self.queens, n)
                #print("Runtime:", end - start, "(seconds)")
                self.queens[:] = list([randint(0, n - 1) for x in range(n)])
            for x in range(len(runtime)):
                sum += runtime[x]
            minimum.append(min(runtime))
            maximum.append(max(runtime))

            average = sum / len(runtime)

            runtimeStat.append(average)
        print('\n', minimum, '\n', maximum)
        xaxis = [i for i in range(4, iterations)]
        print(runtimeStat)
        plt.plot(xaxis, runtimeStat, color='black', linestyle='dashed')
        plt.xlabel('Number of Queens')
        plt.ylabel('Runtime')
        plt.title('Simulated Annealing')
        plt.show()
    def anneal(self, n):

        currentCost = self.cost(self.queens, n)

        # Continue to search until a goal node is reached
        while self.cost(self.queens, n) != 0:
            k = 0
            T = 1.0
            T0 = 1.0
            T_min = 0.0001
            alpha = 0.9

            # Reduce the temperature until the threshold is reached
            while T > T_min:

                i = 1
                # print the goal node cost and its queen locations
                if currentCost == 0 and T <= T_min:
                    print('\r', "Cost:", currentCost, self.queens, end='\n', flush=True)
                else:
                    print('\r', "Cost:", currentCost, self.queens, "queens:", n, end='', flush=True)

                # Choose 100 random neighbours and apply the acceptance probability
                while i <= 100:

                    nextState = self.randomNeighbour(self.queens, n)

                    nextCost = self.cost(nextState, n)

                    a = np.exp(-(nextCost - currentCost) / T)

                    if a > random():
                        self.queens = nextState
                        currentCost = nextCost
                        if currentCost == 0:
                            break
                    i += 1
                if currentCost == 0:
                    break

                T = T*alpha
                #T = 1 / np.log(k + 1)
                #T = alpha**k
                #T = 1 / (1 + alpha*k**2)
                k += 1
                #print(T)
                '''T0 = T
                T = alpha / (np.log(T + T0))'''

    def randomNeighbour(self, queens, n):

        queensTemp = queens[:]

        # Select a random row and column for the random neighbour
        i = randint(0, n - 1)
        j = randint(0, n - 1)

        queensTemp[i] = j

        return queensTemp[:]

    def cost(self, queens, n):
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

        print("\n")
        for i in range(n):

            print("|", end='')
            for j in range(n):

                if queens[j] == i:
                    print(" x |", end='')

                else:
                    print("   |", end='')

            print("\n")