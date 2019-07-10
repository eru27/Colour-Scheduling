import networkx as nx

IDFK_counter = 0

NUMBER_OF_COLOURS = 40 #Number of lectures slots

SOURCE = 'sources/legithehe.csv'
OUT = 'out/first.csv'

class Node:
    def __init__(self, proff = -1, clas = -1):
        'Creates node with def: proff = -1, clas = -1'
        self.proff = proff
        self.clas = clas
    
    def printNode(self):
        'Prints node as "proff,clas"'
        print(str(self.proff) + ',' + str(self.clas))


def initGraph(nodes):
    'Creates graph with Node as nodes and connects two nodes that have same .proff or .clas'
    graph = nx.Graph()
    graph.add_nodes_from(nodes) #Adds all Nodes form the list

    for i, node_1 in enumerate(nodes):
        for j, node_2 in enumerate(nodes[i + 1:]): #Checks for every node and every node that is after it in the list
            if node_1.proff == node_2.proff or node_1.clas == node_2.clas:
                graph.add_edge(nodes[i], nodes[i + j + 1])

    return graph

def colourGraph(graph):
    'Colours graph with greedy algorith first colouring nodes with highest degree'
    global IDFK_counter #Does nothing
    maxColour = 0 #Number of lecture slots used
    sortedNodes = sorted(list(graph.nodes()), key = lambda node: graph.degree[node], reverse = True) #Makes list of nodes sorted by node's degree 
        #with first having the highest degree
    for node in sortedNodes:
        listOfUsedColours = [0] * NUMBER_OF_COLOURS
        for neighbour in list(graph.adj[node]):
            try: #If != None doesn't work ig
                listOfUsedColours[graph.nodes[neighbour]['colour']] = 1 #Sets 1 in the listOUC for the colour neighbour is coloured
            except:
                IDFK_counter = IDFK_counter + 1 #Stil doesn't do anything
        colour = 0
        while listOfUsedColours[colour]: #Finding the first available colour ########Got to write exeption
            colour = colour + 1
        if colour > maxColour: #Checks if new lecture slot is being used
            maxColour = colour
        graph.nodes[node]['colour'] = colour
    print(maxColour)
    
    return graph

def loadNodes(fileName):
    'Loads nodes form csv file with rows being proffesors and values being classes'
    f = open(fileName, 'r')
    nodes = []
    for proff, line in enumerate(f.readlines()):
        classes = line[1:].split(',') #first value in a row is filler for writing ','
        for clas in classes:
            nodes.append(Node(proff, int(clas)))
    f.close()

    return nodes

def writeGraph(graph, fileName):
    'Writes graph in file by nodes as proff,class,colour'
    f = open(fileName, 'w')
    for node in list(graph.nodes):
        f.write(str(node.proff) + ',' + str(node.clas) + ',' + str(graph.nodes[node]['colour']) + '\n')
    f.close()

'''
nodes = loadNodes(SOURCE)

g = initGraph(nodes)

print(g.number_of_edges())
print(g.number_of_nodes())

g = colourGraph(g)

writeGraph(g, OUT)
'''