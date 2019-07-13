import graph as gp

#Hard constraints:
#0. Proffesors and grades cannot have two lectures at the same time
#1. Proffesors cannot have lectures explicit times
#2. Grades cannot have lectures at explicit times
#3. Grades cannot have empty lectures except first and last ones in a day
#4. Grades cannot be thought by the same proffesor more than once a day

#Soft constraints:
#1. Proffesors should not have empty lectures
#2. Proffesors should not have more than MAX_LECTURES_PER_DAY_FOR_PROF lectures per day
#3. Proffesors should have equal number of lectures each day
#4. Grades should not have lecture by the same proffesor more days in a row

MAX_LECTURES_PER_DAY_FOR_PROF = 5

H0_PENALTY = 1
H1_PENALTY = 1
H2_PENALTY = 1
H3_PENALTY = 1
H4_PENALTY = 1

S1_PENALTY = 1
S2_PENALTY = 1
S3_PENALTY = 1
S4_PENALTY = 1

def H0(graph):
    'Proffesors and grades cannot have two lectures at the same time'
    naughtyNodes = []
    proffesorsLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_PROFF)]
    gradesLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_GRADES)]
    for node in list(graph.nodes):
        try:
            if proffesorsLectures[node.proff][graph.nodes[node]['colour']] == 0 and gradesLectures[node.grade][graph.nodes[node]['colour']] == 0:
                proffesorsLectures[node.proff][graph.nodes[node]['colour']] = 1
                gradesLectures[node.grade][graph.nodes[node]['colour']] = 1
            else:
                naughtyNodes.append(node)
        except:
            naughtyNodes.append(node)
    penalty = H0_PENALTY * len(naughtyNodes)
    return (penalty, proffesorsLectures, gradesLectures, naughtyNodes)

def H1(gradesLectures, banLecturesForGrades):
    'Proffesors cannot have lectures explicit times'
    naughtyNodes = []
    for lecture in banLecturesForGrades:
        if gradesLectures[lecture[0][1]][lecture[1]] == 1:
            naughtyNodes.append(lecture)
    penalty = H1_PENALTY * len(naughtyNodes)
    return (penalty, naughtyNodes)

def H2(proffesorsLectures, banLecturesForProffesors):
    'Grades cannot have lectures at explicit times'
    naughtyNodes = []
    for lecture in banLecturesForProffesors:
        if proffesorsLectures[lecture[0][1]][lecture[1]] == 1:
            naughtyNodes.append(lecture)
    penalty = H2_PENALTY * len(naughtyNodes)
    return (penalty, naughtyNodes)

def H3(gradesLectures):
    'Grades cannot have empty lectures except first and last ones in a day'
    emptyLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_GRADES)]
    penalty = 0
    for grade in range(gp.NUMBER_OF_GRADES):
        for day in range(gp.WORKING_DAYS):
            for lectures in range(gp.LECTURES_PER_DAY)[1:-1]:
                if gradesLectures[grade][gp.LECTURES_PER_DAY * day + lectures] == 0:
                    emptyLectures[grade][gp.LECTURES_PER_DAY * day + lectures] = 1
                    penalty += H3_PENALTY
    return (penalty, emptyLectures)

def H4(graph):
    'Grades cannot be thought by the same proffesor more than once a day'
    naughtyNodes = []
    lecturesInDay = [[] for i in range(gp.WORKING_DAYS)]
    for node in list(graph.nodes):
        day = graph.nodes[node]['colour'] // gp.LECTURES_PER_DAY
        nodeTuple = (node.proff, node.grade)
        if not nodeTuple in lecturesInDay[day]:
            lecturesInDay[day].append(nodeTuple)
        else:
            naughtyNodes.append(nodeTuple)
    penalty = H4_PENALTY * len(naughtyNodes)
    return (penalty, lecturesInDay, naughtyNodes)

def S1(proffesorsLectures):
    'Proffesors should not have empty lectures'
    emptyLectures = [[0 for i in range(gp.NUMBER_OF_COLOURS)] for j in range(gp.NUMBER_OF_PROFF)]
    penalty = 0
    for proff in range(gp.NUMBER_OF_PROFF):
        for day in range(gp.WORKING_DAYS):
            firstLecture = 0
            lastLecture = 0
            for lectures in range(gp.LECTURES_PER_DAY):
                if proffesorsLectures[proff][gp.LECTURES_PER_DAY * day + lectures] == 1:
                    firstLecture = 1
                    lastLecture = lectures
                if firstLecture == 1 and proffesorsLectures[proff][gp.LECTURES_PER_DAY * day + lectures] == 0:
                    emptyLectures[proff][gp.LECTURES_PER_DAY * day + lectures] = 1
            for lastEmptyLectures in range(lastLecture, gp.LECTURES_PER_DAY):
                emptyLectures[proff][gp.LECTURES_PER_DAY * day + lastEmptyLectures] = 0
        penalty += S1_PENALTY * emptyLectures[proff].count(1)
    return (penalty, emptyLectures)

def S2(proffesorsLectures):
    'Proffesors should not have more than MAX_LECTURES_PER_DAY_FOR_PROF lectures per day'
    numberOfLecturesPerDay = [[0 for i in range(gp.WORKING_DAYS)] for j in range(gp.NUMBER_OF_PROFF)]
    penalty = 0
    for proff in range(gp.NUMBER_OF_PROFF):
        for day in range(gp.WORKING_DAYS):
            for lecture in range(gp.LECTURES_PER_DAY):
                if proffesorsLectures[proff][gp.LECTURES_PER_DAY * day + lecture] == 1:
                    numberOfLecturesPerDay[proff][day] += 1
            if numberOfLecturesPerDay[proff][day] > MAX_LECTURES_PER_DAY_FOR_PROF:
                penalty += S2_PENALTY * (numberOfLecturesPerDay[proff][day] - MAX_LECTURES_PER_DAY_FOR_PROF)

    return (penalty, numberOfLecturesPerDay)

def S3(numberOfLecturesPerDay):
    'Proffesors should have equal number of lectures each day'
    naughtyProffesorsDays = [[0 for i in range(gp.WORKING_DAYS)] for j in range(gp.NUMBER_OF_PROFF)]
    penalty = 0
    for proff in range(gp.NUMBER_OF_PROFF):
        averageNumOfLectures = (sum(numberOfLecturesPerDay[proff]) + gp.WORKING_DAYS - 1) // gp.WORKING_DAYS
        for day in range(gp.WORKING_DAYS):
            if numberOfLecturesPerDay[proff][day] > averageNumOfLectures + 1 or numberOfLecturesPerDay[proff][day] < averageNumOfLectures - 1:
                naughtyProffesorsDays[proff][day] = numberOfLecturesPerDay[proff][day] - averageNumOfLectures
                penalty += S3_PENALTY * abs(naughtyProffesorsDays[proff][day])
    return (penalty, naughtyProffesorsDays)


def S4(lecturesInDay):
    'Grades should not have lecture by the same proffesor more days in a row'
    twoDaysLectures = [[] for i in range(gp.WORKING_DAYS)]
    penalty = 0
    for numDay, day in enumerate(lecturesInDay):
        for lecture in day:
            if numDay > 0 and lecture in lecturesInDay[numDay - 1]:
                if numDay > 1 and not lecture in lecturesInDay[numDay - 2]:
                    twoDaysLectures[numDay].append(lecture)
                twoDaysLectures[numDay].append(lecture)
        penalty += S4_PENALTY * len(twoDaysLectures[numDay])
    return (penalty, twoDaysLectures)
                        
'''
MAIN

g = gp.getGraph()

t = H0(g)
print(t[0])

banLecturesForGrades = [((0,0),0)]
banLecturesForProffesors = [((0,0),0)]

t1 = H1(t[2], banLecturesForGrades)
print(t1[0])

t2 = H2(t[1], banLecturesForProffesors)
print(t2[0])

t3 = H3(t[2])
print(t3[0])

t4 = H4(g)
print(t4[0])

l1 = S1(t[1])
print(l1[0])

l2 = S2(t[1])
print(l2[0])

l4 = S4(t4[1])
print(l4[0])
'''