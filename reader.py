import operator

# Returns a tuple of [node1, node2] from the location of a textfile
def pullNodes(f):
    # Start off with a quick check to see if the file exists
    try:
        text = open(f)
    except:
        print("Error opening the file!")
        return None

    edges = []
    for line in text.read().split():
        #Split each line by commas
        l = line.split(",")
        edges.append([l[0], l[1]])
    text.close()
    return edges


# Takes in node dataset D and returns a tuple of node types and their influence
def findInfluencers(d):
    nodes ={}
    for edge in d:
        if not edge[0] in nodes:
            nodes[edge[0]]=1
        else:
            nodes[edge[0]]+=1
    sortednodes = sorted(nodes.items(), key=operator.itemgetter(1))
    return sortednodes[::-1][0:3]

dset = pullNodes("/home/drdru/Downloads/facebook_clean_data/public_figure_edges.csv")
print(findInfluencers(dset))
