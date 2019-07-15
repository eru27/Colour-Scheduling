import graph as gp
import evaluating as el

import random

TEMPERATURE = 1000
STEP = 50

banLecturesForProffesors = [(0, 0)]
banLecturesForGrades = [(0, 0)]

#H0 = (penalty, proffesorsLectures, gradesLectures, naughtyNodes)
#H1 = (penalty, naughtyNodes)
#H2 = (penalty, naughtyNodes)
#H3 = (penalty, emptyLectures)
#H4 = (penalty, lecturesInDay, naughtyNodes)

#S1(-1) = (penalty, emptyLectures)
#S2(-1) = (penalty, numberOfLecturesPerDay)
#S3(-1) = (penalty, naughtyProffesorsDays)
#S4(-1) = (penalty, twoDaysLectures)

#svi cvorovi se popravljaju pazeci na dati uslov

def fixH0(graph, H0): ###bez obzira na ban listu ######random?????
    proffesorsLectures = H0[1]
    gradesLectures = H0[2]
    naughtyNodes = H0[3]
    random.seed()
    node = random.choices(naughtyNodes)
    
    isFixed = False
    currentColour = 0
    while not isFixed:
        if proffesorsLectures[node.proff][currentColour] == 0 and gradesLectures[node.grade][currentColour] == 0:
            graph.nodes[node]['colour'] = currentColour
            isFixed = True
        else:
            currentColour += 1
    
    if not isFixed:
        while not isFixed:
            newColour = random.randrange(gp.NUMBER_OF_COLOURS)
            if newColour is not graph.nodes[node]['colour']:
                graph.nodes[node]['colour'] = newColour
                isFixed = True

    return graph

def fixH1(graph, H1):
    naughtyNodes = H1[1]
    
    random.seed()
    node = random.choices(naughtyNodes)

    isFixed = False

    while not isFixed: ######### log inf loop
        nodeToSwap = random.choices(list(graph.nodes))
        if not ((nodeToSwap in naughtyNodes) and (nodeToSwap.proff is not node.proff)):
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[nodeToSwap]['colour']
            graph.nodes[node]['colour'] = tempColour
            isFixed = True

    return graph

def fixH2(graph, H2):
    naughtyNodes = H2[1]

    random.seed()
    node = random.choices(naughtyNodes)

    isFixed = False

    while not isFixed: ######### log inf loop
        nodeToSwap = random.choices(list(graph.nodes))
        if not((nodeToSwap in naughtyNodes) and (nodeToSwap.grade is not node.grade)):
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[nodeToSwap]['colour']
            graph.nodes[nodeToSwap]['colour'] = tempColour
            isFixed = True

    return graph

def fixH3(graph, H3): #for now we pray
    return graph

def fixH4(graph, H4):
    naughtyNodes = H4[2]

    random.seed()
    node = random.choices(naughtyNodes)

    isFixed = False

    while not isFixed: ######### log inf loop
        nodeToSwap = random.choices(list(graph.nodes))
        if (graph.nodes[nodeToSwap]['colour'] // gp.LECTURES_PER_DAY) is not (graph.nodes[node]['colour'] // gp.LECTURES_PER_DAY):
            tempColour = graph.nodes[node]['colour']
            graph.nodes[node]['colour'] = graph.nodes[nodeToSwap]['colour']
            graph.nodes[nodeToSwap]['colour'] = tempColour
            isFixed = True

    return graph

def fixS1(graph, S1):
    return graph

def fixS2(graph, S2):
    

    return graph

def fixS3(graph, S3):
    return graph

def fixS4(graph, S4):
    return graph

def fix(graph, HVector, SVector):
    maxH = 0
    for H in HVector:
        if H[0] > maxH:
            maxH = H[0]
    if HVector[0][0] == maxH:
        fixH0(graph, HVector[0])
    elif HVector[1][0] == maxH:
        fixH1(graph, HVector[1])
    elif HVector[2][0] == maxH:
        fixH2(graph, HVector[2])
    elif HVector[3][0] == maxH:
        fixH3(graph, HVector[3])
    elif HVector[4][0] == maxH:
        fixH4(graph, HVector[4])
    
    maxS = 0
    for S in SVector:
        if S[0] > maxS:
            maxS = S[0]
    if SVector[0][0] == maxS:
        fixS1(graph, SVector[0])
    elif SVector[1][0] == maxS:
        fixS2(graph, SVector)
    elif SVector[2][0] == maxS:
        fixS3(graph, SVector[2])
    elif SVector[3][0] == maxS:
        fixS4(graph, SVector)
    
    return graph
    
    
    

graph = gp.getGraph()

Energy = el.calculateEnergy(graph, banLecturesForProffesors, banLecturesForGrades)

fix(graph, Energy[1], Energy[2])
