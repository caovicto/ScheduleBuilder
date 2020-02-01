from Design.Student import *
from Design.CourseDatabase import *
from Design.Course import *
from Design.ProgramDatabase import *



coursedb = CourseDatabase()
programdb = ProgramDatabase()

pastCourses = "../PreviousCourses/Victoria.txt"
suj = Student(pastCourses)


def testSolvePrereq():
    pastCourses = {"WRA101", "MTHWAIV2", "IAH201", "MTH134", "ISS210"}
    suj = Student(pastCourses)
    course = coursedb.getCourse("WRA101")

    print(suj.solvePrereq(course))



def addProgramTest():
    suj = Student()
    accounting = programdb.getProgramByName("Journalism", "Major")
    suj.addProgram(accounting)

    # actScience = programdb.getProgramByName("Computer Science", "Major")
    # suj.addProgram(actScience)

    for ele in suj.requirements:
        print(ele)


def chooseCoursesTest():
    accounting = programdb.getProgramByName("Computer Science", "Major")
    math = programdb.getProgramByName("Mathematics", "Minor")
    suj.addProgram(accounting)
    suj.addProgram(math)

    suj.chooseCourses()
    ele = suj.chosenCourses
    # print(suj.chosenCourses)


def requirementCreditsTest():
    accounting = programdb.getProgramByName("Journalism", "Major")
    suj.addProgram(accounting)

    suj.chooseCourses()
    print(suj.requirementCredits())



def classOrderTest():
    journ = programdb.getProgramByName("Journalism", "Major")
    chinese = programdb.getProgramByName("Minor in Chinese", "Minor")
    suj.addProgram(journ)
    suj.addProgram(chinese)

    suj.chooseCourses()
    l = suj.classOrder()
    print(l)
    print(l.getCredits())
    print(l.numCourses())


def generateCoursesTest():
    vic = Student("../PreviousCourses/Victoria.txt")


chooseCoursesTest()
