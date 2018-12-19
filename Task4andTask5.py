import reader 
import Nobjects
import operator
import random


outputpath = "Output.txt"

# datapath = "datasets/Email-Enron.txt" # Undirected, but very large
datapath = "datasets/Wiki-Vote.txt" # Directed, good test set
# datapath = "datasets/government_edges.csv" Directed, good test set
# datapath = "datasets/politician_edges.csv"

def task3(dset):
    return dset.findInfluencers()

def printHeader(msg, div = "=", length = 80):
    '''Returns a formatted header using specified divider capped at length'''

    n = len(str(msg))
    if n % 2 == 1:
        n =- 1
    rem = int((length-(n+2))/2)*div
    
    return('\n' + rem + " " + msg + " " + rem + '\n\n')


def printAndWrite(out, msg):
    ''' Automate printing and writing to a file '''
    print(msg, end="")
    out.write(msg)
    
def neatlyPrintList(l, length=80):
    ''' Formats output to match specified line length '''
    breakline = 0
    st =''
    
    for item in l:
       
        # Check if we should insert a line break based on line length
        if breakline + len(str(item)) >= length-1:
            st += "\n"
            breakline = len(str(item))
        else:
            breakline += len(str(item))
        
        # Add item to our output string
        st += str(item)

        # Check if we should put a comma at the end
        if item != l[-1]:
            st += ", "
            breakline += 2
    return st

def tasks4and5(data, outputfile):
    print("\n\nBeginning component search(May take some time)")
    
    # Quickly print network stats
    quick =  ("\n\n---- Quick Network Stats---\n")
    quick += ("Total Nodes                         : "+ str(len(dset.getNodes())) + "\n")
    quick += ("Total Edges                         : "+ str(len(dset.getReversedEdges())) +"\n")
    
    # Calcuate Strong/Weakly connected components
    strong = reader.stronglyConnectedComponents(data).getConnectedComponents()
    print("Found strongly connected components!")
    weak = reader.depthFirstSearch(data, False, False).getConnectedComponents()

    quick += ("Connected Components(Task4)         : " + str(len(weak)) + "\n")
    quick += ("Strongly Connected Components(Task5): " + str(len(strong)) + "\n")
    
    f = outputfile
    printAndWrite(out, quick)

    # Print results for Task 4: 
    f.write(printHeader("Task 4: Cleaning Up the Network"))
    comp = 1
    smallcomp = 0
    for component in list(weak):
        if len(component) == 1:
            smallcomp += 1
            continue
        if len(component) > 6:
            st = (printHeader(" COMPONENT " + str(comp), " "))
        else:
            st = "COMPONENT " + str(comp) + ": "

        st += neatlyPrintList(component) + '\n'
        comp += 1

        f.write(st)
    # Print results for Task 5
    if smallcomp >= 1:
        f.write("\n And "+ str(smallcomp) +" single node components")
    
    # Print results for Task 5
    comp = 1 
    smallcomp = 0
    
    f.write(printHeader("Task 5: Closed Subnetworks"))
    for component in list(strong):
        if len(component) == 1:
            smallcomp += 1
            continue
        if len(str(component)) > 80 - len("COMPONENT " + str(comp)):
            st = (printHeader(" COMPONENT " + str(comp), " "))
        else:
            st = "COMPONENT " + str(comp) + ": "
        
        st += neatlyPrintList(component) + '\n'
        comp += 1
        f.write(st)
    
    if smallcomp >= 1:
        f.write("\n"+ str(smallcomp) +" Single Node Components\n")
    print("More detailed results available at ", outputpath)


# Open the output file, and generate graph object
out = open(outputpath, 'w')
dset = Nobjects.Graph(datapath)

# Output header to file
s =  "Drew Balletto\n"
s += "CS 435 - MiniProject\n"
s += "12/19/2018\n"
printAndWrite(out, s)

printAndWrite(out, "Dataset: " + datapath + '\n')

# Task 3
printAndWrite(out, printHeader("TASK 3: Find Influencers"))
Influencers = dset.findInfluencers()
# Influencers = neatlyPrintList(dset.findInfluencers())
out.write(neatlyPrintList(Influencers))
print("Top influencer   :", Influencers[0])
print("Total Influencers:", len(Influencers))
print("List outputted to " + outputpath)

# Task 4/5
tasks4and5(dset, out)

# Task 6
printAndWrite(out, printHeader("TASK 6:Recommendation Engine"))

k = 5
print("Finding a suitable chain of nodes at length " + str(k))
while(True):
    
    #  Pick 2 random nodes in the set and see if there's a chain of length k
    P1 = random.randint(0, len(dset.getNodes()))
    P2 = random.randint(0, len(dset.getNodes()))
    print("Trying:", P1, str(P2) + "...")
    chains = reader.kChain(P1, P2, 5, dset)

    # Cut out all paths smaller than K
    tchains = []
    for chain in chains:
        if len(chain) == k:
            tchains += [chain]
    chains = tchains

    if len(chains) >= 1:
        printAndWrite(out, "\n" + str(len(chains)) + " Chains Found for " + str(P1) +
         " and " + str(P2) +"!"+'\n')
        
        out.write(neatlyPrintList(chains))
        print("Printed to " + outputpath)
        break

out.close()
    