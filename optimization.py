import graph as gp
import evaluating as el

import random
import copy
import math

#H0 = (penalty, naughtyNodes, professorsLectures, gradesLectures)

#S1 = (penalty, naughtyNodes)
#S2 = (penalty, naughtyNodes)
#S3 = (penalty, emptyGradesLectures)
#S4 = (penalty, naughtyNodes, lecturesInDay)
#S5 = (penalty, emptyProfessorsLectures)
#S6 = (penalty, naughtyNodes, numberOfLecturesPerDay)
#S7 = (penalty, naughtyNodes, naughtyProfessorsDays)
#S8 = (penalty, naughtyNodes, twoDaysLectures) ##fix this shit

#---constants---

banLecturesForProfessors = [] #citanje iz fajla
banLecturesForGrades = []

#---------------

changesCounter = 0

def getNodeColour(graph, node):
    return graph.nodes[node]['colour']

def fixRandom(graph, naughtyNodes):
    random.seed()
    node = random.choice(naughtyNodes)

    if node in graph.nodes:
        graph.nodes[node]['colour'] = random.choice(range(gp.NUMBER_OF_COLOURS))
    else:
        print('.')

    return graph

def fixRandomLegal(graph, naughtyNodes, professorsLectures, gradesLectures):
    index = 0

    isFixed = False
    while not isFixed:
        node = naughtyNodes[index]
        
        legalColours = getLegalMoves(node, professorsLectures, gradesLectures)

        if legalColours:
            graph.nodes[node]['colour'] = random.choice(legalColours)
            isFixed = True
        index += 1

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

def getBannedColoursS1(node, bannedLectures):
    bannedColours = []
    for lecture in bannedLectures:
        if lecture[0] == node.proff:
            bannedColours.append(lecture[1])

    return bannedColours

def getBannedColoursS2(node, bannedLectures):
    bannedColours = []
    for lecture in bannedLectures:
        if lecture[0] == node.grade:
            bannedColours.append(lecture[1])

    return bannedColours

def getBannedColoursS4(node, lecturesInDay):
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if (node.proff, node.grade) in lecturesInDay[day]:
                bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY - 1))

    return bannedColours

def getBannedColoursS6(node, numberOfLecturesPerDay):
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if numberOfLecturesPerDay[node.proff][day] >= el.MAX_LECTURES_PER_DAY_FOR_PROF:
                bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY))
    
    return bannedColours

def getBannedColoursS7(node, naughtyProfessorsDays):
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if naughtyProfessorsDays[node.proff][day] >= 0:
            bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY))
    
    return bannedColours

def getBannedColoursS8(node, twoDaysLectures): #moze da gura ista predavanja u jedan dan
    bannedColours = []
    for day in range(gp.WORKING_DAYS):
        if (node.proff, node.grade) in twoDaysLectures[day]:
            bannedColours += list(range(gp.LECTURES_PER_DAY * day, gp.LECTURES_PER_DAY * day + gp.LECTURES_PER_DAY))
    
    return bannedColours

def swappingNodesCondition(graph, node1, node2, professorsLectures, gradesLectures, swappingNodesConditionArguments, bannedColours):
    if ((swappingNodesConditionArguments[0] and accordingToProfessor(graph, node1, node2, professorsLectures)) or (swappingNodesConditionArguments[1] and accordingToGrade(graph, node1, node2, gradesLectures))) and not getNodeColour(graph, node2) in bannedColours:
        return True
    return False

def accordingToProfessor(graph, node1, node2, professorsLectures):
    if node1.grade == node2.grade and not node1.proff == node2.proff:
        if not professorsLectures[node1.proff][getNodeColour(graph, node2)]:
            if not professorsLectures[node2.proff][getNodeColour(graph, node1)]:
                return True
    return False

def accordingToGrade(graph, node1, node2, gradesLectures):
    if node1.proff == node2.proff and not node1.grade == node2.grade:
        if not gradesLectures[node1.grade][getNodeColour(graph, node2)]:
            if not gradesLectures[node2.grade][getNodeColour(graph, node1)]:
                return True
    return False

def getPerfectColours(perfectColours, legalColours):
    pLColours = []
    for colour in range(gp.NUMBER_OF_COLOURS):
        if perfectColours[colour] == 1 and colour in legalColours:
            pLColours.append(colour)

    return pLColours

def fix00(graph, naughtyNodes, professorsLectures, gradesLectures, perfectColours, getBannedColours, getBannedColoursArgumet, swappingNodesConditionArguments):
    if not naughtyNodes:
        return graph
    random.seed()
    node = random.choice(naughtyNodes)

    legalColours = getLegalMoves(node, professorsLectures, gradesLectures)

    perfColoursToUse = [] #neke boje se pojavljuju dvaput
    if swappingNodesConditionArguments[0] == 1:
        perfColoursToUse += getPerfectColours(perfectColours[0][node.grade], legalColours)
    if swappingNodesConditionArguments[1] == 1:
        perfColoursToUse += getPerfectColours(perfectColours[1][node.proff], legalColours)
    if perfColoursToUse:
        graph.nodes[node]['colour'] = random.choice(perfColoursToUse)
 
    else:
        bannedColours = getBannedColours(node, getBannedColoursArgumet)
        colours = [colour for colour in legalColours if colour not in bannedColours]
        if colours:
            graph.nodes[node]['colour'] = random.choice(colours)

        else:
            swapList = []
            for swapNode in graph.nodes:
                if swappingNodesCondition(graph, node, swapNode, professorsLectures, gradesLectures, swappingNodesConditionArguments, bannedColours):
                    swapList.append(swapNode)
            if swapList:
                swapNode = random.choice(swapList)
                tempColour = graph.nodes[node]['colour']
                graph.nodes[node]['colour'] = graph.nodes[swapNode]['colour']
                graph.nodes[swapNode]['colour'] = tempColour

            else:
                fixRandomLegal(graph, naughtyNodes, professorsLectures, gradesLectures)


    return graph

'''
def fix(graph, HardConstraint, SVector): #izbaci sve osim nn
    naughtyNodes = HardConstraint[1] + SVector[0][1] + SVector[1][1] + SVector[3][1]
    
    #fixRandom(graph, naughtyNodes)
    fixRandomLegal(graph, naughtyNodes, HardConstraint)
    return graph
'''

def getArguments(constraint, energy):
    getBannedColours = None
    getBannedColoursArgumet = None
    swappingNodesConditionArguments = None
    if constraint == 1:
        getBannedColours = getBannedColoursS1
        getBannedColoursArgumet = banLecturesForProfessors
        swappingNodesConditionArguments = (1, 0)
    elif constraint == 2:
        getBannedColours = getBannedColoursS2
        getBannedColoursArgumet = banLecturesForGrades
        swappingNodesConditionArguments = (0, 1)
    elif constraint == 4:
        getBannedColours = getBannedColoursS4
        getBannedColoursArgumet = energy[2][3][2]
        swappingNodesConditionArguments = (1, 1)
    elif constraint == 6:
        getBannedColours = getBannedColoursS6
        getBannedColoursArgumet = energy[2][5][2]
        swappingNodesConditionArguments = (1, 0)
    elif constraint == 7:
        getBannedColours = getBannedColoursS7
        getBannedColoursArgumet = energy[2][6][2]
        swappingNodesConditionArguments = (1, 0)
    elif constraint == 8:
        getBannedColours = getBannedColoursS8
        getBannedColoursArgumet = energy[2][7][2]
        swappingNodesConditionArguments = (1, 1)

    arguments = {}
    arguments['getBannedColours'] = getBannedColours
    arguments['getBannedColoursArgumet'] = getBannedColoursArgumet
    arguments['swappingNodesConditionArguments'] = swappingNodesConditionArguments

    return arguments

def annealing(orgGraph, orgEnergy, TEMPERATURE):
    newGraph = copy.deepcopy(orgGraph)

    newEnergy = el.calculateEnergy(newGraph, banLecturesForProfessors, banLecturesForGrades) #zbog adresa node-ova ne budi debil ponovo

    for i in range(int(math.log(TEMPERATURE))):
        random.seed()
        constraint = 0

        while constraint == 0 or constraint == 3 or constraint == 5:
            constraint = random.randint(1, el.NUMBER_OF_SOFT_CONSTRAINTS)

        moreArguments = getArguments(constraint, newEnergy)
        newGraph = fix00(graph = newGraph, naughtyNodes = newEnergy[2][constraint - 1][1], professorsLectures = newEnergy[1][2], gradesLectures = newEnergy[1][3], perfectColours = (newEnergy[2][2][1], newEnergy[2][4][1]), **moreArguments)

        newEnergy = el.calculateEnergy(newGraph, banLecturesForProfessors, banLecturesForGrades)

    deltaEnergy = orgEnergy[0] - newEnergy[0]

    if deltaEnergy > 0:
        return (newGraph, newEnergy, 1, 0)

    elif math.exp(deltaEnergy / TEMPERATURE) >= random.uniform(0, 1):
        return (newGraph, newEnergy, 1, 1)

    else:
        return (orgGraph, orgEnergy, 0, 0)



'''
for i in range(13):
    getMin()
    TEMPERATURE_0 = int(TEMPERATURE_0 * 1.5)
'''

'''
print(Energy[0])


print(Energy[2][3][0])
print(Energy[2][3][1])
print(Energy[2][3][2])


#fix00(graph, Energy[2][7][1], Energy[1][2], Energy[1][3], getBannedColoursS8, Energy)

Energy = el.calculateEnergy(graph, banLecturesForProfessors, banLecturesForGrades)

print(Energy[0])

print(Energy[1][0])

gp.writeGraph(graph, 'testsukurac')
'''
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