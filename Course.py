from Utilities.LineParsers import *


class Course:
    class Prerequisite:
        def __init__(self, prereq_sentence):
            """
            self.courses: (list) of courses, where all [[A], [B]]=A and B, [A, B]=A or B
            self.completed: (bool) if self.courses is all True
            """
            self.courses = []
            self.raw_courses = get_all_courses(prereq_sentence)
            self.completed = False

            # changes self.courses into parsable format
            self.create_prerequisite(prereq_sentence)

        def all_possible_courses(self):
            return self.raw_courses

        def get_courses(self):
            return self.courses

        def complete_course(self, code):
            pass

        def are_prereqs_completed(self):
            pass

        # helper functions
        def create_prerequisite(self, line):
            """
            Changes line into post fix notation
            """
            parsed_line = re.findall(r"[\w]+|[()]", line)

            parsed_line = combine_text(parsed_line)

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
            """
            "Solves" post fix course arithmetic
            """
            stack = []
            for ele in self.courses:
                if ele == "and":
                    first = stack.pop()
                    second = stack.pop()
                    if type(first) is list and type(first[0]) == type(second):
                        first.append([second])
                    else:
                        first = [[first], [second]]
                    stack.append(first)

                elif ele == "or":
                    first = stack.pop()
                    second = stack.pop()
                    if type(first) is list and type(first[0]) == type(second):
                        first.append(second)
                    else:
                        first = [first, second]
                    stack.append(first)


                else:
                    stack.append(ele)

            self.courses = stack[0]


    def __init__(self, code, name, sem, cred, prereqs):
        """
        self.code: (string) subject code and course code
        self.name: (
        self.credits: (pair<int, int>) first: lower bound credit, second: upper bound credit
        """
        self.code = code
        self.name = name
        self.semester = sem

        c_list = cred.split()
        try:
            self.credits = (int(c_list[0]), int(c_list[1]))
        except IndexError:
            self.credits = (int(c_list[0]), int(c_list[0]))


        if prereqs:
            self.prereq_string = prereqs
            self.prerequisites = Course.Prerequisite(prereqs)
        else:
            self.prereq_string = ""
            self.prerequisites = None

        self.completed = False

    def __str__(self):
        """

        :return:
        """
        c_string = self.get_code() + ": " + self.get_name()
        c_string += "\nCredits: " + str(self.get_credits())
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

    # information completion
    def set_complete(self):
        """

        :return:
        """
        self.completed = True








