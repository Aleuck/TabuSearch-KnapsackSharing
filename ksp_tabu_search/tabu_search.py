import sys, getopt, random, numpy, math
from queue import *

class KnapsackSharing:
    capacity = 0
    numItens = 0
    numGroups = 0
    itens = None
    def __init__(self, capacity, num_itens, num_groups):
        self.capacity = capacity
        self.numItens = num_itens
        self.numGroups = num_groups
        self.itens = numpy.zeros(shape=[self.numItens,3],dtype=numpy.int16)

class KnapsackSharingTabuSearch:
    instance = None
    best = None
    bestResult = None
    def __init__(self, instance):
        self.instance = instance
    def fitness(self, solution):
        group_profit = numpy.zeros(self.instance.numGroups, dtype=numpy.int32)
        total_weigth = 0
        for index, value in enumerate(solution):
            if value == 1:
                group_profit[self.instance.itens[index,2]] += self.instance.itens[index,1]
                total_weigth += self.instance.itens[index,0]
        feasable = total_weigth <= self.instance.capacity
        return feasable, group_profit.min(), total_weigth
    def _generateNeighborsFlips(self):
        num_neighbors = math.floor(math.sqrt(self.instance.numItens))
        flips = []
        for i in range(num_neighbors):
            flips.append(random.randint(0,self.instance.numItens-1))
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
    def generateNeighboors(self, max_neighbors):
        return
    def solve(self):
        self.best = numpy.ones(self.instance.numItens,dtype=numpy.int8)
        self.bestResult = self.fitness(self.best)
        if (not self.bestResult[0]):
            self._make_feasable(self.best, self.bestResult)
        self.bestResult = self.fitness(self.best)
        print(self.bestResult)
        print(self.best)


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
