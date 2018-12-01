import reader 
import Nobjects
import operator

# Part 1
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K"]


edges2 = [['A', 'B'], ['B','E'], ['E','A'], ['E','C'], ['C','E']]
edges2+= [['E','F'], ['E','K'], ['C','H'], ['F','H'], ['F','K'], ['K','G']]
edges2+= [['K','I'], ['I','K'], ['K','D'], ['D','I'], ['I','G'], ['G','E']]
edges2+= [['C','A']]

edges2 = sorted(edges2, key=operator.itemgetter(1))
edges2 = sorted(edges2, key=operator.itemgetter(0))

G2 = Nobjects.Graph(None, edges2, nodes)
N = reader.findSinks(G2, True)
print(N)

