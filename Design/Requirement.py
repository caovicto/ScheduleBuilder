import nltk
import re
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import PorterStemmer

from Design.CourseDatabase import *

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)

    return sent


class Requirement:
    def __init__(self, requirementString):
        try:
            self.completed = False
            self.possibleReqs = []

            self.text = requirementString

            brokenReq = requirementString.split(':')
            self.name = brokenReq[1].split('\n')[0][1:]

            for ele in brokenReq:
                self.addReq(ele)

        except IndexError:
            pass

    def __eq__(self, other):
        return self.name == other.name


    def isValid(self):
        if len(self.possibleReqs) > 0:
            return True
        return False

    def isCompleted(self):
        return self.completed

    def getRequirements(self):
        return self.possibleReqs

    # def getName(self):
    #     return self.name

    def addReq(self, line):
        possibleOptions = ReqContainer()

        splitLine = line.split('\n')
        for ele in splitLine:
            typeReq = None
            num = None
            choices = []

            sentenceNlp = preprocess(ele)
            # print(sentenceNlp)
            try:
                if sentenceNlp.index(('from', 'IN')):
                    typeReq = sentenceNlp[sentenceNlp.index(('from', 'IN'))-1][0][:6]
                    num = int(sentenceNlp[sentenceNlp.index(('from', 'IN'))-2][0])
                    choices = ele[ele.find("from")+5:].split(',')
                    choices = [course.upper() for course in choices]
                    choices = [course.strip() for course in choices]


            except ValueError:
                pass

            if (typeReq == "course" or typeReq == "credit") and num and choices:
                newReqSet = ReqSet(num, typeReq, choices)
                possibleOptions.add(newReqSet)

        if len(possibleOptions) > 0:
            self.possibleReqs.append(possibleOptions)


    def __str__(self):
        s = self.name + "\n"
        if len(self.possibleReqs) > 1:
            counter = 0
            for ele in self.possibleReqs:
                s += "Set " + str(counter) + ": \n" + str(ele)
                counter += 1
        else:
            s += str(self.possibleReqs[0])

        return s


    def isFulfilled(self, collectionsCourses):
        for req in self.possibleReqs:
            if req.isFulfilled(collectionsCourses):
                return True

        return False

    def setComplete(self):
        self.completed = True


class ReqContainer:
    def __init__(self):
        self.container = []

    def __str__(self):
        s = ""
        for ele in self.container:
            s += str(ele)

        return s

    def __len__(self):
        return len(self.container)

    def get(self):
        return self.container

    def add(self, reqset):
        self.container.append(reqset)

    def getPossibleCourses(self):
        tempList = []
        for req in self.container:
            tempList.extend(req.courses)
        return tempList

    def isFulfilled(self, collectionCourses):
        fulfilled = True
        for req in self.container:
            fulfilled = fulfilled and req.isFulfilled(collectionCourses)

        return fulfilled


class ReqSet:
    def __init__(self, number, typeChoice, courses):
        """
        self.number: (int) number for courses/credits
        self.type_choice: (string) "courses" or "credits"
        self.choices: (list<string>) courses available
        """
        self.number = number
        self.typeChoice = typeChoice
        self.courses = courses
        if self.courses:
            self.courses.sort()


    def __str__(self):
        s = str(self.number) + " " + self.typeChoice + " [" + ",".join(self.courses) + "]\n"
        return s

    def getCourses(self):
        return self.courses

    def totalCredits(self):
        totalCredits = 0
        courseDB = CourseDatabase()
        for code in self.courses:
            courseObj = courseDB.getCourse(code)
            totalCredits += courseObj.getCredits()

        return totalCredits

    def isFulfilled(self, collectionCourses):
        if self.typeChoice == "course":
            intersection = len(set(self.courses).intersection(collectionCourses))

            if intersection >= self.number:
                return True
            else:
                return False

        else:
            courseDB = CourseDatabase()
            creditCount = 0
            intersection = set(self.courses).intersection(collectionCourses)

            for course in intersection:
                courseObj = courseDB.getCourse(course)
                creditCount += courseObj.getCredits()
                if creditCount >= self.number:
                    return True

            return False
