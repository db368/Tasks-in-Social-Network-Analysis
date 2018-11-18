import operator
import sys

datapath = "datasets/soc-Epinions1.txt"
isdirected = True

# Returns a list of tuples containing edges in the form [node1,node2]
def pullNodes(f):
    
    # Start off with a quick check to see if the file exists
    try:
        text = open(f)
    except FileNotFoundError:
        print("The requested file could not be found!")
        return None
    
    edges = []
    # The file exists, check to see what type of file it is:
    # print("Filetype is: ", f[-3:])
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


# Takes list of edges d, and whether or not it's directed. If So, return top 3%
# of influencers. A node's rank as an influencer is determined by its 
# _In-Degree_ which is the  number of edges into it. Only relevant in a directed 
# graph

def findInfluencers(d, directed):
    nodes ={}

    #Iterate through list of edges
    for edge in d:
        
        #Check to see if if we've recorded this node yet, if not set it to one,
        # if so increment
        if not edge[0] in nodes:
            nodes[edge[0]]=1
        else:
            nodes[edge[0]]+=1

    # Sort nodes by 'influencers'
    sortednodes = sorted(nodes.items(), key=operator.itemgetter(1))

    # Calculate how many nodes comprise 3%
    topsize = (int)(0.03*len(d))

    # Return top 3% of influencers
    return sortednodes[::-1][0:topsize] 

# Pull nodes from the specified datapath
dset = pullNodes(datapath)

# Quit if dset fails to be created
if dset == None:
    sys.exit()

print(findInfluencers(dset, isdirected))