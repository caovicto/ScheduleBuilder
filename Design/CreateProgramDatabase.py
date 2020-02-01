import os
import sqlite3
from Design.Program import *


class CreateProgramDatabase:
    def __init__(self):
        self.path = "../Databases/Programdb.sqlite3"

        self.connection = sqlite3.connect(self.path)
        self.cur = self.connection.cursor()

        self.createDatabase()

        self.listDatabase()


    ###############################################################
    #          Initializing Databse Functions
    ###############################################################

    def createDatabase(self):
        """
        DO NOT USE UNLESS RECREATING DATABASE
        """
        self.initializeDatabase()
        self.initializeMajors()
        self.initializeMinors()

        self.listDatabase()

    def initializeDatabase(self):
        """
        Generates table within
        :param name: name of the table
        """
        major_sql = """
        CREATE TABLE Major (
            number int NOT NULL,
            name text NOT NULL,
            requirements text); """

        self.cur.execute(major_sql)

        minor_sql = """
        CREATE TABLE Minor (
            number int NOT NULL,
            name text NOT NULL,
            requirements text); """

        self.cur.execute(minor_sql)

        self.connection.commit()

    def initializeMajors(self):
        counter = 0

        for filename in os.listdir("../Majors"):
            path = "../Majors/"+filename
            f = open(path)
            name = filename[:-4]
            text = f.read()

            self.addProgram(counter, name, text, "Major")

            counter += 1

    def initializeMinors(self):
        counter = 0

        for filename in os.listdir("../Minors"):
            path = "../Minors/"+filename
            f = open(path)
            name = filename[9:-4]
            text = f.read()

            self.addProgram(counter, name, text, "Minor")

            counter += 1


    def addProgram(self, number, p_name, text, p_type):
        """
        Adds program name as key, program object as value
        :param program: program Object
        """
        try:
            insert_sql = "INSERT INTO " + p_type + " (number, name, requirements) " + \
                         "VALUES (?, ?, ?)"

            self.cur.execute(insert_sql,
                             (number, p_name, text))

            self.connection.commit()

        except sqlite3.OperationalError:
            pass



    def listDatabase(self):
        """
        Lists all elements within Database
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for ele in self.cur.fetchall():
            print("***************************************************************************")
            print("\nTABLE: ", ele[0], "\n")
            self.listElementsInTable(ele[0])

    def listElementsInTable(self, program):
        """
        lists all elements form table with name cCode
        """
        self.cur.execute("SELECT name, requirements FROM " + program)
        for ele in self.cur.fetchall():
            print(ele)


