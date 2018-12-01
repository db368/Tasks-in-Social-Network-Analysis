import operator
import sys
import Nobjects
import os

debugpath = "crash.txt"

# Define Global Vairables
layer = None
previsit = None
clock = None
postvisit = None
visited = None
prepostvisit = None
G = None
Gr = None


def gracefulFailure(edges, excepted):
    ''' Writes all relevant information to a log file at <datapath>-crash.txt'''
    
    global visited    # A set of all visited nodes
    global layer     # Recursion Depth for Debug Purposes
    global previsit  # The previsit numbers of a all nodes
    global postvisit # The post visit values of all nodes
    global clock     # One clock for both
    global G
    
    print(excepted)
    f = open(debugpath, "w")
    f.write("NODE COUNT: " + str(len(G.keys())) + '\n')
    f.write("LAYER: " + str(layer) + '\n')
    f.write("VISITED: " + str(len(visited)) + '\n' +  str(sorted(visited))+ '\n')
    f.write("POSTVISIT: " + str(len(postvisit)) +  '\n' +  str(postvisit)+ '\n')
    f.write("PREVISIT: " + str(len(previsit)) +  '\n' +  str(previsit)+ '\n')
    f.write("CLOCK:" + str(clock)+ '\n')
    f.write("EDGES IN STACK:" + '\n' + str(edges)+ '\n')
    f.close()
    print("Log file created at:", debugpath)

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

def resetGlobals(graph = None):
    ''' Resets globals to ready for an exploration, optinally can set G 
        as a dictionary from the provided graph '''
    global visited   # A set of all visited nodes
    global layer     # Recursion Depth for Debug Purposes
    global previsit  # The previsit numbers of a all nodes
    global postvisit # The post visit values of all nodes
    global clock     # One clock for both
    global G
    global Gr

    if not graph is None:
        G = graph.nodeDict()
        Gr = graph.nodeDict(True)
    
    previsit = {}
    postvisit = {}
    clock = 0
    visited = set() # Reset visited nodes
    layer = 0 # Reset Recursion Depth

def findSinks(graph, print_state = False):
    ''' Returns all sink nodes  '''
    
    global G
    global Gr
    global prepostvisit
    global postvisit
    global visited
    resetGlobals(graph)
    
    # Manually reset prepost visit
    prepostvisit = {}

    # Reverse G   
    G = graph.nodeDict(True)

    # Initialize sets
    this_run = set()
    sinks = {}
    
    # First, Run through a depth first search and store results
    if print_state:
        print("----Running on Gr---")
    idfs = depthFirstSearch(graph, print_state)
    prepostvisit = idfs.getPrevisit().copy()
    resetGlobals()

    ordered_edges = []

    G = graph.nodeDict()

    # Format list to be as if pulled from nodeDict
    sorted_prepostvisit  = sorted(prepostvisit.items(), key=operator.itemgetter(1))
    for edge in sorted_prepostvisit:
        ordered_edges.append(edge[0])
    
    ordered_edges.reverse()


    if print_state:
        print("Running on G with postordering")

    # DFS through Gr to find highest reverse post number
    for edge in ordered_edges:
        
        # Store previously visited nodes for comparison
        saved_visited = visited.copy()

        # See how many nodes are connected to this 
        if edge not in visited:
            if print_state:
                print("->", edge)
            explore(edge, False, False)

        # Isolate nodes found during last search
        this_run = visited - saved_visited

        # Quick check to see if this yields any connected components
        if len(this_run) < 1:
            continue
        considered_posts = {}


        # Add this node and its post to "considered posts"
        for node in this_run:
            considered_posts[node] = postvisit[node]

        # Sort this and pull the highest post number, which should be our sink
        highest_postvisit = sorted(considered_posts.items(), key=operator.itemgetter(1))

        # Append a 
        sinks[highest_postvisit[-1][0]] = this_run - set([highest_postvisit[-1][0]])

    return sinks

def depthFirstSearch(graph, print_steps = False):
    ''' Perform a Depth First Search on graph. Return a Network Object. '''
    global visited
    resetGlobals()   

    # Create a set of all nodes in G
    unvisited = graph.getNodes()

    # Continue to DFS on next element in stack until all edges are unvisited
    for edge in unvisited:
        if edge not in visited:
                if print_steps:
                    print("->", edge)
                explore(edge, True, print_steps)

    return Nobjects.Network(None, visited, previsit, postvisit)


def explore(v, directed = True, print_steps = False):
    """ Returns nodes connected to N """
    
    # Define Global Variables
    global visited
    global layer
    global G
    global Gr
    global prepostvisit

    # Mark v as visited
    layer = layer + 1
    visited.add(v)
    setPrevisit(v)

    # Add all foward edges
    edges = []
    if v in G:
        edges += G[v]

    # Add reversed edges as well if this is undirected
    if not directed: 
        if v in Gr:
            edges += Gr[v]

    # Iterate through our list of edges, check if we've visited them, if not: explore
    for edge in edges:
        if edge not in visited:
            if print_steps:
                print(str(v), "->", edge)
            try:
                explore(edge, directed, print_steps)
            except (RecursionError, RuntimeError, OverflowError, MemoryError) as exc:
                print("Max recursion reached on node " + str(v))
                gracefulFailure(edges, exc)
                exit()
               
    # Set postvisit, return visited
    layer = layer-1
    setPostvisit(v)
    return visited

# Forgive me.
sys.setrecursionlimit(8192)
