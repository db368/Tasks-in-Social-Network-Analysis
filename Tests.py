import reader 
import Nobjects
import operator
import unittest

class Test_TestGraphFunctions(unittest.TestCase):

    def test_reverse(self):
        ''' Tests if getting a reversed dictionary has any side effects '''
        # Generate Graph
        nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K"]
        edges2 = [['A', 'B'], ['B','E'], ['E','A'], ['E','C'], ['C','E']]
        edges2+= [['E','F'], ['E','K'], ['C','H'], ['F','H'], ['F','K'], ['K','G']]
        edges2+= [['K','I'], ['I','K'], ['K','D'], ['D','I'], ['I','G'], ['G','E']]
        edges2+= [['C','A']]
        edges2 = sorted(edges2, key=operator.itemgetter(1))
        edges2 = sorted(edges2, key=operator.itemgetter(0))
        G = Nobjects.Graph(None, edges2, nodes)


        # Get a nodedict, a reversed nodeDict, then a normal one
        C = G.nodeDict()
        C2 = G.nodeDict(True)
        C3 = G.nodeDict()
        C4 = G.nodeDict(True)

        #go through key by key and compare
        for key in C3.keys():
            # First check if the key even is in C
            assert key in C

            # Then see if every edge in C exists in C3
            for edge in C[key]:
                assert edge in C3[key]

        #go through key by key and compare
        for key in C4.keys():
            # First check if the key even is in C
            assert key in C2

            # Then see if every edge in C exists in C3
            for edge in C2[key]:
                assert edge in C2[key]
    
    def test_findSinks(self):
        ''' Tests to see if find sinks is working properly '''
        nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K"]
        edges2 = [['A', 'B'], ['B','E'], ['E','A'], ['E','C'], ['C','E']]
        edges2+= [['E','F'], ['E','K'], ['C','H'], ['F','H'], ['F','K'], ['K','G']]
        edges2+= [['K','I'], ['I','K'], ['K','D'], ['D','I'], ['I','G'], ['G','E']]
        edges2+= [['C','A']]
        
        edges2 = sorted(edges2, key=operator.itemgetter(1))
        edges2 = sorted(edges2, key=operator.itemgetter(0))

        G = Nobjects.Graph(None, edges2, nodes)


        read =  reader.stronglyConnectedComponents(G)
        N =  read.getConnectedComponents()
        print(read.getPostvisit())
        assert N[0][0] == 'H'

    def test_chain(self):
        ''' Test if kchain can properly find the test chain in friendship.txt '''

        # Load in friendship.txt, obtain chains from kChain
        #G = Nobjects.Graph("datasets/Testset2.csv")
        #chains = reader.kChain(3, 8, 5, G)
        
        G = Nobjects.Graph("datasets/politician_edges.csv")
        chains = reader.kChain(503, 5065, 5, G)

        # See if our test chain was found
        print(chains)
        assert chains is not None and len(chains) != 0
        
if __name__ == '__main__':
    unittest.main()