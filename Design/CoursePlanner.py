from math import ceil, floor
from Design.Term import *
from Design.Student import *
from Design.ProgramDatabase import *


class CoursePlanner:
    def __init__(self, student):
        self.student = student
        self.creditMax = 12
        self.programDB = ProgramDatabase()
        self.courseDB = CourseDatabase()

        self.startMenu()

    def startMenu(self):
        # 1. Add Major
        self.chooseMajor()

        # 2. Add Minor
        minor = input("Would you like to choose a minor [y/n]?: ")
        if minor == "y":
            self.chooseMinor()


        # 3. Choose Courses
        listCourses = self.student.chooseCourses()
        chosenCourses = CourseContainer()
        allCourses = CourseContainer()
        for course in listCourses:
            courseObj = self.courseDB.getCourse(course)

            if course not in self.student.coursesTaken:
                if courseObj.getName() != "":
                    chosenCourses.addCourseByObject(courseObj)

            allCourses.addCourseByObject(courseObj)


        time.sleep(2)
        print()
        print("You are at", allCourses.getCredits())
        print("Graduation requires", self.student.graduationCredits())
        electiveCredits = self.student.graduationCredits()-allCourses.getCredits()
        if electiveCredits > 0:
            totalElective = ceil(electiveCredits/3)
            print("You'll need about", totalElective, " elective to fill the extra ", electiveCredits)

            addElective = "y"
            while addElective != "n":
                addElective = input(
                    "Add electives you know you'll want or enter 'n' and the rest will be filled with a dummy: ")
                courseObj = self.courseDB.getCourse(addElective)
                if courseObj.getName() != "":
                    chosenCourses.addCourseByObject(courseObj)
                    print("Added ", courseObj.getName())

        print()

        print("Now we have all the classes you need. Let's create your schedule")
        season = input("What term are we starting with (Fall/Spring)?: ")
        semList = self.arrange(season, chosenCourses)

        print("Here is your schedule")
        for sem in semList:
            print(sem)

        file = open("/home/victoria/Projects/ScheduleBuilder/Schedules/"+self.student.name+".txt", 'w+')
        for sem in semList:
            file.write(str(sem))



    def chooseMajor(self):
        print("********************************************************\n")
        print("\t\t\t Choosing a Major")
        print("\n********************************************************\n")

        time.sleep(3)
        print("Here are all the programs")
        time.sleep(2)
        listMajors = sorted(self.programDB.list_elements_in_table("Major"), key=lambda x: x[1])
        for ele in listMajors:
            print(ele)
        time.sleep(0.5)

        while True:
            programNum = input("Add a program (n to quit): ")
            if programNum == "n":
                break
            else:
                program = self.programDB.getProgramByNumber(programNum, "Major")
                self.addProgram(program, "Major")


    def chooseMinor(self):
        print("\n********************************************************\n")
        print("\t\t\t Choosing a Minor")
        print("\n********************************************************\n")

        time.sleep(1)
        print("Here are all the programs")
        time.sleep(1)
        listMajors = sorted(self.programDB.list_elements_in_table("Minor"), key=lambda x: x[1])
        for ele in listMajors:
            print(ele)
        time.sleep(0.5)

        while True:
            programNum = input("Add a program (n to quit): ")
            if programNum == "n":
                break
            else:
                program = self.programDB.getProgramByNumber(programNum, "Minor")
                self.addProgram(program, "Minor")


    def addProgram(self, program, programType):
        self.student.addProgram(program)

    def arrange(self, startTerm, chosenCourses):
        semList = [Semester(startTerm)]
        semCourses = []

        counter = 0
        while len(chosenCourses) > 0 and counter < 50:
            print(semList[-1])
            # print(self.student.coursesTaken)
            # print(chosenCourses)

            eligibleCourses = CourseContainer()
            for course in chosenCourses.get():
                if len(solvePrereq(course, self.student.coursesTaken)) == 0 and course.termEligible(semList[-1].Term):
                    eligibleCourses.addCourseByObject(course)

            if semList[-1].getCredits() >= self.creditMax:
                createNew = input(
                    "You're at "+str(semList[-1].getCredits())+" would you like to start a new Semster [y/n]? ")
                if createNew == "y":
                    for courseObj in semCourses:
                        self.student.addCourseToTaken(courseObj.getCode())

                    semCourses = []

                    if startTerm == "Fall":
                        startTerm = "Spring"
                    else:
                        startTerm = "Fall"

                    semList.append(Semester(startTerm))
                else:
                    print("These are courses you can take: ")
                    print(eligibleCourses)
                    courseObj = self.courseDB.getCourse("none")
                    while len(eligibleCourses) > 0 and courseObj not in eligibleCourses.get():
                        addCourse = input("Choose a course: ")
                        courseObj = chosenCourses.getCourse(addCourse)

                    chosenCourses.remove(courseObj)
                    eligibleCourses.remove(courseObj)
                    semCourses.append(courseObj)

                    semList[-1].addCourse(courseObj)

            elif len(eligibleCourses) != 0:
                print("These are courses you can take: ")
                print(eligibleCourses)
                courseObj = self.courseDB.getCourse("none")
                while len(eligibleCourses) > 0 and courseObj not in eligibleCourses.get():
                    addCourse = input("Choose a course: ")
                    courseObj = chosenCourses.getCourse(addCourse)

                chosenCourses.remove(courseObj)
                eligibleCourses.remove(courseObj)
                semCourses.append(courseObj)

                semList[-1].addCourse(courseObj)


            else:
                for courseObj in semCourses:
                    self.student.addCourseToTaken(courseObj.getCode())

                semCourses = []

                if startTerm == "Fall":
                    startTerm = "Spring"
                else:
                    startTerm = "Fall"

                semList.append(Semester(startTerm))

            counter += 1


        return semList


class Semester:
    def __init__(self, season):
        self.courses = []
        self.credits = 0
        self.Term = Term(season)
        self.num = 0

    def __len__(self):
        return self.num

    def getCredits(self):
        return self.credits

    def addCourse(self, course):
        self.courses.append(course)
        self.credits += course.getCredits()
        self.num += 1

    def __str__(self):
        s = "SEMESTER: " + str(self.Term) + "\n"
        for ele in self.courses:
            s += str(ele) + "\n"

        return s

