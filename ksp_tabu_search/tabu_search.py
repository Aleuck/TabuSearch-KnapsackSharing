import sys, getopt, random, numpy, math, time
from queue import *


NBC = 1
NBF = 1

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
        self.tabu = []
        self.tabuset = set()

class KnapsackSharingTabuSearch:
    instance = None
    best = None
    bestResult = None
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
        return feasable, group_profit[idxMin], total_weigth
    def _generateNeighbors(self, sol, res, entropy):
        local_tabu = set()
        max_neighbors = math.floor(math.pow(self.instance.numItens,1/2)*NBC)
        # elements_in = PriorityQueue();
        # elements_out = PriorityQueue();
        # for i in range(sol.size):
        #     if sol[i]:
        #         elements_in.put((item[1]/item[0], i))
        #     else:
        #         elements_out.put((item[0]/item[1], i))
        neighbors = []
        for n in range(max_neighbors):
            neighbors.append(self._generateNeighborsFlips(sol, res, local_tabu, entropy))
        # for n in range(max_neighbors//4):
        #     neighbors.append({random.randint(0,self.instance.numItens-1)})
        return neighbors
    def _generateNeighborsFlips(self, sol, res, local_tabu, num_flips_per_neighbors):
        flips = set()
        #for i in range(num_flips_per_neighbors):
        while len(flips) < num_flips_per_neighbors:
            flip = random.randint(0,self.instance.numItens-1)
            if flip in local_tabu:
                continue
            if flip in self.tabuset:
                # print ("tabu hit")
                continue
            flips.add(flip)
            local_tabu.add(flip)
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
        if result[1] > previous_result[1]:
            # print("feasable")
            # print (result)
            # print (previous_result)
            return True
        if (result[1] == previous_result[1]
            and result[2] < previous_result[2]):
            return True
        return False
    def solve(self):
        self.best = numpy.ones(self.instance.numItens,dtype=numpy.int8)
        self.bestResult = self.fitness(self.best)
        if (not self.bestResult[0]):
            self._make_feasable(self.best, self.bestResult)
        self.bestResult = self.fitness(self.best)
        # print(self.bestResult)
        print ("Initial solution found (%d)" % self.bestResult[1])
        curSolution = self.best
        curSolutionResult = (True, 0, 0)
        self.tabu = []
        self.tabuset = set()
        maxNonImpIterations = math.floor(math.pow(self.instance.numItens,1/2)*2)
        nonImprovingIterations = 0
        max_tabu_size = math.floor(math.pow(self.instance.numItens,1/2))
        while (nonImprovingIterations < maxNonImpIterations):
            entropy = math.floor(math.log(self.instance.numItens,2+nonImprovingIterations))
            neighbors_flips = self._generateNeighbors(curSolution, curSolutionResult, entropy)
            bestCandidate = None
            bestCandidate_result = None
            bestFlips = None
            for flips in neighbors_flips:
                neighbor = numpy.copy(curSolution)
                for flip in flips:
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
                if flip not in self.tabuset:
                    self.tabu.append(flip)
                    self.tabuset.add(flip)
            while len(self.tabu) > max_tabu_size:
                rem = self.tabu.pop(0)
                self.tabuset.remove(rem)
            curSolution = bestCandidate
            curSolutionResult = bestCandidate_result
            print ("current:  min_profit: %6d  weight: %6d" % (self.bestResult[1], self.bestResult[2]))
            if (self._isBetterResult(curSolutionResult,self.bestResult)):
                nonImprovingIterations = 0
                self.best = curSolution
                self.bestResult = curSolutionResult
                print ("new best: min_profit: %6d  weight: %6d" % (self.bestResult[1], self.bestResult[2]))
            else:
                nonImprovingIterations += 1
        print("best: %d" % self.bestResult[1])






def main(argv):
    inputfile = ''
    outputfile = ''
    seed = random.randint(1, sys.maxsize)
    try:
        opts, args = getopt.getopt(argv,"s:n:f:",["seed="])
    except getopt.GetoptError:
        print ("Error(command should be: %s -s <seed>)" % sys.argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--seed"):
            seed = int(arg)
        elif opt in ("-n"):
            NBC = float(arg)
        elif opt in ("-f"):
            NBF = float(arg)
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
    t_start = time.time()
    solver.solve()
    t_end = time.time() - t_start
    print("%.0d" % (t_end))
    # Gerar solucao inicial

    #generate neighbors



if __name__ == "__main__":
   main(sys.argv[1:])
