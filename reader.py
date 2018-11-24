import operator
import sys

datapath = "datasets/Wiki-Vote.txt"
visited = set()
layer = 0


def pullNodes(f): # For task 2
    """Returns a list of tuples containing edges in the form [node1,node2]"""

    # Start off with a quick check to see if the file exists
    try:
        text = open(f)
    except FileNotFoundError:
        print("The requested file could not be found!")
        return None
    
    edges = []
    # The file exists, check to see what type of file it is: print("Filetype is:
    # ", f[-3:])
    if f[-3:] == "txt":
        for line in text.read().splitlines():
            
            # Some text files have notes at the top, ignore it if so
            if not line[0].isdigit():
                # print("Ignoring ", line)
                continue

            # Split line by whitespace
            l = line.split()

            # Add this to our list as a tuple
            edges.append([l[0], l[1]])

    #This is a CSV
    elif f[-3:] == "csv":
        for line in text.read().split():
            
            # Split again by comma
            l = line.split(",")

            #Add this edge to our list as a tuple
            edges.append([l[0], l[1]])
        
        # Remove the headerline from out list of edges
        edges.pop(0)

    # Close the textfile and return
    text.close()
    return edges


def findInfluencers(d, de): # For Task 3
    """ Takes list of edges d, and whether or not it's directed. If So, return 
    top 3% of influencers. A node's rank as an influencer is determined by its
    _In-Degree_ which is the  number of edges into it. Only relevant in a
    directed graph """

    nodes ={}

    # If we're looking for the in degree, we care about what is being linked to,
    # for out degree we care about what is doing the linking 
    degree = 0
    if de == "in": 
        degree = 1

    #Iterate through list of edges
    for edge in d:
        
        #Check to see if if we've recorded this node yet, if not set it to one,
        # if so increment
        if not edge[degree] in nodes:
            nodes[edge[degree]]=1
        else:
            nodes[edge[degree]]+=1

    # Sort nodes by 'influencers'
    sortednodes = sorted(nodes.items(), key=operator.itemgetter(1))

    # Calculate how many nodes comprise 3%
    topsize = (int)(0.03*len(d))

    # Return top 3% of influencers
    return sortednodes[::-1][0:topsize] 

def nodeDict(d):     
    """ Returns graph as a dictionary, where each key is a node, and its value is a
     list of edges out of it """
    nodes ={}
   
    # Iterate through list of edges
    for edge in d:
        
        # Check to see if if we've recorded this node yet, if not, create a new
        # list
        if not edge[0] in nodes:
            nodes[edge[0]] = [edge[1]]
        else:
            nodes[edge[0]].append(edge[1])

    return nodes


def beginExploration(n):
    """ Takes in a Node n, then returns all connected nodes """
    global visited # A set of all visited nodes
    global layer   # Recursion Depth for Debug Purposes

    visited = set() # Reset visited nodes
    layer = 0 # Reset Recursion Depth

    return explore(n)

def explore(v):

    """ Returns nodes connected to N """
    # Define Global Variables
    global visited
    global layer
    global G

    # Mark v as visited   
    layer = layer + 1
    visited.add(v)

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

# Pull nodes from the specified datapath
dset = pullNodes(datapath)

# Quit if dset fails to be created
if dset == None:
    sys.exit()

# Generate a dictionary of Nodes for fast access, then generate a list of
# influencers
G = nodeDict(dset)
influencers = findInfluencers(dset, "in")

# Explore all nodes connected to the biggest influencer
network = beginExploration(influencers[0][0])
print("VISITED NODES", network)