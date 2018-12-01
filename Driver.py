import reader 
import Nobjects
import operator

# datapath = "datasets/friendship.txt"
# datapath = "datasets/Wiki-Vote.txt"
# datapath = "datasets/soc-Epinions1.txt"
datapath = "datasets/tvshow_edges.csv"

dset = Nobjects.Graph(datapath)
print(reader.findSinks(dset))