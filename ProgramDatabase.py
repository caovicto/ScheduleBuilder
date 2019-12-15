import requests
from bs4 import BeautifulSoup

from Major import *


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
        """
        Adds major name as key, major object as value
        :param major: Major Object
        """
        name = major.name

        if not self.table.get(name):
            self.table[name] = major

    def get_major(self, major_name):
        """
        Grabs all requirement information from major
        """
        if self.table.get(major_name):
            major = self.table.get(major_name)
            major.get_requirements()

            return major

    def print_database(self):
        print(self.table)

