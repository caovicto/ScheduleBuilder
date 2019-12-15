from selenium import webdriver

from Utilities.LineParsers import *


class Program:
    class ReqSet:
        def __init__(self, n, type_choice, choices):
            """
            self.number: (int) number for courses/credits
            self.type_choice: (string) "courses" or "credits"
            self.choices: (list<string>) courses available
            """
            self.number = n
            self.type_choice = type_choice
            self.choices = choices

    class Requirement:
        def __init__(self):
            """
            self.completed: (bool) if the requirement if fulfilled
            self.req_list: (list<ReqSet>) sets of choices that can fulfill the requirement
            """
            self.completed = False
            self.req_list = []

        def set_completed(self):
            self.completed = True

        def add_req(self, rset):
            self.req_list.append(rset)

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
    def __init__(self, p_number, p_name, p_type):
        """

        """
        self.program_number = str(p_number)
        self.program_name = p_name
        self.program_type = p_type

        self.credits = 0
        self.requirements = []

        # initialize credits and requirements
        self.initialize_requirements()

        self.alias = []

    def initialize_requirements(self):
        """
        Get requirements for program
        """
        # initialize selenium
        url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + self.program_number
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        driver.get(url)

        # scrape requirement information from website
        info = driver.find_elements_by_xpath("//div[@class='panel-body']")
        paragraphs = info[1].text.split('\n\n')

        counter = 0

        # parse website information
        for i in range(len(paragraphs)):
            # finds total credits for program
            if paragraphs[i].find("Required Credits:") != -1:
                self.credits = find_total_credits(paragraphs[i])
                print("CREDITS", self.credits, "\n")

            # str
            else:
                # print(paragraphs[i])
                raw_courses = remove_titles(paragraphs[i])
                req = self.Requirement()

                # print(raw_courses, '\n')

                for row in raw_courses:
                    info = find_all_codes(row)

                    if len(info[2]) != 0 and info[0] != 0:
                        new_req = self.ReqSet(info[0], info[1], info[2])
                        req.add_req(new_req)

                # add requirement to requirement list
                self.requirements.append(req)

        driver.close()

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

