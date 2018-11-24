import operator


class Network:
    ''' A collection stats for a specific node'''
    
    def __init__(self, source = None, visited = set(), previsit = {}, postvisit = {}):
        self.source = source       # Root Node
        self.previsit = previsit   # Previsits
        self.postvisit = postvisit # Postvisits
        self.visited = visited     # A set of all visited nodes
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

    def __str__(self):
        return ("Node: " + (str)(self.source) + " Nodes visited: " + (str)(len(self.visited)))

class Graph():
    def __init__(self, input_file):
        self.pullNodes(input_file)


    def pullNodes(self, f): # For task 2
        """Initializes node set and graph list from an input file"""

        nodes = set()
        edges = []

        # Start off with a quick check to see if the file exists
        try:
            text = open(f)
        except FileNotFoundError:
            print("The requested file could not be found!")
            return None
        
        edges = []
        # The file exists, check to see what type of file it is: print("Filetype is:
        # ", f[-3:])

        # This is a text file
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

        # Populate our list of nodes
        for edge in edges:
            if edge[0] not in nodes:
                nodes.add(edge[0])
            if edge[1] not in nodes:
                nodes.add(edge[1])
        
        self.nodes = nodes
        self.edges = edges
    
    def nodeDict(self):     
        """ Returns graph as a dictionary, where each key is a node, and its value is a
        list of edges out of it """
        
        nodes = {}
        # Iterate through list of edges
        for edge in self.edges:
            # Check to see if if we've recorded this node yet, if not, create a new
            # list
            if not edge[0] in nodes:
                nodes[edge[0]] = [edge[1]]
            else:
                nodes[edge[0]].append(edge[1])


        return nodes

    
    def findInfluencers(self, foodegree): # For Task 3
        ''' returns a list of sorted influencers using the specified degree '''
        
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