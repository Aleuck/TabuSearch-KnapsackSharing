import sys, getopt, random, numpy, math
from queue import *

class KnapsackSharing:
    capacity = 0
    numItens = 0
    numGroups = 0
    itens = None
    groupsOffset = None
    def __init__(self, capacity, num_itens, num_groups):
        self.capacity = capacity
        self.numItens = num_itens
        self.numGroups = num_groups
        self.groupsOffset = [None]*self.numGroups
        self.itens = numpy.zeros(shape=[self.numItens,3],dtype=numpy.int16)

class KnapsackSharingTabuSearch:
    instance = None
    best = None
    bestResult = None
    tabu = []
    def __init__(self, instance):
        self.instance = instance
    def fitness(self, solution):
        group_profit = numpy.zeros(self.instance.numGroups, dtype=numpy.int32)
        total_weigth = 0
        for index in range(self.instance.numItens):
            if solution[index] == 1:
                group_profit[self.instance.itens[index,2]] += self.instance.itens[index,1]
                total_weigth += self.instance.itens[index,0]
        feasable = total_weigth <= self.instance.capacity
        idxMin = group_profit.argmin()
        return feasable, group_profit[idxMin], total_weigth, group_profit
    def _generateNeighbors(self, sol, res):
        max_neighbors = math.floor(math.sqrt(self.instance.numItens))
        neighbors = []
        for n in range(max_neighbors):
            neighbors.append(self._generateNeighborsFlips())
        return neighbors
    def _generateNeighborsFlips(self):
        num_flips_per_neighbors = math.floor(math.sqrt(self.instance.numItens))
        flips = []
        for i in range(num_flips_per_neighbors):
            flip = random.randint(0,self.instance.numItens-1)
            if flips.count(flip) == 0 and self.tabu.count(flip) == 0:
                flips.append(flip)
        return flips
    def _make_feasable(self, sol, result):
        total_weigth = result[2]
        heaviest = (-1, 0);
        pq = PriorityQueue()
        for i in range(self.instance.numItens):
            if sol[i] == 1 and self.instance.itens[i][0] >= heaviest[1]:
                pq.put((-self.instance.itens[i][0],i))
        while total_weigth > self.instance.capacity:
            item = pq.get()
            sol[item[1]] = 0;
            total_weigth -= self.instance.itens[item[1]][0]
    def _isBetterResult(self, result, previous_result):
        if not result[0]:
            return False
        if result[1] >= previous_result[1]:
            print("feasable")
            print (result)
            print (previous_result)
            return True
        return False
    def solve(self):
        self.best = numpy.ones(self.instance.numItens,dtype=numpy.int8)
        self.bestResult = self.fitness(self.best)
        if (not self.bestResult[0]):
            self._make_feasable(self.best, self.bestResult)
        self.bestResult = self.fitness(self.best)
        print(self.bestResult)
        maxNonImpIterations = math.floor(math.sqrt(self.instance.numItens))
        nonImprovingIterations = 0
        tabu = []
        curSolution = self.best
        curSolutionResult = (True, 0, 0)
        while (nonImprovingIterations < maxNonImpIterations):
            neighbors_flips = self._generateNeighbors(curSolution, curSolutionResult)
            bestCandidate = None
            bestCandidate_result = None
            bestFlips = None
            max_tabu_size = math.floor((self.instance.numItens/4))
            for flips_idx, flips in enumerate(neighbors_flips):
                for flip in flips:
                    neighbor = numpy.copy(curSolution)
                    neighbor[flip] = 1 - neighbor[flip]
                neighbor_result = self.fitness(neighbor)
                if not neighbor_result[0]:
                    self._make_feasable(neighbor, neighbor_result);
                neighbor_result = self.fitness(neighbor)
                if (bestCandidate_result is None) or self._isBetterResult(neighbor_result, bestCandidate_result):
                    bestCandidate = neighbor
                    bestCandidate_result = neighbor_result
                    bestFlips = flips
            for flip in bestFlips:
                tabu.append(flip)
            if len(tabu) > max_tabu_size:
                tabu.pop(0)
            curSolution = bestCandidate
            curSolutionResult = bestCandidate_result
            if (self._isBetterResult(curSolutionResult,self.bestResult)):
                nonImprovingIterations = 0
                self.best = curSolution
                self.bestResult = curSolutionResult
            else:
                nonImprovingIterations += 1







def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"s:",["seed="])
    except getopt.GetoptError:
        print ("Error(command should be: %s -s <seed>)" % sys.argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--seed"):
            seed = int(arg)
    try:
        seed
    except NameError:
        seed = random.randint(1, sys.maxsize)
    print("seed = %s" % seed)
    random.seed(seed)

    numItens = int(input())
    numGroups = int(input())
    knapsackCapacity = int(input())
    sizeGroups = list(map(int,input().split()))
    print ("n=%d, g=%d, c=%d" % (numItens,numGroups,knapsackCapacity))
    currentGroup = 0
    groupBase = 0
    ksp = KnapsackSharing(capacity=knapsackCapacity, num_itens=numItens,
                          num_groups=numGroups)
    for i, line in enumerate(sys.stdin):
        if i - groupBase >= sizeGroups[currentGroup]:
            ksp.groupsOffset[currentGroup] = (groupBase, i)
            currentGroup += 1;
            groupBase = i;
        aux = list(map(int,line.split()))
        aux.append(currentGroup)
        ksp.itens[i] = aux

    solver = KnapsackSharingTabuSearch(ksp)
    solver.solve()
    # Gerar solucao inicial

    #generate neighbors



if __name__ == "__main__":
   main(sys.argv[1:])
