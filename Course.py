from Utilities.LineParsers import *


class Course:
    def __init__(self, code, name, sem, cred, prereqs):
        self.code = code
        self.name = name
        self.semester = sem
        self.credits = cred

        self.prereq_string = prereqs
        self.prerequisites = []
        self.create_prerequisite(prereqs)

        self.completed = False

        # printing

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
                    self.prerequisites.append(popped)
                    popped = s_arith.pop()

            else:
                c = combine_course(i, parsed_line)
                self.prerequisites.append(c[0])
                i = c[1] - 1

            i += 1

        while s_arith:
            self.prerequisites.append(s_arith.pop())

