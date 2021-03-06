import operator
# import networkx as nx

class Results:
    ''' A collection of results for a search in a graph '''
    
    def __init__(self, source = None, visited = set(), previsit = {}, postvisit = {}, weak = [], strong = {}):
        self.source = source       # Root Node
        self.previsit = previsit   # Previsits
        self.postvisit = postvisit # Postvisits
        self.visited = visited     # A set of all visited nodes
        self.strong_components = strong
        self.components = weak
        self.clock = 0

    def addPostVisit(self, node):
        self.postvisit[node] = self.clock
        self.clock += 1

    def addPreVisit(self, node):
        self.previsit[node] = self.clock
        self.clock += 1

    def getPrevisit(self):
        ''' Returns an array of ordered previsit nodes '''
        return self.previsit
    
    def getPostvisit(self):
        ''' Returns an array of ordered postvisit nodes '''
        return self.postvisit

    def getVisited(self):
        return self.visited

    def setStronglyConnectedComponents(self, components):
        self.strong_components = components.copy()

    def getConnectedComponents(self):
        ''' Returns an array of weakly connected components '''
        return self.components

    def getStronglyConnectedComponents(self):
        ''' Returns an array of strongly connected components'''
        return self.strong_components

    def __str__(self):
        return ("Node: " + (str)(self.source) + " Nodes visited: " + (str)(len(self.visited)))
    
    def writeVisits(self, filepath):
        ''' Writes pre/postvisits in a csv format at filepath'''
        f = open(filepath, 'w')
        f.write('NODE, Previsit, Postvisit\n')
        for key in self.previsit:
            f.write(key + ',' + str(self.previsit[key]) + ',' + str(self.postvisit[key]) + '\n')
        f.close

class Graph():

    def __init__(self, input_file = None, edges = [], nodes = []):
        ''' Creates a new graph object from a list of edges and nodes, or a an
            input file of the correct format '''
        if not input_file is None:
            self.pullNodes(input_file)
        else:
            self.edges = edges
            self.nodes = nodes


    def pullNodes(self, f): # For task 2
        """Initializes node set and graph list from an input file"""

        nodes = set()
        edges = []

        # Start off with a quick check to see if the file exists
        try:
            text = open(f)
        except FileNotFoundError:
            print("The requested file could not be found!")
            exit()
            return None
        
        edges = []
        
        # This is a text file
        if f[-3:] == "txt":
            for line in text.read().splitlines():
                
                # Some text files have notes at the top, ignore it if so
                if not line[0].isdigit():
                    continue

                # Split line by whitespace
                l = line.split()

                # Add this to our list as a tuple
                edges.append([int(l[0]), int(l[1])])

        #This is a CSV
        elif f[-3:] == "csv":
            for line in text.read().split():
                edge = []
                
                # Split again by comma and check if this is a header
                l = line.split(",")
                if line[0] is "node_1":
                    continue
                
                # If non-integers are conained in these cells, store them as strings
                try:
                    edge= [int(l[0]), int(l[1])]
                except ValueError:
                    edge = [l[0], l[1]]
                    continue

                #Add this edge to our list as a tuple
                edges.append(edge)

        # Close the textfile and return
        text.close()

        # Populate our list of nodes
        for edge in edges:
            if edge[0] not in nodes:
                nodes.add(edge[0])
            if edge[1] not in nodes:
                nodes.add(edge[1])

        # Save sorted node and edge lists
        self.nodes = sorted(nodes)
        self.edges = sorted(edges, key=operator.itemgetter(1))
        self.edges = sorted(self.edges, key=operator.itemgetter(0))
    
    def nodeDict(self, reversed = False):     
        """ Returns graph as a dictionary, where each key is a node, and its value is a
        list of edges out of it. If Reverse is specified, return a dict of reversed 
        edges GR. """
        
        nodes = {key:[] for key in self.nodes}

        # Allow for a dict of reversed edges
        if reversed:
            edges = self.getReversedEdges().copy()
        else:
            edges = self.edges.copy()

        # Iterate through list of edges
        for edge in edges:
            nodes[edge[0]].append(edge[1])

        return nodes

    
    def findInfluencers(self, foodegree = "in"): # For Task 3
        ''' Returns a list of sorted influencers using the specified degree '''
        
        # Initialize a dictionary from internal list of nodes
        nodes = dict.fromkeys(self.nodes, 0)

        # If we're looking for the in degree, we care about what is being linked to,
        # for out degree we care about what is doing the linking 
        degree = 0
        if foodegree == "in": 
            degree = 1

        # Iterate through list of edges, increment if we're good
        for edge in self.edges:
            nodes[edge[degree]]+=1

        # Sort nodes by 'influencers'
        sortednodes = sorted(nodes.items(), key=operator.itemgetter(1))

        # Calculate how many nodes comprise 3%
        topsize = (int)(0.03*len(nodes))

        # Return top 3% of influencers
        return sortednodes[::-1][0:topsize] 

    def getNodes(self):
        ''' Returns a list of all nodes in the graph '''
        return self.nodes

    def getReversedEdges(self):
        ''' Returns a reversed list of edges GR '''
        
        reversed_edges = []
        for i in range(0, len(self.edges)):
            # Store Edge
            edge = self.edges[i].copy()
            
            # Swap 
            temp = edge[0]
            edge[0] = edge[1]
            edge[1] = temp

            # Append
            reversed_edges.append(edge)
        
        #Sort new list of edges then return
        return sorted(reversed_edges, key=operator.itemgetter(0))
    
    def cleanGraph(self, component):
        ''' Creates a new graph object only conatining nodes and edges present in component '''
       # Sort list of nodes
        newnodes = sorted(component)

        # Only append edges to nodes that exist in newnodes
        newedges = []
        for edge in self.edges:
            if edge[0] in newnodes and edge[1] in newnodes:
                newedges.append(edge)
        return Graph(None, newedges, sorted(newnodes, key=operator.itemgetter(0)))

    # def printEdges(self, filename):
    #     G = nx.convert.from_edgelist(self.edges, nx.MultiDiGraph)
    #     nx.write_pajek(G, filename)