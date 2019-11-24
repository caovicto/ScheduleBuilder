import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class Major:
    class Requirement:
        def __init__(self):
            self.number = 0
            self.req_list = []

    def __init__(self, p_number, n):
        self.program_number = p_number
        self.name = n
        self.credits = 0
        self.requirements = {}
        self.alias = []

    def get_number(self):
        return self.program_number

    def get_requirements(self):
        url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + self.get_number()
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        driver.get(url)

        results = driver.find_elements_by_xpath("//*[@id='MainContent_divDnData']")
        # header = driver.find_elements_by_xpath("//strong")
        info = driver.find_elements_by_xpath("//div[@class='panel-body']")

        for i in range(len(info)):
            # if info[i].text.find("Required Credits:") != -1:
            #     n = info[i].text.split()
            #     print(n[2])
            # else:
            #     print(info[i].text)
            print(info[i].text)



        driver.close()

        time.sleep(5)




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





