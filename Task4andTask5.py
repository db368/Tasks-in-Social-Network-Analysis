import reader 
import Nobjects
import operator



outputpath = "Output.txt"
datapath = "datasets/Wiki-Vote.txt" # Directed, good demonstration set
# datapath = "datasets/Email-Enron.txt" # Undirected, but very large

print("Executing on ", datapath)

# Generate our graph object from datapath
dset = Nobjects.Graph(datapath)
# dset.printEdges("datasets/" + datapath.split("datasets/")[1].split(".")[0] + ".net")

# Calcuate Strongly connected components
strong = reader.stronglyConnectedComponents(dset).getConnectedComponents()

# Calculate Weakly Connected Components
weak = reader.depthFirstSearch(dset, False, False).getConnectedComponents()

# Quickly print network stats
quick =  ("---- Quick Network Stats----\n")
quick += ("Total Nodes                  : "+ str(len(dset.getNodes())) + "\n")
quick += ("Total Edges                  : "+ str(len(dset.getReversedEdges())) +"\n")
quick += ("Connected Components         : " + str(len(weak)) + "\n")
quick += ("Strongly Connected Components: " + str(len(strong)) + "\n")
f = open(outputpath, 'w')
f.write(quick)
print(quick)

# Print results for Task 4: 
f.write("\n--- Weak Components ---\n")
comp = 1
for component in list(weak):
    st = (" COMPONENT " + str(comp) + ':\n')
    comp +=1 
    breakline = 0
    for node in component:
        st += str(node)
        if node != component[-1]:
            st += ", "
        if breakline is 10:
            st += "\n"
            breakline = 0
        else: 
            breakline += 1
    st += "\n------------------------\n"
    f.write(st)

# Print results for Task 5
f.write("\n--- Strongly Connected Components ---\n")
comp = 1
for component in list(strong):
    st = (" COMPONENT " + str(comp) + ':\n')
    comp +=1 
    breakline = 0
    for node in component:
        st += str(node)
        if node != component[-1]:
            st += ", "
        if breakline is 10:
            st += "\n"
            breakline = 0
        else: 
            breakline += 1
    st += "\n ------------------------\n"
    f.write(st)
f.close()

print("More detailed results available at ", outputpath)