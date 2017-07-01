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
        

if __name__ == "__main__":
   main(sys.argv[1:])
