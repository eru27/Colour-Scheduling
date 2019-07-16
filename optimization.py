import graph as gp
import evaluating as el

import random
import copy
import math

#H0 = (penalty, naughtyNodes, proffesorsLectures, gradesLectures)

#S1 = (penalty, naughtyNodes)
#S2 = (penalty, naughtyNodes)
#S3 = (penalty, emptyLectures)
#S4 = (penalty, naughtyNodes, lecturesInDay)
#S5 = (penalty, emptyLectures)
#S6 = (penalty, numberOfLecturesPerDay)
#S7 = (penalty, naughtyProffesorsDays)
#S8 = (penalty, twoDaysLectures)

#---constants---

TEMPERATURE = 10000
STEP = 0.98

banLecturesForProffesors = [(0, 0)] #citanje iz fajla
banLecturesForGrades = [(0, 0)]

#---------------

changesCounter = 0

def fixRandom(graph, naughtyNodes):
    random.seed()
    node = random.choice(naughtyNodes)

    if node in graph.nodes:
        graph.nodes[node]['colour'] = random.choice(range(gp.NUMBER_OF_COLOURS))
    else:
        print('.')

    return graph

def fixRandomLegal(graph, naughtyNodes, H0):
    random.seed()

    isFixed = False
    while not isFixed:
        node = random.choice(naughtyNodes)
        
        legalColours = []
        for colour in range(gp.NUMBER_OF_COLOURS):
            if H0[2][node.proff][colour] == 0 and H0[3][node.grade][colour] == 0:
                legalColours.append(colour)

        if node in graph.nodes:
            if legalColours:
                graph.nodes[node]['colour'] = random.choice(legalColours)
                isFixed = True
        else:
            print('.')

    return graph

def getLegalMoves(node, proffesorsLectures, gradesLectures):
    legalMoves = []
    for colour in range(gp.NUMBER_OF_COLOURS):
        if proffesorsLectures[node.proff][colour] == 0 and gradesLectures[node.grade][colour] == 0:
            legalMoves.append(colour)
        
    return legalMoves

def isThisMoveLegal(graph, node1, node2, proffesorsLectures, gradesLectures):
    if node1.proff == node2.proff and gradesLectures[node1.grade][graph.nodes[node2]['colour']] == 0 and gradesLectures[node2.grade][graph.nodes[node1]['colour']]:
        return True
    if node1.grade == node2.grade and proffesorsLectures[node1.proff][graph.nodes[node2]['colour']] == 0 and proffesorsLectures[node2.proff][graph.nodes[node1]['colour']]:
        return True
    print(node2.proff, node2.grade)
    return False

def fixH0(graph, H0):
    naughtyNodes = H0[1]
    proffesorsLectures = H0[2]
    gradesLectures = H0[3]

    random.seed()
    node = random.choice(naughtyNodes)
    
    colours = getLegalMoves(node, proffesorsLectures, gradesLectures)

    if colours:
        graph.nodes[node]['colour'] = random.choice(colours)
    else:
        isFixed = False
        while not isFixed:
            swapNode = random.choice(list(graph.nodes))
            if isThisMoveLegal(graph, node, swapNode, proffesorsLectures, gradesLectures):
                tempColour = graph.nodes[node]['colour']
                graph.nodes[node]['colour'] = graph.nodes[swapNode]['colour']
                graph.nodes[swapNode]['colour'] = tempColour
                isFixed = True

    return graph

def fixS1(graph, H0, S1):
    naughtyNodes = S1[1]
    proffesorsLectures = H0[2]
    gradesLectures = H0[3]

    random.seed()
    node = random.choice(naughtyNodes)

    colours = getLegalMoves(node, proffesorsLectures, gradesLectures)

    for lecture in banLecturesForProffesors:
        if lecture[0] == node.proff:
            if lecture[1] in colours:
                colours.remove(lecture[1])

    if colours:
        graph.nodes[node]['colour'] = random.choice(colours)
    else:
        swapList = []
        for swapNode in graph.nodes:
            if isThisMoveLegal(graph, node, swapNode, proffesorsLectures, gradesLectures):
                swapList.append(swapNode)
        if swapList:
            swapNode = random.choice(swapList)
            swapNode.printNode()
            node.printNode()
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[swapNode]['colour']
            graph.nodes[swapNode]['colour'] = tempColour
        else:
            print('jebi se')

    return graph

def fixS2(graph, S2):
    naughtyNodes = S2[1]

    random.seed()
    node = random.choice(naughtyNodes)

    isFixed = False

    while not isFixed: ######### log inf loop
        nodeToSwap = random.choice(list(graph.nodes))
        if not((nodeToSwap in naughtyNodes) and (nodeToSwap.grade is not node.grade)):
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[nodeToSwap]['colour']
            graph.nodes[nodeToSwap]['colour'] = tempColour
            isFixed = True

    return graph

def fixS3(graph, S3): #for now we pray
    return graph

def fixS4(graph, S4):
    naughtyNodes = S4[2]

    random.seed()
    node = random.choice(naughtyNodes)

    isFixed = False

    while not isFixed: ######### log inf loop
        nodeToSwap = random.choice(list(graph.nodes))
        if (graph.nodes[nodeToSwap]['colour'] // gp.LECTURES_PER_DAY) is not (graph.nodes[node]['colour'] // gp.LECTURES_PER_DAY):
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[nodeToSwap]['colour']
            graph.nodes[nodeToSwap]['colour'] = tempColour
            isFixed = True

    return graph

def fixS5(graph, S5):
    return graph

def fixS6(graph, S6):
    return graph

def fixS7(graph, S7):
    return graph

def fixS8(graph, S8):
    return graph

def fix(graph, HardConstraint, SVector): #izbaci sve osim nn
    naughtyNodes = HardConstraint[1] + SVector[0][1] + SVector[1][1] + SVector[3][1]
    
    #fixRandom(graph, naughtyNodes)
    fixRandomLegal(graph, naughtyNodes, HardConstraint)
    return graph
    
def annealing(orgGraph, orgEnergy):
    newGraph = copy.deepcopy(graph)

    energy = el.calculateEnergy(newGraph, banLecturesForProffesors, banLecturesForGrades)
    fix(newGraph, energy[1], energy[2])

    newEnergy = el.calculateEnergy(newGraph, banLecturesForProffesors, banLecturesForGrades)

    deltaEnergy = Energy[0] - newEnergy[0]

    random.seed()
    global changesCounter
    if deltaEnergy > 0:
        
        changesCounter += 1
        return (newGraph, newEnergy)
    elif math.exp(deltaEnergy / TEMPERATURE) >= random.uniform(0, 1):
        changesCounter += 1
        return (newGraph, newEnergy)
    else:
        return (graph, newEnergy)

graph = gp.getGraph()

gp.writeGraph(graph, 'orgsukurac')

Energy = el.calculateEnergy(graph, banLecturesForProffesors, banLecturesForGrades)

print(Energy[0])

fixS1(graph, Energy[1], Energy[2][0])

Energy = el.calculateEnergy(graph, banLecturesForProffesors, banLecturesForGrades)

print(Energy[0])

gp.writeGraph(graph, 'sukurac')
'''
generation = 0

t = TEMPERATURE

avgE = []

maxE = Energy[0]
bestGraph = graph

while generation < 100000:
    new = annealing(graph, Energy)
    graph = new[0]
    Energy = new[1]
    if Energy[0] > maxE:
        maxE = Energy[0]
        bestGraph = graph
    generation += 1
    if generation % 1000 == 0 or t == 1:
        t = TEMPERATURE
        TEMPERATURE *= 0.7
        print()
        print(generation)
        print(Energy[0])
        avgE.append(Energy[0])
        print(sum(avgE) / len(avgE))
    else:
        t = int(t * STEP)

print(changesCounter)
gp.writeGraph(graph, 'outof/bestkurcina01')
'''
'''
Im18 = 0

for i in range(20):
        print()
        graph = gp.getGraph()

        Energy = el.calculateEnergy(graph, banLecturesForProffesors, banLecturesForGrades)

        generation = 0

        t = TEMPERATURE

        while t > 1:
            new = annealing(graph, Energy)
            graph = new[0]
            Energy = new[1]
            generation += 1
            t = int(t * STEP)

        print(generation)
        print(Energy[0])
        print(len(Energy[1][1]))
        if len(Energy[1][1]) == 0:
            Im18 += 1

        for n in Energy[1]:
            print(n.gp.printNode())
            print(graph.nodes[n]['colour'])


        gp.writeGraph(graph, 'outof/kurcina' + str(i))
'''
'''
print()
print()
print(Im18 / 20)
'''