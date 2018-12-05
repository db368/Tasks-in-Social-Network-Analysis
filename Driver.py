import reader 
import Nobjects
import operator

# datapath = "datasets/friendship.txt"
# datapath = "datasets/tvshow_edges.csv"
datapath = "datasets/Wiki-Vote.txt"
# datapath = "datasets/soc-Epinions1.txt" 

dset = Nobjects.Graph(datapath)
strong = reader.stronglyConnectedComponents(dset).getConnectedComponents()
weak = reader.depthFirstSearch(dset, False, False).getConnectedComponents()

print(weak)


f = open("Output.txt", 'w')
print("Components: " + str(len(weak)))
for component in list(weak):
    st = "NODES: "
    for node in component:
        st += str(node)
        if node != component[-1]:
            st += ", "
    st += "\n ------------------------\n\n"
    f.write(st)

f.close()