import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from LineParsers import *


class Major:
    class Requirement:
        def __init__(self):
            self.completed = False
            self.req_list = []

        def set_completed(self):
            self.completed = True

        def add_req(self, rset):
            self.req_list.append(rset)

        def print_requirements(self):
            for ele in self.req_list:
                print(ele.number, ele.type_choice, "from", ele.choices)

        def __str__(self):
            s = ""
            for i in range(1, len(self.req_list)+1):
                s += str(i) + ". "
                for ele in self.req_list[i-1].choices:
                    s += ele

    class ReqSet:
        def __init__(self, n, type_choice, choices):
            self.number = n
            self.type_choice = type_choice
            self.choices = choices

    def __init__(self, p_number, n):
        self.program_number = p_number
        self.name = n
        self.credits = 0

        self.requirements = []
        self.alias = []

    def get_number(self):
        return self.program_number

    def get_requirements(self):
        # initialize selenium
        url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + self.get_number()
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        driver.get(url)

        # scrape requirement information from website
        info = driver.find_elements_by_xpath("//div[@class='panel-body']")
        paragraphs = info[1].text.split('\n\n')

        # parse website information
        for i in range(len(paragraphs)):
            # finds total credits for major
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

                req.print_requirements()


        driver.close()

    def print_major(self):
        print(self.name)


class MajorDatabase:
    def __init__(self):
        self.table = {}

        url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=UN'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
            s = ele.get('href')
            m = Major(s[len(s) - 4:len(s)], ele.text)

            self.add_major(m)

    def add_major(self, major):
        name = major.name

        if not self.table.get(name):
            self.table[name] = major

    def get_major(self, major_name):
        return self.table.get(major_name)

    def print_database(self):
        print(self.table)



def find_total_credits(line):
    words = line.split()
    for i in range(len(line)):
        if words[i] == "Credits:":
            return int(words[i+1])

