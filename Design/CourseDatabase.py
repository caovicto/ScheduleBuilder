import sqlite3

from Design.Term import *
from Design.Subject import *
from Design.Prerequisite import *
from Design.Course import *


def getTerms(termList):
    """
    Returns
    :param termList: string
    :return: Term.obj from termList
    """
    vectorTerms = []
    if termList.find("F") != -1:
        vectorTerms.append(Term("Fall"))

    if termList.find("Sp") != -1:
        vectorTerms.append(Term("Spring"))

    if termList.find("Su") != -1:
        vectorTerms.append(Term("Summer"))

    return vectorTerms


class CourseDatabase:
    def __init__(self):
        self.path = "/home/victoria/Projects/ScheduleBuilder/Databases/Coursedb.sqlite3"

        self.connection = sqlite3.connect(self.path)
        self.cur = self.connection.cursor()

    def getCourse(self, code):
        """
        Gets course item from course database
        """
        table = "c"+subject_code(code)
        course_id = subject_id(code)

        # get course from database
        try:
            self.cur.execute("SELECT Cid, name, semester, credits, prerequisites FROM " + table +
                             " WHERE Cid='" + course_id + "'")

            # 0:number 1:name 2:terms 3:credits 4:prerequisites
            ele = self.cur.fetchone()

            # get information for course
            name = ele[1]
            subject = Subject(subject_code(code))
            credits = int(ele[3][-1])
            termList = getTerms(ele[2])
            prerequisite = Prerequisite(ele[4])

            course = Course(name, subject, code, credits, termList, prerequisite)

            return course

        except (sqlite3.OperationalError, TypeError) as e:
            subject = Subject(subject_code(code))
            return Course("", subject, code, 0, None)

    def courseLookUp(self):
        done = False
        while not done:
            print("\n*************************  Menu *******************************")
            print("List Subject Code: 0 ")
            print("List Subject Code by First Letter: 1 [a-z]")
            print("List Courses from Subject: 2 <subject code>")
            print("List Courses from Subject with Level: 3 <subject code> [1-4]")
            print("Search Course: 4 <code>")
            print("Exit: 666")
            print("***************************************************************")
            request = input("\nCommand: ")
            print()

            try:
                if request[0] == '0':
                    for ele in self.listTables():
                        subject = Subject(ele[0][1:])
                        print(subject)

                elif request[0] == '1':
                    for ele in self.listTables():
                        if ele[0][1].upper() == request[2].upper():
                            subject = Subject(ele[0][1:])
                            print(subject)

                elif request[0] == '2':
                    code = subject_code(request[2:])
                    for ele in self.listElementsTable(code):
                        print("Code: "+ele[0], " |  Name: "+ele[1], "\nCredits:"+ele[3], " |  Prerequisites:"+str(ele[4])+"\n")

                elif request[0] == '3':
                    code = subject_code(request[2:])
                    for ele in self.listElementsTable(code):
                        if ele[0][0] == request[6:]:
                            print("Code: "+ele[0], " |  Name: "+ele[1], "\nCredits:"+ele[3], " |  Prerequisites:"+str(ele[4])+"\n")

                elif request[0] == '4':
                    code = subject_code(request[2:])
                    for ele in self.listElementsTable(code):
                        if ele[0][0:] == subject_id(request[2:]):
                            print("Code: "+ele[0], " |  Name: "+ele[1], "\nCredits:"+ele[3], " |  Prerequisites:"+str(ele[4])+"\n")
                            break

                elif request == "666":
                    done = True

                else:
                    print("Error: Invalid Command")

            except (IndexError, sqlite3.OperationalError) as e:
                print("Error: Invalid Command")

    #######################################################
    # Printing
    #######################################################
    def listTables(self):
        """
        Lists all tables in database
        """
        fetch_sub = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cur.execute(fetch_sub)
        return self.cur.fetchall()

    def listElementsTable(self, code):
        """
        lists all elements form table with name cCode
        """
        self.cur.execute("SELECT Cid, name, semester, credits, prerequisites FROM " + "c" + code)
        return self.cur.fetchall()

    def listDatabase(self):
        """
        Lists all elements within Database
        """
        for ele in self.listTables():
            print("***************************************************************************")
            print("\nTABLE: ", ele[0], "\n")
            for ele2 in self.listElementsTable(ele[0]):
                print(ele2)
