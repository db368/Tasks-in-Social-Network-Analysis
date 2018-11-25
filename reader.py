import operator
import sys
import Nobjects

datapath = "datasets/Wiki-Vote.txt"
#datapath = "datasets/soc-Epinions1.txt"

visited = set()
layer = 0

# Define Global Vairables
layer = None
previsit = None
clock = None
postvisit = None
visited = None
prepostvisit = None

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

def resetGlobals():
    ''' Resets globals to ready for an exploration '''
    global visited    # A set of all visited nodes
    global layer     # Recursion Depth for Debug Purposes
    global previsit  # The previsit numbers of a all nodes
    global postvisit # The post visit values of all nodes
    global clock     # One clock for both


    previsit = {}
    postvisit = {}
    clock = 0
    visited = set() # Reset visited nodes
    layer = 0 # Reset Recursion Depth


def directedConnectedness(graph):
    ''' Returns all strongly connected components of a given node '''
    
    global G
    global prepostvisit
    global postvisit
    global visited
    resetGlobals()
    
    # Manually reset prepost visit
    prepostvisit = {}
    
    G = graph.nodeDict(True)

    # Initialize sets
    this_run = set()
    sinks = []
    
    # First, Run through a depth first search and store results
    idfs = depthFirstSearch(graph)
    prepostvisit = idfs.getPrevisit().copy()
    resetGlobals()

    ordered_edges = []
    # Format list to be as if pulled from nodeDict
    sorted_prepostvisit  = sorted(prepostvisit.items(), key=operator.itemgetter(1))
    for edge in sorted_prepostvisit:
        ordered_edges.append(str(edge[0]))
    
    ordered_edges.reverse()
    # print(ordered_edges)

    # Set G back to the unreversed graph
    G = graph.nodeDict()

    # DFS through Gr to find highest reverse post number
    for edge in ordered_edges:

        # Save visited before the search
        saved_visited = visited.copy()

        if edge not in visited:
            explore(edge)

        # Find out which nodes were discovered in this component, store them
        # and their post visits in a considered posts
        this_run = visited-saved_visited
        
        # Quick check to see if this yields any connected components
        if len(this_run) < 1:
            continue
        considered_posts = {}

        # And a check here to see if this node even got a post visit
        for node in this_run:
            considered_posts[int(node)] = postvisit[int(node)]


        # Sort this and pull the highest post number, which should be our sink
        highest_postvisit = sorted(considered_posts.items(), key=operator.itemgetter(1))

        # Append a tuple of (node, size of component)
        sinks.append((highest_postvisit[-1][0], len(considered_posts)))

    return sinks

def depthFirstSearch(graph):
    ''' Perform a Depth First Search on G '''
    global visited
    resetGlobals()   
    
    # Create a set of all nodes in G
    unvisited = graph.getNodes()

    # Continue to DFS on arbitrary element until all elements are visited   
    for edge in unvisited:
        if edge not in visited:
            explore(edge)
    
    return Nobjects.Network(None, visited, previsit, postvisit)



def beginExploration(n):
    """ Takes in a Node n, then returns all connected nodes """
    
    resetGlobals()
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
    global prepostvisit

    # Mark v as visited   
    layer = layer + 1
    visited.add(v)
    setPrevisit(int(v))

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


# Generate a graph from our specified Text file
dset = Nobjects.Graph(datapath)

# Store the dictionary representation of our graph globally
G = dset.nodeDict()
influencers = dset.findInfluencers("out")

# Gather a list of sinks in this graph
sinks = directedConnectedness(dset)
print(sinks)
print("SINKS: ", len(sinks))


#dset.printEdges("T2.net")