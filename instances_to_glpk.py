import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ("Error(command should be: instances_to_glpk.py -i <inputfile> -o <outputfile>)")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    with open(inputfile) as f:
        n = int(f.readline())
        g = int(f.readline())
        c = int(f.readline())
        
        tam_grupos = map(int,f.readline().split())
        groups = []
        for tam in tam_grupos:
            group = []
            for j in range(tam):
                s,p = f.readline().split()
                s,p = int(s), int(p);
                group.append([s,p])
            groups.append(group)

    with open(outputfile, "w") as of:
        of.write('data;\n\n')
        of.write('param nOfGroups :=' + str(g) + '\n')
        of.write('param nOfObjects :=' + str(n) + '\n')
        of.write('param C := ' + str(c) + ';\n\n')
        
        of.write('/* groups */\n')
        of.write('param g :\t')
        for i in range(n):
            of.write("%3.0d\t" % (i+1))
        of.write(':=\n')
        bottom = 0
        for i in range(g):
            of.write("\t\t%3.0d\t" % (i+1)) # '\t\t' + str(i+1) + '\t\t')
            for j in range(n):
                if(j >= bottom and j < bottom + len(groups[i])):
                    of.write(' 1' + '\t\t')
                else:
                    of.write(' 0' + '\t\t')
            bottom = bottom + len(groups[i])
            of.write('\n')
        of.write(';\n\n')

        of.write('/* profit */\n')
        of.write('param p :=\n')
        count = 1
        for group in groups:
            for item in group:
                of.write(str(count) + ' ' + str(item[1]) + '\n')
                count = count + 1
        of.write(';\n\n')

        of.write('/* weight */\n')
        of.write('param w :=\n')
        count = 1
        for group in groups:
            for item in group:
                of.write(str(count) + ' ' + str(item[0]) + '\n')
                count = count + 1
        of.write(';\n')

if __name__ == "__main__":
   main(sys.argv[1:])
