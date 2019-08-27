import graph as gp
import evaluating as el
import optimization as opt

from datetime import datetime
import math

AVG_COST = 5500

P0 = 0.9
PG = 0.01
G = 300
MAX_G = 1000

TEMPERATURE_0 = (-AVG_COST) / (math.log(P0))
TEMPERATURE = TEMPERATURE_0
STEP = (-AVG_COST / (TEMPERATURE_0 * math.log(PG))) ** (1 / G)

def writeParameters(fileName):
    f = open(fileName, 'w')

    f.write('AVG_COST' + ',' + str(AVG_COST) + '\n')
    f.write('P0' + ',' + str(P0) + '\n')
    f.write('PG' + ',' + str(PG) + '\n')
    f.write('G' + ',' + str(G) + '\n')
    f.write('MAX_G' + ',' + str(MAX_G) + '\n')
    f.write('\n')

    f.write('NUMBER_OF_HARD_CONSTRAINTS' + ',' + str(el.NUMBER_OF_HARD_CONSTRAINTS) + '\n')
    f.write('NUMBER_OF_SOFT_CONSTRAINTS' + ',' + str(el.NUMBER_OF_SOFT_CONSTRAINTS) + '\n')
    f.write('MAX_LECTURES_PER_DAY_FOR_PROF' + ',' + str(el.MAX_LECTURES_PER_DAY_FOR_PROF) + '\n')
    f.write('H0_PENALTY' + ',' + str(el.H0_PENALTY) + '\n')
    f.write('S1_PENALTY' + ',' + str(el.S1_PENALTY) + '\n')
    f.write('S2_PENALTY' + ',' + str(el.S2_PENALTY) + '\n')
    f.write('S3_PENALTY' + ',' + str(el.S3_PENALTY) + '\n')
    f.write('S4_PENALTY' + ',' + str(el.S4_PENALTY) + '\n')
    f.write('S5_PENALTY' + ',' + str(el.S5_PENALTY) + '\n')
    f.write('S6_PENALTY' + ',' + str(el.S6_PENALTY) + '\n')
    f.write('S7_PENALTY' + ',' + str(el.S7_PENALTY) + '\n')
    f.write('S8_PENALTY' + ',' + str(el.S8_PENALTY) + '\n')

    f.close()

def getFileName():
    fN = str(datetime.now())
    fN = fN.replace('-', '').replace(' ', '').replace(':', '').replace('.', '')

    return fN

def getParameters():
    return [P0, PG, G, MAX_G]

def getMin():
    graph = gp.getGraph()

    print(len(graph.nodes))

    Energy = el.calculateEnergy(graph, opt.banLecturesForProfessors, opt.banLecturesForGrades)

    changesCounter = 0

    global TEMPERATURE

    generation = 0
    minPenalty = Energy[0]
    minEnergy = Energy
    minGraph = graph
    #k = 1

    while generation < MAX_G:
        graph, Energy, change = opt.annealing(graph, Energy, TEMPERATURE)
        changesCounter += change

        if minPenalty > Energy[0]:
            minPenalty = Energy[0]
            minEnergy = Energy
            minGraph = graph

        if generation % 100 == 0:
            print(generation, changesCounter, Energy[0], TEMPERATURE)
        
        #if TEMPERATURE > 1:    
        TEMPERATURE = TEMPERATURE * STEP
        
        '''
        else:
            TEMPERATURE = TEMPERATURE_0 * (STEP ** k)
            k += 1
        '''
        generation += 1

    fileName = getFileName()

    gp.writeGraph(minGraph, getParameters(), fileName)


    print(minPenalty, minEnergy[1][0])
    print(TEMPERATURE_0, TEMPERATURE, STEP)
    print(AVG_COST)
    print(P0, PG)
    print(G, MAX_G)
    print('-')
    #print(minEnergy[1][0], minEnergy[2][0][0], minEnergy[2][1][0], minEnergy[2][2][0], minEnergy[2][3][0], minEnergy[2][4][0], minEnergy[2][5][0], minEnergy[2][6][0], minEnergy[2][7][0])

    return minGraph

getMin()