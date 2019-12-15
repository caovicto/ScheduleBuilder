import requests
from bs4 import BeautifulSoup

from Program import *
import sqlite3


class ProgramDatabase:
    def __init__(self):
        self.path = "/home/victoria/ScheduleBuilder/Databases/Programdb.sqlite3"

        self.connection = sqlite3.connect(self.path)
        self.cur = self.connection.cursor()

    def initialize_database(self):
        """
        Generates table within
        :param name: name of the table
        """
        major_sql = """
        CREATE TABLE Major (
            Pid text NOT NULL,
            name text NOT NULL); """

        self.cur.execute(major_sql)

        minor_sql = """
                CREATE TABLE Minor (
                    Pid text NOT NULL,
                    name text NOT NULL); """

        self.cur.execute(minor_sql)

    def initialize_majors(self):
        # ADDING MAJORS
        url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=UN'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        # add all majors within page
        for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
            s = ele.get('href')  # text for link

            p_name = s[len(s) - 4:len(s)]
            p_number = ele.text
            p_type = "Major"

            self.add_program(p_name, p_number, p_type)

        # ADDING MINORS
        url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=UN'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
            s = ele.get('href')  # text for link

            p_name = s[len(s) - 4:len(s)]
            p_number = ele.text
            p_type = "Minor"

            self.add_program(p_name, p_number, p_type)

    def initialize_minors(self):

    def add_program(self, p_name, p_num, p_type):
        """
        Adds program name as key, program object as value
        :param program: program Object
        """
        insert_sql = "INSERT INTO " + p_type + " (Pid, name) " + \
                     "VALUES (?, ?, ?, ?, ?)"

        num = vals[0]
        nm = vals[1]
        sem = vals[2]
        cred = vals[3]
        prereq = vals[4]

        self.cur.execute(insert_sql, (num, nm, sem, cred, prereq))

    def get_program(self, program_name):
        """
        Grabs all requirement information from program
        """
        if self.table.get(program_name):
            program = Program()
            program.get_requirements()

            return program

    def print_database(self):
        print(self.table)

