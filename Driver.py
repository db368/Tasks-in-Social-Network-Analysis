import reader 
import Nobjects
import operator

# datapath = "datasets/friendship.txt"
datapath = "datasets/Wiki-Vote.txt"
# datapath = "datasets/soc-Epinions1.txt"
# datapath = "datasets/tvshow_edges.csv"

dset = Nobjects.Graph(datapath)
S = reader.findSinks(dset)
print(S)

f = open("Output of thing.txt", 'w')
for key in list(S.keys()):
    st = "SINK: " + str(key) + '\n'
    st += "NODES: "
    nodes = list(S[key])
    for node in nodes:
        st += str(node)
        if node != nodes[-1]:
            st += ", "
    st += "\n ------------------------\n\n"
    f.write(st)

f.close()