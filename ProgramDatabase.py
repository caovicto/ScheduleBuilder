import os
import requests
import sqlite3
from bs4 import BeautifulSoup

from Program import *


class ProgramDatabase:
    def __init__(self):
        self.path = "/home/victoria/ScheduleBuilder/Databases/Programdb.sqlite3"

        self.connection = sqlite3.connect(self.path)
        self.cur = self.connection.cursor()

    def create_database(self):
        """
        DO NOT USE UNLESS RECREATING DATABASE
        """
        os.remove(self.path)

        self.initialize_database()
        self.initialize_majors()
        self.initialize_minors()

        self.list_entire_database()

    def initialize_database(self):
        """
        Generates table within
        :param name: name of the table
        """
        major_sql = """
        CREATE TABLE Major (
            Pid integer NOT NULL,
            name text NOT NULL); """

        self.cur.execute(major_sql)

        minor_sql = """
        CREATE TABLE Minor (
            Pid integer NOT NULL,
            name text NOT NULL); """

        self.cur.execute(minor_sql)

        self.connection.commit()

    def initialize_majors(self):
        """
        Adds all majors
        """
        # Scraping majors from website
        url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=UN'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        # add all majors within page
        for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
            s = ele.get('href')  # text for link

            p_number = int(s[len(s) - 4:len(s)])
            p_name = ele.text
            p_type = "Major"

            self.add_program(p_number, p_name, p_type)

        self.connection.commit()

    def initialize_minors(self):
        # Scraping minors from website
        url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=MNUN'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
            s = ele.get('href')  # text for link
            parse_name = ele.text.split()

            p_number = int(s[len(s) - 4:len(s)])
            p_name = ' '.join(parse_name[2:])
            p_type = "Minor"

            self.add_program(p_number, p_name, p_type)

        self.connection.commit()

    def add_program(self, p_num, p_name, p_type):
        """
        Adds program name as key, program object as value
        :param program: program Object
        """
        insert_sql = "INSERT INTO " + p_type + " (Pid, name) " + \
                     "VALUES (?, ?)"

        self.cur.execute(insert_sql, (p_num, p_name))

    def list_elements_in_table(self, program):
        """
        lists all elements form table with name cCode
        """
        self.cur.execute("SELECT Pid, name FROM " + program)
        for ele in self.cur.fetchall():
            print(ele)

    def list_entire_database(self):
        """
        Lists all elements within Database
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for ele in self.cur.fetchall():
            print("***************************************************************************")
            print("\nTABLE: ", ele[0], "\n")
            self.list_elements_in_table(ele[0])


    def get_program(self, p_name, p_type):
        """
        Gets program from database
        """
        try:
            self.cur.execute("SELECT Pid, name FROM " + p_type +
                             " WHERE name='" + p_name + "'")
            ele = self.cur.fetchone()
            return ele

        except sqlite3.OperationalError:
            self.cur.execute("SELECT Pid, name FROM " + p_type)
            for ele in self.cur.fetchall():
                if ele[1].find(p_name) != -1:
                    return ele

            return None

