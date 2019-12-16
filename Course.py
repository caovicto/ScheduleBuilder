from Utilities.LineParsers import *


class Course:
    class Prerequisite:
        def __init__(self, courses):
            self.courses = []
            self.completed = False

            self.create_prerequisite()

        def completed_course(self, code):
            pass

        # helper functions
        def create_prerequisite(self, line):
            parsed_line = re.findall(r"[\w]+|[()]", line)
            s_arith = []

            i = 0
            while i < len(parsed_line):
                if parsed_line[i] in ["and", "or", "("]:
                    s_arith.append(parsed_line[i])

                elif parsed_line[i] == ")":
                    popped = s_arith.pop()
                    while popped != "(":
                        self.courses.append(popped)
                        popped = s_arith.pop()

                else:
                    c = combine_course(i, parsed_line)
                    self.courses.append(c[0])
                    i = c[1] - 1

                i += 1

            while s_arith:
                self.courses.append(s_arith.pop())

            # create in 
            self.rearrange_prereq()

        def rearrange_prereq(self):
            stack = []
            for ele in self.courses:
                if ele == "and":
                    first = stack.pop()
                    second = stack.pop()
                    if is_ands(first) and type(second) is str:
                        first.append([second])
                        stack.append(first)
                    else:
                        stack.append([[first], [second]])

                elif ele == "or":
                    first = stack.pop()
                    second = stack.pop()
                    if is_ors(first) and type(second) is str:
                        first.append(second)
                        stack.append(first)
                    else:
                        stack.append([first, second])

                else:
                    stack.append(ele)

            self.courses = stack[0]

    def __init__(self, code, name, sem, cred, prereqs):
        self.code = code
        self.name = name
        self.semester = sem
        self.credits = cred

        self.prereq_string = prereqs
        self.prerequisites = Course.Prerequisite()

        self.completed = False

    def __str__(self):
        """

        :return:
        """
        c_string = self.get_code() + ": " + self.get_name()
        c_string += "\nCredits: " + self.get_credits()
        c_string += "\nPrerequisites: " + self.prereq_string

        return c_string

    # getting functions
    def get_code(self):
        """

        :return:
        """
        return self.code

    def get_name(self):
        """

        :return:
        """
        return self.name

    def get_credits(self):
        """

        :return:
        """
        return self.credits

    def get_prerequisite(self):
        """

        :return:
        """
        return self.prerequisites

    # information completion
    def set_complete(self):
        """

        :return:
        """
        self.completed = True




def is_ors(l):
    if type(l) is list:
        for ele in l:
            if type(ele) is not str:
                return False

        return True

    return False


def is_ands(l):
    if type(l) is list:
        for ele in l:
            if type(ele) is not list:
                return False

        return True

    return False






