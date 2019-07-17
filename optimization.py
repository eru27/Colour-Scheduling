import graph as gp
import evaluating as el

import random
import copy
import math

#H0 = (penalty, naughtyNodes, professorsLectures, gradesLectures)

#S1 = (penalty, naughtyNodes)
#S2 = (penalty, naughtyNodes)
#S3 = (penalty, emptyLectures)
#S4 = (penalty, naughtyNodes, lecturesInDay)
#S5 = (penalty, emptyLectures)
#S6 = (penalty, numberOfLecturesPerDay)
#S7 = (penalty, naughtyProfessorsDays)
#S8 = (penalty, twoDaysLectures)

#---constants---

TEMPERATURE = 10000
STEP = 0.98

banLecturesForProfessors = [(0, 0)] #citanje iz fajla
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

def getLegalMoves(node, professorsLectures, gradesLectures):
    legalMoves = []
    for colour in range(gp.NUMBER_OF_COLOURS):
        if professorsLectures[node.proff][colour] == 0 and gradesLectures[node.grade][colour] == 0:
            legalMoves.append(colour)
        
    return legalMoves

def getBannedColoursH0(graph, node, naughtyNodes):
    bannedColours = []
    for badNode in naughtyNodes:
        if badNode.proff == node.proff and badNode.grade == node.grade:
            bannedColours.append(graph.nodes[badNode]['colour'])

    return bannedColours

def getBannedColoursS12(nodeAtribute, bannedLectures):
    bannedColours = []
    for lecture in bannedLectures:
        if lecture[0] == nodeAtribute:
            bannedColours.append(lecture[1])

    return bannedColours

def getBannedColoursS4(graph, node, lecturesInDay):
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if (node.proff, node.grade) in lecturesInDay[day]:
                bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY - 1))

    return bannedColours

def getBannedColoursS6(graph, node, numberOfLecturesPerDay):
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if numberOfLecturesPerDay[node.proff][day] >= el.MAX_LECTURES_PER_DAY_FOR_PROF:
                bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY - 1))
    
    return bannedColours

def getBannedColoursS7(node, naughtyProfessorsDays):
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if naughtyProfessorsDays[node.proff][day] > 0:
            bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY - 1))
    
    return bannedColours

def getBannedColoursS8(node, twoDaysLectures):
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if (node.proff, node.grade) in twoDaysLectures[day]:
            bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY - 1))
    
    return bannedColours

def fixH0(graph, H0):
    naughtyNodes = H0[1]
    professorsLectures = H0[2]
    gradesLectures = H0[3]

    random.seed()
    node = random.choice(naughtyNodes)
    bannedColours = []
    for badNode in naughtyNodes:
        if badNode.proff == node.proff and badNode.grade == node.grade:
            bannedColours.append(graph.nodes[badNode]['colour'])

    colours = getLegalMoves(node, professorsLectures, gradesLectures)

    if colours:
        graph.nodes[node]['colour'] = random.choice(colours)
    else:
        swapList = []
        for swapNode in graph.nodes:
            if ((node.proff == swapNode.proff and not node.grade == swapNode.grade) or (node.grade == swapNode.grade and not node.proff == swapNode.proff)) and graph.nodes[swapNode]['colour'] not in bannedColours:
                swapList.append(swapNode)
        if swapList:
            swapNode = random.choice(swapList)
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[swapNode]['colour']
            graph.nodes[swapNode]['colour'] = tempColour
        else:
            print('jebi se0')

    return graph

def fixS1(graph, H0, S1):
    naughtyNodes = S1[1]
    professorsLectures = H0[2]
    gradesLectures = H0[3]

    random.seed()
    node = random.choice(naughtyNodes)
    bannedColours = []
    colours = getLegalMoves(node, professorsLectures, gradesLectures)
    for lecture in banLecturesForProfessors:
        if lecture[0] == node.proff:
            bannedColours.append(lecture[1])
            if lecture[1] in colours:
                colours.remove(lecture[1])

    if colours:
        graph.nodes[node]['colour'] = random.choice(colours)
    else:
        swapList = []
        for swapNode in graph.nodes:
            if node.grade == swapNode.grade and not node.proff == swapNode.proff and not graph.nodes[swapNode]['colour'] in bannedColours: #Assuming this schedule is already legal. Keep the grade and make proff free
                swapList.append(swapNode)
        if swapList:
            swapNode = random.choice(swapList)
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[swapNode]['colour']
            graph.nodes[swapNode]['colour'] = tempColour
        else:
            print('jebi se1')

    return graph

def fixS2(graph, S2):
    
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

def swappingNodeCondition():
    return True

def fix00(graph, naughtyNodes, professorsLectures, gradesLectures, getBannedColours):
    random.seed()
    node = random.choice(naughtyNodes)

    legalColours = getLegalMoves(node, professorsLectures, gradesLectures)
    bannedColours = getBannedColours(graph, node, naughtyNodes)
    colours = [colour for colour in legalColours if colour not in bannedColours]

    if colours:
        graph.nodes[node]['colour'] = random.choice(colours)
    else:
        swapList = []
        for swapNode in graph.nodes:
            if swappingNodeCondition():
                swapList.append(swapNode)
        if swapList:
            swapNode = random.choice(swapList)
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[swapNode]['colour']
            graph.nodes[swapNode]['colour'] = tempColour
        else:
            print('jebi se')

    return graph

def fix(graph, HardConstraint, SVector): #izbaci sve osim nn
    naughtyNodes = HardConstraint[1] + SVector[0][1] + SVector[1][1] + SVector[3][1]
    
    #fixRandom(graph, naughtyNodes)
    fixRandomLegal(graph, naughtyNodes, HardConstraint)
    return graph
    
def annealing(orgGraph, orgEnergy):
    newGraph = copy.deepcopy(graph)

    energy = el.calculateEnergy(newGraph, banLecturesForProfessors, banLecturesForGrades)
    fix(newGraph, energy[1], energy[2])

    newEnergy = el.calculateEnergy(newGraph, banLecturesForProfessors, banLecturesForGrades)

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

nodes = list(graph.nodes)

graph.nodes[nodes[0]]['colour'] = 6

gp.writeGraph(graph, 'testorgsukurac')

Energy = el.calculateEnergy(graph, banLecturesForProfessors, banLecturesForGrades)

print(Energy[0])

while Energy[1][1]:
    fix00(graph, Energy[1][1], Energy[1][2], Energy[1][3], getBannedColoursH0)

    Energy = el.calculateEnergy(graph, banLecturesForProfessors, banLecturesForGrades)

    print(Energy[0])

gp.writeGraph(graph, 'testsukurac')
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

        Energy = el.calculateEnergy(graph, banLecturesForProfessors, banLecturesForGrades)

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