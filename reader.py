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

def stronglyConnectedComponents(graph, print_state = False):
    ''' Returns all strongly connected components in a directed graph as a
        dictionary of (sink:component)'''
    
    global G
    global Gr
    global prepostvisit
    global postvisit
    global visited
    resetGlobals(graph)
    
    # Manually reset prepost visit and reverse G
    prepostvisit = {}
    G = graph.nodeDict(True)
    ordered_edges = []
    
    # First, Run through a depth first search and store results
    if print_state:
        print("----Running on Gr---")
    idfs = depthFirstSearch(graph, print_state)
    prepostvisit = idfs.getPostvisit().copy()

    # Order nodes by the post visit of the previous search
    sorted_prepostvisit  = sorted(prepostvisit.items(), key=operator.itemgetter(1))
    ordered_edges = [edge[0] for edge in sorted_prepostvisit]
    ordered_edges.reverse()
    
    # Run undirected DFS using post visit ordering
    if print_state:
        print("Running on G with postordering")
    G = graph.nodeDict()

    post_search = depthFirstSearch(graph, print_state, False, ordered_edges)
    return post_search

def depthFirstSearch(graph, print_steps = False, directed = True, order = []):
    ''' Perform a Depth First Search on graph. Returns a Network Object
        complete with previsit, postvisit, and components. If directed
        is set to false, the dfs will treat the graph as undirected. If
        order is specified, the DFS will search through nodes in the 
        specified order, otherwise it will search in alphabetical order.'''
    global postvisit
    global visited
    global G
    if G is None:
        resetGlobals(graph)   
    else:
        resetGlobals()

    # See if order is set, if not grab ordering from the graph   
    if len(order) == 0:
        unvisited = graph.getNodes()
    else:
        unvisited = order

    # Continue to DFS on next element in stack until all edges are unvisited
    components = []
    for edge in unvisited:
        saved_visited = visited.copy()

        # Perform Search
        if edge not in visited:
            if print_steps:
                print("->", edge)
            explore(edge, directed, print_steps)
        else:
            continue
        # Seperate newly found components
        this_run = visited - saved_visited

        # Create a list of tuples (node, post#,  sort by post number, then
        # generate a new list of only nodes and append to components
        considered_posts = []
        for node in this_run:
            considered_posts.append((node, postvisit[node]))
        sorted_pairs = sorted(considered_posts, key=operator.itemgetter(1), reverse=True)
        sorted_nodes = [pair[0] for pair in sorted_pairs]
        components.append(sorted_nodes)

    # Return final product
    return Nobjects.Results(None, visited, previsit, postvisit, components)


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

    # Add all forward edges
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
