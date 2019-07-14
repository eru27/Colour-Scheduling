import graph as gp
import evaluating as el

def calculateEnergy(graph, banLecturesForProffesors, banLecturesForGrades):
    energy = 0

    H0 = el.H0(graph)
    H0Penalty = H0[0]
    proffesorsLectures = H0[1]
    gradesLectures = H0[2]
    H0NaughtyNodes = H0[3]

    energy += H0Penalty
    #print(H0Penalty)

    H1 = el.H1(graph, proffesorsLectures, banLecturesForProffesors)
    H1Penalty = H1[0]
    H1NaughtyNodes = H1[1]

    energy += H1Penalty
    #print(H1Penalty)

    H2 = el.H2(graph, gradesLectures, banLecturesForGrades)
    H2Penalty = H2[0]
    H2NaughtyNodes = H2[1]

    energy += H2Penalty
    #print(H2Penalty)

    H3 = el.H3(gradesLectures)
    H3Penalty = H3[0]
    gradesEmptyLectures = H3[1]

    energy += H3Penalty
    #print(H3Penalty)

    H4 = el.H4(graph)
    H4Penalty = H4[0]
    gradesLecturesInDay = H4[1]
    H4NaughtyNodes = H4[2]

    energy += H4Penalty
    #print(H4Penalty)

    S1 = el.S1(proffesorsLectures)
    S1Penalty = S1[0]
    proffesorsEmptyLectures = S1[1]

    energy += S1Penalty
    #print(S1Penalty)

    S2 = el.S2(proffesorsLectures)
    S2Penalty = S2[0]
    proffesorsNumberOfLecturesPerDay = S2[1]

    energy += S2Penalty
    #print(S2Penalty)

    S3 = el.S3(proffesorsNumberOfLecturesPerDay)
    S3Penalty = S3[0]
    S3NaughtyNodes = S3[1]

    energy += S3Penalty
    #print(S3Penalty)

    S4 = el.S4(gradesLecturesInDay)
    S4Penalty = S4[0]
    gradesTwoDaysLectures = S4[1]

    energy += S4Penalty
    #print(S4Penalty)

    return (energy, (H0, H1, H2, H3, H4), (S1, S2, S3, S4))

    




banLecturesForGrades = [(0, 0)]
banLecturesForProffesors = [(0, 0)]

graph = gp.getGraph()


