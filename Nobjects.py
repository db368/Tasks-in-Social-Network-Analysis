

class Network:
    ''' A collection stats for a specific node'''
    
    def __init__(self, source, visited = set(), previsit = {}, postvisit = {}):
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

