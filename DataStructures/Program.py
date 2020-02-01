from DataStructures.CourseDatabase import *


class Program:
    class ReqSet:
        def __init__(self, n, type_choice, choices):
            """
            self.number: (int) number for courses/credits
            self.type_choice: (string) "courses" or "credits"
            self.choices: (list<string>) courses available
            """
            self.number = int(n)
            self.type_choice = type_choice
            self.choices = choices

    class Requirement:
        def __init__(self, name):
            """
            self.completed: (bool) if the requirement if fulfilled
            self.req_list: (list<ReqSet>) sets of choices that can fulfill the requirement
            """
            self.completed = False
            self.name = name
            self.req_list = []

        def set_completed(self):
            self.completed = True

        def add_req(self, rset):
            self.req_list.append(rset).

        def print_requirements(self):
            for ele in self.req_list:
                print(ele.number, ele.type_choice, "from", ele.choices)

        def get_courses(self):
            l_courses = []
            for ele in self.req_list:
                for course in ele.choices:
                    l_courses.append(course)

            return l_courses

        def __str__(self):
            s = ""
            for i in range(1, len(self.req_list) + 1):
                s += str(i) + ". "
                for ele in self.req_list[i - 1].choices:
                    s += ele

    ################################################################
    # Program functions
    ################################################################
    def __init__(self, p_number, p_name="", p_type="", creds=0):
        """

        """
        self.program_number = str(p_number)
        self.program_name = p_name
        self.program_type = p_type

        self.credits = int(creds)
        self.requirements = []

        # initialize credits and requirements
        # self.initialize_requirements()

        self.alias = []

    def __str__(self):
        s = "Program " + self.program_number + ": " + self.program_name + " " + self.program_type
        s += "\nCredits: " + str(self.credits) + "\n"
        s += self.string_requirements()

        return s

    def set_name(self, name):
        self.program_name = name

    def set_type(self, type):
        self.program_type = type

    def get_credits(self):
        return self.credits

    def set_credits(self, num):
        self.credits = int(num)

    def add_requirement(self, req):
        self.requirements.append(req)

    def list_courses(self):
        """
        Lists all courses within all requirements
        """
        ret_list = []
        for req in self.requirements:
            for course in req.get_courses():  # for list of choices in req
                ret_list.append(course)

        return ret_list

    def print_requirements(self):
        """
        prints all requirements for program
        """
        for req in self.requirements:
            req.print_requirements()

    def string_requirements(self):
        """
        prints all requirements for program
        """
        s = ""
        for req in self.requirements:
            s += req.name + " Requirement: \n"
            for ele in req.req_list:
                s += str(ele.number) + "|" + ele.type_choice + "|" + ' '.join(ele.choices) + "\n"

        return s


    def list_possible_classes(self):
        courseDB = CourseDatabase()
        ret_list = []

        for req in self.requirements:
            try:
                sub_req = req.req_list[0]
                # add number of courses
                if sub_req.type_choice == "course":
                    ret_list.extend(sub_req.choices[0:sub_req.number])
                # add up to total number of credits
                else:
                    cred = 0
                    for ele in sub_req.choices:
                        if cred >= sub_req.number:
                            break

                        c = courseDB.get_course(ele)
                        if c:
                            cred += (c.credit_lb()+c.credit_ub())/2
                            ret_list.append(ele)
            except IndexError:
                pass

        return ret_list

