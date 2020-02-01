from Utilities.LineParsers import *


class Course:
    class Prerequisite:
        def __init__(self, prereq_sentence):
            """
            self.courses: (list) of courses, where all [[A], [B]]=A and B, [A, B]=A or B
            self.completed: (bool) if self.courses is all True
            """
            self.courses = []
            self.create_prerequisite(prereq_sentence)  # changes self.courses into parsable format
            self.raw_courses = []
            self.get_raw_courses()

            self.course_arith = self.courses

        def all_possible_courses(self):
            return self.raw_courses

        def get_courses(self):
            return self.courses

        def get_raw_courses(self):
            for ele in self.courses:
                if ele not in ["and", "or", "(", ")"]:
                    self.raw_courses.append(ele)

        # helper functions
        def create_prerequisite(self, line):
            """
            Changes line into post fix notation
            """
            parsed_line = re.findall(r"[\w]+|[()]", line)

            # parsed_line = combine_text(parsed_line)

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


        def solve_prereq(self):
            """
            "Solves" post fix course arithmetic
            """
            stack = []
            for ele in self.course_arith:
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

            if stack[0] == 1:
                return True
            return False


    def __init__(self, code, name="", sem="", cred="0 0", prereqs=[]):
        """
        self.code: (string) subject code and course code
        self.name: (
        self.credits: (pair<int, int>) first: lower bound credit, second: upper bound credit
        """

        self.code = code
        self.name = name
        self.semester = sem

        self.completed = False
        self.prereq_completed = True

        c_list = cred.split()
        try:
            self.credits = (int(c_list[0]), int(c_list[1]))
        except IndexError:
            self.credits = (int(c_list[0]), int(c_list[0]))


        if prereqs:
            self.prereq_string = prereqs
            self.prerequisites = Course.Prerequisite(prereqs)
            self.prereq_completed = False
        else:
            self.prereq_string = ""
            self.prerequisites = None


    def __str__(self):
        """

        :return:
        """
        c_string = self.get_code() + ": " + self.get_name()
        c_string += "\nCredits: " + str(self.credit_average())
        c_string += "\nCompleted: " + str(self.completed)
        c_string += "\nPrerequisites: " + self.prereq_string

        return c_string

    def complete_prereq(self, code):
        """
        :param code:
        """
        if self.prerequisites:
            try:
                self.prerequisites.course_arith[self.prerequisites.course_arith.index(code)] = 1
                if self.prerequisites.solve_prereq():
                    self.prereq_completed = True
                    return True

            except ValueError:
                pass

        return False

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
        if self.credit_ub() == self.credit_lb():
            return str(self.credit_ub())
        else:
            return str(self.credit_lb())+"-"+str(self.credit_ub())

    def credit_lb(self):
        """

        :return:
        """
        return self.credits[0]

    def credit_ub(self):
        """

        :return:
        """
        return self.credits[1]

    def credit_average(self):
        """
        :return: average credits for course
        """
        return (self.credits[0]+self.credits[1])/2

    def get_prerequisite(self):
        """

        :return:
        """
        if self.prerequisites:
            return self.prerequisites.get_courses()

    def get_list_prerequisites(self):
        """
        gets list of all courses within prerequisite list
        """
        if self.prerequisites:
            return self.prerequisites.all_possible_courses()

        return []

    def complete(self):
        self.completed = True

    def is_completed(self):
        return self.completed

    def is_prereq_completed(self):
        return self.prereq_completed









