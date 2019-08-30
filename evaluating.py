import graph as gp

#Hard constraints:
#0. Professors and grades cannot have two lectures at the same time

#Soft constraints:
#1. Professors cannot have lectures explicit times
#2. Grades cannot have lectures at explicit times
#3. Grades cannot have empty lectures except first and last ones in a day
#4. Grades cannot be thought by the same professor more than once a day
#5. Professors should not have empty lectures
#6. Professors should not have more than MAX_LECTURES_PER_DAY_FOR_PROF lectures per day
#7. Professors should have equal number of lectures each day
#8. Grades should not have lecture by the same professor more days in a row

#---constants---

NUMBER_OF_HARD_CONSTRAINTS = 1
NUMBER_OF_SOFT_CONSTRAINTS = 8

MAX_LECTURES_PER_DAY_FOR_PROF = 3

H0_PENALTY = 200

S1_PENALTY = 100
S2_PENALTY = 100
S3_PENALTY = 100
S4_PENALTY = 20
S5_PENALTY = 5
S6_PENALTY = 10
S7_PENALTY = 5
S8_PENALTY = 50

#---------------

def findNode(graph, proff = None, grade = None, colour = None):
    'Finds node in the graph'
    for node in list(graph.nodes):
        if (proff == None or node.proff == proff) and (grade == None or node.grade == grade) and (colour == None or graph.nodes[node]['colour'] == colour):
            return node
    return None

def H0(graph):
    'Professors and grades cannot have two lectures at the same time'
    naughtyNodes = []
    professorsLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_PROFF)]
    gradesLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_GRADES)]
    for node in list(graph.nodes):
        try:
            if professorsLectures[node.proff][graph.nodes[node]['colour']] == 0 and gradesLectures[node.grade][graph.nodes[node]['colour']] == 0:
                professorsLectures[node.proff][graph.nodes[node]['colour']] = 1
                gradesLectures[node.grade][graph.nodes[node]['colour']] = 1
            else:
                naughtyNodes.append(node)
        except:
            naughtyNodes.append(node)
    penalty = H0_PENALTY * len(naughtyNodes)
    #print(naughtyNodes)
    return (penalty, naughtyNodes, professorsLectures, gradesLectures)

def S1(graph, professorsLectures, banLecturesForProfessors):
    'Professors cannot have lectures at explicit times'
    naughtyNodes = []
    for lecture in banLecturesForProfessors:
        if professorsLectures[lecture[0]][lecture[1]] == 1:
            naughtyNodes.append(findNode(graph, proff = lecture[0], colour = lecture[1]))
    penalty = S2_PENALTY * len(naughtyNodes)
    #print(naughtyNodes)
    return (penalty, naughtyNodes)

def S2(graph, gradesLectures, banLecturesForGrades):
    'Grades cannot have lectures explicit times'
    naughtyNodes = []
    for lecture in banLecturesForGrades:
        if gradesLectures[lecture[0]][lecture[1]] == 1:
            naughtyNodes.append(findNode(graph, grade = lecture[0], colour =  lecture[1]))
    penalty = S1_PENALTY * len(naughtyNodes)
    #print(naughtyNodes)
    return (penalty, naughtyNodes)

def S3(gradesLectures):
    'Grades cannot have empty lectures except first and last ones in a day'
    emptyGradesLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_GRADES)]
    penalty = 0
    for grade in range(gp.NUMBER_OF_GRADES):
        for day in range(gp.WORKING_DAYS):
            for lectures in range(gp.LECTURES_PER_DAY)[1:-1]:
                if gradesLectures[grade][gp.LECTURES_PER_DAY * day + lectures] == 0:
                    emptyGradesLectures[grade][gp.LECTURES_PER_DAY * day + lectures] = 1
                    penalty += S3_PENALTY
    return (penalty, emptyGradesLectures)

def S4(graph):
    'Grades cannot be thought by the same professor more than once a day'
    naughtyNodes = []
    lecturesInDay = [[] for i in range(gp.WORKING_DAYS)]
    for node in list(graph.nodes):
        day = graph.nodes[node]['colour'] // gp.LECTURES_PER_DAY
        nodeTuple = (node.proff, node.grade)
        if not nodeTuple in lecturesInDay[day]:
            lecturesInDay[day].append(nodeTuple)
        else:
            naughtyNodes.append(node)
    penalty = S4_PENALTY * len(naughtyNodes)
    #print(naughtyNodes)
    return (penalty, naughtyNodes, lecturesInDay)

def S5(professorsLectures):
    'Professors should not have empty lectures'
    emptyProfessorsLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_PROFF)]
    penalty = 0
    for proff in range(gp.NUMBER_OF_PROFF):
        for day in range(gp.WORKING_DAYS):
            firstLecture = 0
            lastLecture = 0
            for lectures in range(gp.LECTURES_PER_DAY):
                if professorsLectures[proff][gp.LECTURES_PER_DAY * day + lectures] == 1:
                    firstLecture = 1
                    lastLecture = lectures
                if firstLecture == 1 and professorsLectures[proff][gp.LECTURES_PER_DAY * day + lectures] == 0:
                    emptyProfessorsLectures[proff][gp.LECTURES_PER_DAY * day + lectures] = 1
            for lastEmptyLectures in range(lastLecture, gp.LECTURES_PER_DAY):
                emptyProfessorsLectures[proff][gp.LECTURES_PER_DAY * day + lastEmptyLectures] = 0
        penalty += S5_PENALTY * emptyProfessorsLectures[proff].count(1)
    return (penalty, emptyProfessorsLectures)

def S6(graph, professorsLectures):
    'Professors should not have more than MAX_LECTURES_PER_DAY_FOR_PROF lectures per day'
    numberOfLecturesPerDay = [[0 for i in range(gp.WORKING_DAYS)] for j in range(gp.NUMBER_OF_PROFF)]
    penalty = 0
    for proff in range(gp.NUMBER_OF_PROFF):
        for day in range(gp.WORKING_DAYS):
            for lecture in range(gp.LECTURES_PER_DAY):
                if professorsLectures[proff][gp.LECTURES_PER_DAY * day + lecture] == 1:
                    numberOfLecturesPerDay[proff][day] += 1
            if numberOfLecturesPerDay[proff][day] > MAX_LECTURES_PER_DAY_FOR_PROF:
                penalty += S6_PENALTY * (numberOfLecturesPerDay[proff][day] - MAX_LECTURES_PER_DAY_FOR_PROF)

    naughtyNodes = []
    for node in graph:
        if numberOfLecturesPerDay[node.proff][graph.nodes[node]['colour'] // gp.LECTURES_PER_DAY] > MAX_LECTURES_PER_DAY_FOR_PROF:
            naughtyNodes.append(node) 
    #print(naughtyNodes)

    return (penalty, naughtyNodes, numberOfLecturesPerDay)

def S7(graph, numberOfLecturesPerDay):
    'Professors should have equal number of lectures each day'
    naughtyProfessorsDays = [[0 for i in range(gp.WORKING_DAYS)] for j in range(gp.NUMBER_OF_PROFF)]
    penalty = 0
    for proff in range(gp.NUMBER_OF_PROFF):
        averageNumOfLectures = (sum(numberOfLecturesPerDay[proff]) + gp.WORKING_DAYS - 1) // gp.WORKING_DAYS
        for day in range(gp.WORKING_DAYS):
            if numberOfLecturesPerDay[proff][day] > averageNumOfLectures + 1 or numberOfLecturesPerDay[proff][day] < averageNumOfLectures - 1:
                naughtyProfessorsDays[proff][day] = numberOfLecturesPerDay[proff][day] - averageNumOfLectures
                penalty += S7_PENALTY * abs(naughtyProfessorsDays[proff][day])

    naughtyNodes = []
    for node in graph:
        if naughtyProfessorsDays[node.proff][graph.nodes[node]['colour'] // gp.LECTURES_PER_DAY] > 0:
            naughtyNodes.append(node)
    #print(naughtyNodes)

    return (penalty, naughtyNodes, naughtyProfessorsDays)

def S8(graph, lecturesInDay):
    'Grades should not have lecture by the same professor more days in a row'
    twoDaysLectures = [[] for i in range(gp.WORKING_DAYS)]
    penalty = 0
    for numDay, day in enumerate(lecturesInDay):
        for lecture in day:
            if numDay > 0 and lecture in lecturesInDay[numDay - 1] and lecture not in twoDaysLectures[numDay - 1]:
                twoDaysLectures[numDay].append(lecture)
        penalty += S8_PENALTY * len(twoDaysLectures[numDay])

    naughtyNodes = []
    for node in graph:
        if (node.proff, node.grade) in twoDaysLectures[graph.nodes[node]['colour'] // gp.LECTURES_PER_DAY]:
            naughtyNodes.append(node)
    #print(naughtyNodes)
    
    return (penalty, naughtyNodes, twoDaysLectures)

def calculateEnergy(graph, banLecturesForProfessors, banLecturesForGrades):
    energy = 0

    H0Energy = H0(graph)
    H0Penalty = H0Energy[0]
    #H0NaughtyNodes = H0Energy[1]
    professorsLectures = H0Energy[2]
    gradesLectures = H0Energy[3]

    energy += H0Penalty
    #print(H0Penalty)

    S1Energy = S1(graph, professorsLectures, banLecturesForProfessors)
    S1Penalty = S1Energy[0]
    #S1NaughtyNodes = S1Energy[1]

    energy += S1Penalty
    #print(S1Penalty)

    S2Energy = S2(graph, gradesLectures, banLecturesForGrades)
    S2Penalty = S2Energy[0]
    #S2NaughtyNodes = S2Energy[1]

    energy += S2Penalty
    #print(S2Penalty)

    S3Energy = S3(gradesLectures)
    S3Penalty = S3Energy[0]
    #gradesEmptyLectures = S3Energy[1]

    energy += S3Penalty
    #print(S3Penalty)

    S4Energy = S4(graph)
    S4Penalty = S4Energy[0]
    #S4NaughtyNodes = S4Energy[1]
    gradesLecturesInDay = S4Energy[2]

    energy += S4Penalty
    #print(S4Penalty)

    S5Energy = S5(professorsLectures)
    S5Penalty = S5Energy[0]
    #professorsEmptyLectures = S5Energy[1]

    energy += S5Penalty
    #print(S5Penalty)

    S6Energy = S6(graph, professorsLectures)
    S6Penalty = S6Energy[0]
    #S6NaughtyNodes = S6Energy[1]
    professorsNumberOfLecturesPerDay = S6Energy[2]

    energy += S6Penalty
    #print(S6Penalty)

    S7Energy = S7(graph, professorsNumberOfLecturesPerDay)
    S7Penalty = S7Energy[0]
    #S7NaughtyNodes = S7Energy[1]
    #naughtyProfessorsDays = S7Energy[2]

    energy += S7Penalty
    #print(S7Penalty)

    S8Energy = S8(graph, gradesLecturesInDay)
    S8Penalty = S8Energy[0]
    #naughtyNodes[1]
    #gradesTwoDaysLectures = S8Energy[2]

    energy += S8Penalty
    #print(S8Penalty)

    return (energy, H0Energy, (S1Energy, S2Energy, S3Energy, S4Energy, S5Energy, S6Energy, S7Energy, S8Energy))

'''
MAIN

g = gp.getGraph()

t = H0(g)
print(t[0])

banLecturesForGrades = [((0, 0)]
banLecturesForProfessors = [(0, 0)]

t1 = S1(g, t[1], banLecturesForProfessors)
print(t1[0])

t2 = S2(g, t[2], banLecturesForGrades)
print(t2[0])

t3 = S3(t[2])
print(t3[0])

t4 = S4(g)
print(t4[0])

l1 = S5(t[1])
print(l1[0])

l2 = S6(t[1])
print(l2[0])

l4 = S8(t4[1])
print(l4[0])
'''