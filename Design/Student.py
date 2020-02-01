import copy

import os
import time
from random import shuffle, random

from past.builtins import raw_input

from Design.Course import *
from Design.Program import *
from Design.CourseDatabase import *
from Design.CourseContainer import *

import operator


#########################################
# Course Related Functions
#########################################
def solvePrereq(course, coursesTaken):
    """

    :param course: Course.obj
    :return:
    """
    if course.getPrereq():
        stack = []
        courseArith = completePrereqs(course, coursesTaken)

        # solve post fix course
        for ele in courseArith:
            if ele == "and":
                first = stack.pop()
                second = stack.pop()
                if first == 1 and second == 1:
                    stack.append(1)
                else:
                    first = [[first], [second]]
                    stack.append(first)

            elif ele == "or":
                first = stack.pop()
                second = stack.pop()
                if first == 1 or second == 1:
                    stack.append(1)
                else:
                    first = [first, second]
                    stack.append(first)

            else:
                stack.append(ele)

        if len(stack) == 0 or stack[0] == 1:
            return []

        return stack

    else:
        return []


def completePrereqs(course, coursesTaken):
    """
    :param course:
    """
    copyPrereqArith = copy.deepcopy(course.getPrereq().getCourseArith())

    for ele in coursesTaken:
        try:
            copyPrereqArith[copyPrereqArith.index(ele)] = 1
        except ValueError:
            pass

    return copyPrereqArith


class Student:
    def __init__(self, name, pastCourseText):
        self.name = name
        self.coursesTaken = set()
        self.requirements = {}
        self.chosenCourses = {}

        self.courseDB = CourseDatabase()

        self.creditsNeeded = 0

        self.generateCoursesTaken(pastCourseText)


        self.chosenCourses["Electives"] = CourseContainer()


    def generateCoursesTaken(self, pastCourseText):
        f = open(pastCourseText)
        preTest = ["MTHWAIV1", "MTHWAIV2", "DESIGNATED SCORE ON MATHEMATICS PLACEMENT TEST", "DESIGNATED SCORE ON ENGLISH PLACEMENT TEST"]
        for course in preTest:
            self.coursesTaken.add(course)

        uniTier1Writing = ["LB133", "MC111", "MC112", "RCAH111", "WRA101", "WRA195H"]

        for line in f.read().split():
            words = line.split()
            for word in words:
                if word.isupper():
                    course = self.courseDB.getCourse(word)
                    if course.getName() != "":
                        self.coursesTaken.add(word)
                        if word in uniTier1Writing:
                            self.coursesTaken.add("COMPLETION OF TIER I WRITING REQUIREMENT")

        print(self.coursesTaken)

        f.close()


    def graduationCredits(self):
        return self.creditsNeeded

    def addProgram(self, program):
        print("\nAdding", program.name, "\n")
        self.creditsNeeded = program.credits if program.credits > self.creditsNeeded else self.creditsNeeded

        for req in program.getRequirements():
            if not self.requirements.get(req.name):
                self.requirements[req.name] = req

    def requirementCredits(self):
        total = 0
        for ele in self.chosenCourses.values():
            total += ele.getCredits()

        return total

    def addCourseToTaken(self, course):
        self.coursesTaken.add(course)

    def chooseCourses(self):
        collectionCourses = set(copy.deepcopy(self.coursesTaken))


        print("***********************************************************\n")
        print("Lets see which requirements you've fulfilled ")
        print("\n***********************************************************")
        # 1. Print Requirements you've already fulfilled
        for req in self.requirements.values():
            if req.isFulfilled(collectionCourses):
                # time.sleep(0.5)
                print("\n"+str(req))
                req.setComplete()


        print("***********************************************************\n")
        print("Lets go through the which requirements you need to fulfill")
        print("\n***********************************************************")
        input("Press any key to continue")

        for req in self.requirements.values():
            if not req.isCompleted():
                time.sleep(0.5)
                print("\n"+str(req))
                self.chooseRequirement(req, collectionCourses)
            if req.name.find("Tier I Writing") != -1:
                collectionCourses.add("COMPLETION OF TIER I WRITING REQUIREMENT")


        return collectionCourses


    def chooseRequirement(self, req, collectionCourses):
        subReq = req.getRequirements()

        bestContainer = subReq[0]
        bestContainerNum = 0

        if len(subReq) > 1:
            bestIntersect = len(set(bestContainer.getPossibleCourses()).intersection(collectionCourses))

            # choose requirement with most intersection
            for i in range(1, len(subReq)):
                if len(set(subReq[i].getPossibleCourses()).intersection(collectionCourses)) > bestIntersect:
                    bestContainer = subReq[i]
                    bestContainerNum = i

            print("Recommended: Set "+str(bestContainerNum)+"-", bestContainer)

            changeSet = input("Would you like to change the recommended Set [y/n] ? : ")

            if changeSet == "y":
                changeSetNum = input("Which set would you like (type the number of the set) ? :")
                while not changeSetNum.isdigit() or int(changeSetNum) > len(subReq):
                    changeSetNum = input("Which set would you like (type the number of the set) ? :")
                bestContainerNum = int(changeSetNum)
                bestContainer = subReq[bestContainerNum]


            print("You have chosen: ")
            print(bestContainer)

            time.sleep(1.5)


        # iterate through reqContainer to choose courses
        for reqset in bestContainer.get():
            # if type of requirement is courses
            if reqset.typeChoice == "course":
                newCourseCont = self.courseRequirement(reqset, collectionCourses)
                self.chosenCourses[req.name] = newCourseCont
            # if requirement type is credits
            else:
                newCourseCont = self.creditRequirement(reqset, collectionCourses)
                self.chosenCourses[req.name] = newCourseCont


    def courseRequirement(self, reqset, collectionCourses):
        """
        Lets user choose which courses to take for the requirement
        :param reqset: Requirement.obj Requirement to get courses from
        :param collectionCourses: set<string> names of courses taken so far
        :return: CourseContainer.obj Courses chosen for the specific requirement
        """
        newCourseCont = CourseContainer()  # container for current requirement courses

        # 1. course intersection first
        reqIntersect = set(reqset.getCourses()).intersection(collectionCourses)
        for course in reqIntersect:
            courseObj = self.courseDB.getCourse(course)
            newCourseCont.addCourseByObject(courseObj)
            if len(newCourseCont) >= reqset.number:
                break

        if len(newCourseCont) > 0:
            print("Current Fulfillments: ", newCourseCont)


        # 2. show which courses are best
        if len(newCourseCont) < reqset.number:

            # a. If there are multiple options
            if len(reqset.getCourses()) > reqset.number:
                # I. List best options
                self.listBestOptions(reqset, collectionCourses)

                # II. Let user choose options
                while len(newCourseCont) < reqset.number:
                    if len(newCourseCont) > 0:
                        print("Current chosen courses: ", newCourseCont)
                    courseObj = self.getNewCourse()
                    newCourseCont.addCourseByObject(courseObj)
                    collectionCourses.add(courseObj.getCode())
                    self.addPrerequisite(courseObj, collectionCourses)


            # b. Can only use those courses
            else:
                for course in reqset.getCourses():
                    courseObj = self.courseDB.getCourse(course)
                    while courseObj.getName() == "":
                        print("Requirement "+course+" needs a course")
                        courseObj = self.getNewCourse()

                    newCourseCont.addCourseByObject(courseObj)
                    collectionCourses.add(courseObj.getCode())
                    self.addPrerequisite(courseObj, collectionCourses)

                while len(newCourseCont) < reqset.number:
                    if len(newCourseCont) > 0:
                        print("Current chosen courses: ", newCourseCont)
                    courseObj = self.getNewCourse()
                    newCourseCont.addCourseByObject(courseObj)
                    collectionCourses.add(courseObj.getCode())
                    self.addPrerequisite(courseObj, collectionCourses)

        return newCourseCont

    def creditRequirement(self, reqset, collectionCourses):
        """
        Lets user choose which courses to take for the requirement
        :param reqset: Requirement.obj Requirement to get courses from
        :param collectionCourses: set<string> names of courses taken so far
        :return: CourseContainer.obj Courses chosen for the specific requirement
        """
        newCourseCont = CourseContainer()  # container for current requirement courses

        # 1. course intersection first
        reqIntersect = set(reqset.getCourses()).intersection(collectionCourses)
        for course in reqIntersect:
            courseObj = self.courseDB.getCourse(course)
            newCourseCont.addCourseByObject(courseObj)
            if newCourseCont.getCredits() >= reqset.number:
                break

        if newCourseCont.getCredits() > 0:
            print("Current Fulfillments: ", newCourseCont)


        # 2. show which courses are best
        if newCourseCont.getCredits() < reqset.number:
            # a. If there are multiple options
            if reqset.totalCredits() > reqset.number:
                # I. List best options
                self.listBestOptions(reqset, collectionCourses)

                # II. Let user choose options
                while newCourseCont.getCredits() < reqset.number:
                    if len(newCourseCont) > 0:
                        print("Current chosen courses: ", newCourseCont)
                    courseObj = self.getNewCourse()
                    newCourseCont.addCourseByObject(courseObj)
                    collectionCourses.add(courseObj.getCode())
                    self.addPrerequisite(courseObj, collectionCourses)


            # b. Can only use those courses
            else:
                for course in reqset.getCourses():
                    courseObj = self.courseDB.getCourse(course)
                    while courseObj.getName() == "":
                        print("Requirement "+course+" needs a course")
                        courseObj = self.getNewCourse()

                    newCourseCont.addCourseByObject(courseObj)
                    collectionCourses.add(courseObj.getCode())
                    self.addPrerequisite(courseObj, collectionCourses)

                while newCourseCont.getCredits() < reqset.number:
                    if len(newCourseCont) > 0:
                        print("Current chosen courses: ", newCourseCont)
                    courseObj = self.getNewCourse()
                    newCourseCont.addCourseByObject(courseObj)
                    collectionCourses.add(courseObj.getCode())
                    self.addPrerequisite(courseObj, collectionCourses)


        return newCourseCont


    def listBestOptions(self, reqset, collectionCourses):
        bestCourses = []
        otherCourses = []

        # I. List best options
        for course in reqset.getCourses():
            courseObj = self.courseDB.getCourse(course)

            if len(solvePrereq(courseObj, collectionCourses)) == 0:  # add course you fulfill prereqs first
                bestCourses.append(courseObj)

            else:  # make a list of courses (course, number of courses you fulfill in prereqs)
                otherCourses.append(
                    (courseObj, len(set(courseObj.getPrereqCourses()).intersection(collectionCourses))))

        #  PRINTING COURSES YOU FULFILL PREREQS FOR
        if len(bestCourses) > 0:
            print("Recommended Courses:")
            for course in bestCourses:
                if course.getName() != "":
                    print(course, "Prerequisite Fulfilled")

        #  PRINTING COURSES YOU FULFILL MOST PREREQS FOR
        for course, commonPrereq in otherCourses:
            if commonPrereq > 0 or course.getNumPrereqs() == 0:
                print(course, "Fulfilled", commonPrereq, "Prerequisites for Course")

        print()


    def getNewCourse(self):
        courseObj = self.courseDB.getCourse("none")
        while courseObj.getName() == "":
            newCourse = input(
                "Add another course or type 'menu' to look up courses: ")
            courseObj = self.courseDB.getCourse(newCourse)

            if newCourse == "menu":
                self.courseDB.courseLookUp()
            else:
                courseObj = self.courseDB.getCourse(newCourse)

        return courseObj

    def addPrerequisite(self, courseObj, collectionCourses):
        while len(solvePrereq(courseObj, collectionCourses)) != 0:
            print("Courses Left: ", solvePrereq(courseObj, collectionCourses))
            print("Add courses to fulfill ", courseObj.getCode(), "prerequisite: \n", courseObj.getPrereqLine())
            courseObj = self.getNewCourse()
            self.chosenCourses.get("Electives").addCourseByObject(courseObj)
            collectionCourses.add(courseObj.getCode())
\

