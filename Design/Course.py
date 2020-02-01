from Design.Subject import *
from Design.Term import *
from Design.Prerequisite import *


class Course:
    def __init__(self, name, subject, code, creds, terms, prereqs=None):
        """
        :param name: string
        :param subject: Subject.obj
        :param code: string
        :param creds: int
        :param terms: list<Term.obj>
        :param prereqs: Prerequisite.obj
        """
        self.name = name
        self.subject = subject
        self.code = code.upper()

        self.credits = creds

        # Find credits if course is abstract
        if creds == 0 and name.find("Lab") != -1:
            self.credits = 1
            for ele in self.name:
                if ele.isdigit():
                    self.credits = int(ele)
                    break

        elif creds == 0:
            self.credits = 3


        self.terms = terms
        self.prerequisite = prereqs
        self.level = 5

        # Find level of course
        for ele in self.code:
            if ele.isdigit():
                self.level = int(ele)
                break


    def __str__(self):
        try:
            s = str(self.subject) + " " + self.code + self.name + \
                str(self.credits) + " " + str(','.join(self.terms)) + \
                str(self.prerequisite)
        except TypeError:
            s = self.code

        return s

    def __lt__(self, other):
        return self.code < other.code

    def __gt__(self, other):
        return self.code > other.code

    def __eq__(self, other):
        if type(self) == Course and type(other) == Course:
            return self.code == other.code
        else:
            return False

    def getLevel(self):
        return self.level

    def getCode(self):
        return self.code

    def getPrereq(self):
        return self.prerequisite

    def getPrereqLine(self):
        return self.prerequisite.line

    def getPrereqCourses(self):
        if self.prerequisite:
            return self.prerequisite.getAllCourses()
        else:
            return []

    def getNumPrereqs(self):
        return self.prerequisite.getNumPrereqs()

    def getCredits(self):
        return self.credits

    def getName(self):
        return self.name

    def termEligible(self, term):
        if term in self.terms:
            return True
        else:
            return False
