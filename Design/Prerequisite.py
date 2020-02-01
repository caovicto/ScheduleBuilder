from Utilities.LineParsers import *


class Prerequisite:
    def __init__(self, prereqLine=""):
        """
        self.courses: (list) of courses, where all [[A], [B]]=A and B, [A, B]=A or B
        """
        self.courseArith = []
        self.line = prereqLine
        if prereqLine:
            self.createPrerequisite()


    def __str__(self):
        return self.line

    def getNumPrereqs(self):
        return len(self.getAllCourses())

    def getAllCourses(self):
        """

        :return: list<string> all courses of prerequisite
        """
        courses = []
        for ele in self.courseArith:
            if ele not in ["and", "or", "(", ")"]:
                courses.append(ele)

        return courses

    def getCourseArith(self):
        return self.courseArith

    # helper functions
    def createPrerequisite(self):
        """
        Changes line into post fix notation
        """
        parsed_line = re.findall(r"[\w]+|[()]", self.line)

        # parsed_line = combine_text(parsed_line)

        s_arith = []

        i = 0
        while i < len(parsed_line):
            if parsed_line[i] in ["and", "or", "("]:
                s_arith.append(parsed_line[i])

            elif parsed_line[i] == ")":
                popped = s_arith.pop()
                while popped != "(":
                    self.courseArith.append(popped)
                    popped = s_arith.pop()

            else:
                c = combine_course(i, parsed_line)
                self.courseArith.append(c[0].upper())
                i = c[1] - 1

            i += 1

        while s_arith:
            self.courseArith.append(s_arith.pop())

