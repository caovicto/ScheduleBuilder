from Design.Course import *


class CourseContainer:
    def __init__(self):
        """
        :param self.container: list<Course.obj>
        """
        self.container = []
        self.totalCredits = 0

    def __str__(self):
        s = ""
        for course in self.container:
            s += str(course) + ", "

        return s[:-2]

    def __len__(self):
        return len(self.container)

    def inside(self, course):
        return course in self.container

    def get(self):
        return self.container

    def getCourseStrings(self):
        tempArr = []
        for course in self.container:
            tempArr.append(course.getCode())
        return tempArr

    def getCourse(self, code):
        for course in self.container:
            if course.getCode() == code:
                return course

    def remove(self, course):
        if course in self.container:
            self.container.remove(course)

    def getCredits(self):
        return self.totalCredits

    def setCredits(self, credits):
        self.totalCredits = credits

    def addCourseByObject(self, course):
        if course not in self.container:
            self.container.append(course)
            if type(course) == Course:
                self.totalCredits += course.getCredits()
            return True

        return False

    def numCourses(self):
        return len(self.container)-self.numDivs()-self.countNone()
