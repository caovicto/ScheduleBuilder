import os
import sqlite3
from Design.Program import *


class ProgramDatabase:
    def __init__(self):
        cwd = os.getcwd()
        self.path = cwd + "/Databases/Programdb.sqlite3"

        self.connection = sqlite3.connect(self.path)
        self.cur = self.connection.cursor()

    def getProgramByName(self, p_name, p_type):
        """
        Gets program from database
        """
        try:
            self.cur.execute("SELECT number, name, requirements FROM " + p_type +
                             " WHERE name='" + p_name + "'")
            ele = self.cur.fetchone()

            # Program(number, name, reqString)
            program = Program(ele[0], ele[1], ele[2])
            return program

        except sqlite3.OperationalError:
            pass

        return None

    def getProgramByNumber(self, p_number, p_type):
        """
        Gets program from database
        """
        try:
            self.cur.execute("SELECT number, name, requirements FROM " + p_type +
                             " WHERE number='" + p_number + "'")
            ele = self.cur.fetchone()

            program = Program(ele[0], ele[1], ele[2])
            return program

        except sqlite3.OperationalError:
            pass

        return None


    def list_elements_in_table(self, program):
        """
        lists all elements form table with name cCode
        """
        self.cur.execute("SELECT number, name FROM " + program)
        return self.cur.fetchall()

    def list_entire_database(self):
        """
        Lists all elements within Database
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for ele in self.cur.fetchall():
            print("***************************************************************************")
            print("\nTABLE: ", ele[0], "\n")
            self.list_elements_in_table(ele[0])