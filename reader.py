import operator
import sys
import Nobjects

datapath = "datasets/Wiki-Vote.txt"
visited = set()
layer = 0

layer = None
previsit = None
clock = None
postvisit = None
visited = None

def setPrevisit(node):
    ''' Sets the previsit value for the specified node during a traversal '''
    global previsit
    global clock
    previsit[node] = clock
    clock += 1 

def setPostvisit(node):
    ''' Sets the postvisit value for the specified node during a traversal '''
    global postvisit
    global clock
    postvisit[node] = clock
    clock += 1 


def depthFirstSearch(graph):
    ''' Perform a Depth First Search on G '''
    global visited    # A set of all visited nodes
    global layer     # Recursion Depth for Debug Purposes
    global previsit  # The previsit numbers of a all nodes
    global postvisit # The post visit values of all nodes
    global clock     # One clock for both    

    previsit = {}; postvisit = {}
    clock = 0
    visited = set() # Reset visited nodes
    layer = 0 # Reset Recursion Depth
    
    # Create a set of all nodes in G
    unvisited = set(graph.getNodes())

    # Continue to DFS on arbitrary element until all elements are visited   
    while len(unvisited) > 0 :
        unvisited -= visited
        explore(unvisited.pop())
    

    return Nobjects.Network(None, visited, previsit, postvisit)



def beginExploration(n):
    """ Takes in a Node n, then returns all connected nodes """
   
    global visited    # A set of all visited nodes
    global layer     # Recursion Depth for Debug Purposes
    global previsit  # The previsit numbers of a all nodes
    global postvisit # The post visit values of all nodes
    global clock     # One clock for both    

    previsit = {}; postvisit = {}
    clock = 0
    visited = set() # Reset visited nodes
    layer = 0 # Reset Recursion Depth
    
    # Explore the given node
    explore(n)

    C = Nobjects.Network(n, visited, previsit, postvisit)
    return C

def explore(v):
    """ Returns nodes connected to N """
    # Define Global Variables
    global visited
    global layer
    global G

    # Mark v as visited   
    layer = layer + 1
    visited.add(v)
    setPrevisit(int(v))
    # Quick check to see if this node exists in our dictionary
    if v not in G or G[v] is None:
        return
    
    # Iterate through all edges of v
    for edge in G[v]:

        # Check to see if we've already visited v , or if it even has any edges
        # out of it 
        if edge not in visited and edge in G:
                
                #It has edges, go one layer deeper
               explore(edge)

    layer = layer-1
    setPostvisit(int(v))
    # Return visited edges
    return visited

def cleanNetwork(d): # Task 4
    '''Report nodes that are either disconnected, or only have some connections
    to each other. '''
    # Depth first search can be used to check if a graph is connected
    
    # Two nodes u and v of a directed graph are connected if there is a path
    # from u to v and a path from v to u
    
    # The node that receives the highest post number in a depth-first search
    # must lie in a source strongly connected component
    return None


dset = Nobjects.Graph(datapath)

if dset == None:
    sys.exit()

# Generate a dictionary of Nodes for fast access, then generate a list of
# influencers
G = dset.nodeDict()
influencers = dset.findInfluencers("out")

# Explore all nodes connected to the biggest influencer
network = depthFirstSearch(dset)
print(network)
print(network.getPrevisit())