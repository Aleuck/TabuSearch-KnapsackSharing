import sys, getopt, random, numpy

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
    def fitness(solution):
        group_profit = numpy.zeros(self.numGroups, dtype=numpy.int32)
        total_weigth = 0
        for index, value in enumerate(solution):
            if value == 1:
                group_profit[self.itens[index,2]] += self.itens[index,1]
                total_weigth += self.itens[index,0]
        feasable = total_weigth <= self.capacity
        return feasable, group_profit.min()

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
    for i, size in enumerate(sizeGroups):
        print ("group %d has %d elements" % (i, size))
    currentGroup = 0
    groupBase = 0
    ksp = KnapsackSharing(capacity=knapsackCapacity, num_itens=numItens, num_groups=numGroups)
    for i, line in enumerate(sys.stdin):
        if i - groupBase >= sizeGroups[currentGroup]:
            currentGroup += 1;
            groupBase = i;
        aux = list(map(int,line.split()))
        aux.append(currentGroup)
        ksp.itens[i] = aux


if __name__ == "__main__":
   main(sys.argv[1:])
