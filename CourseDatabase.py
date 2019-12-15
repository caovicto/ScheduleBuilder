import re
import time
import sqlite3
import os
from sqlite3 import Error

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Course import *
from LineParsers import *


#######################################################
# Parsing Information from pdf lines
#######################################################
class CourseDatabase:
    def __init__(self):
        self.path = "/home/victoria/ScheduleBuilder/Databases/Coursedb.sqlite3"

        self.connection = sqlite3.connect(self.path)
        self.cur = self.connection.cursor()

        self.create_database()

        # printing database



    def create_database(self):
        """
        DO NOT USE UNLESS RECONFIGURING DATABASE
        """
        # entering driver information
        url = 'https://reg.msu.edu/Courses/Search.aspx'
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        driver.get(url)

        selections = driver.find_element_by_id("MainContent_ddlSubjectCode")
        options = [x for x in selections.find_elements_by_tag_name("option")]
        driver.set_script_timeout(300)

        # looping through all subjects
        for text in range(1, len(options)):
            # collect subject code
            subject_element = options[text]
            subject = subject_element.get_attribute("value")
            subject_table = "c" + subject

            try:
                # add subject table to sql
                self.generate_table(subject_table)

                # selecting subject code
                subject_element.click()

                # submission
                driver.find_element_by_xpath("//input[@id='MainContent_btnSubmit']").click()

                # wait until body has loaded and contains subject information
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "MainContent_divSearchResults"))
                )
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element((By.XPATH, '//h3'), subject)
                )

                # scraping information
                course_name = driver.find_elements_by_xpath("//h3")
                info = driver.find_elements_by_xpath(
                    "//div[starts-with(@id, 'MainContent_rptrSearchResults_divMainDetails_')]")


                # Creating course information
                for i in range(len(course_name)):
                    try:
                        heading = course_name[i].text.split()  # course name
                        sub_id = heading[1]  # subject id
                        sub_name = ' '.join(heading[2:])

                        course_info = info[i].text.split('\n')  # course information

                        # values to insert: id, name, semesters, credits, prereqs
                        vals = [sub_id, sub_name, None, None, None]

                        # parse course information
                        for line in range(len(course_info)):
                            # Get semester information
                            if course_info[line] == "Semester:":
                                sem = ""
                                if course_info[line+1].find("Fall") != -1:
                                    sem += "F"
                                if course_info[line+1].find("Spring") != -1:
                                    sem += "Sp"
                                if course_info[line+1].find("Summer") != -1:
                                    sem += "Su"

                                vals[2] = sem  # add to value array
                                line += 1

                            # Get credit information
                            elif course_info[line] == "Credits:":
                                cred = ""
                                parse = course_info[line+1].split()
                                if parse[0] == "Total":  # if total credits
                                    cred = parse[2]
                                else:  # if variable credits
                                    cred = ' '.join(re.findall(r"\d+", course_info[line+1]))

                                vals[3] = cred  # add to value array
                                line += 1

                            # Get prereq information
                            elif course_info[line] == "Prerequisite:":
                                vals[4] = course_info[line+1]  # add prerequisite info
                                break

                        self.insert_to_table(subject_table, vals)

                    except IndexError:
                        break

            except (NoSuchElementException, TimeoutException, sqlite3.OperationalError) as e:
                pass

        print("\n\nDONE\n\n")
        driver.quit()

        self.connection.commit()

    def generate_table(self, name):
        """
        Generates table within
        :param name: name of the table
        """
        course_sql = """
        CREATE TABLE """ + name + """ (
            Cid text NOT NULL,
            name text NOT NULL,
            semester text NOT NULL,
            credits text NOT NULL,
            prerequisites text); """

        self.cur.execute(course_sql)


    def insert_to_table(self, subject, vals):
        """
        Inserts
        :param subject:
        :param vals: values to insert into table
        """
        insert_sql = "INSERT INTO " + subject + " (Cid, name, semester, credits, prerequisites) " + \
                     "VALUES (?, ?, ?, ?, ?)"

        num = vals[0]
        nm = vals[1]
        sem = vals[2]
        cred = vals[3]
        prereq = vals[4]

        self.cur.execute(insert_sql, (num, nm, sem, cred, prereq))


    def list_tables(self):
        """
        Lists all tables in database
        """
        fetch_sub = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cur.execute(fetch_sub)
        return self.cur.fetchall()


    def list_elements_in_table(self, code):
        """
        lists all elements form table with name cCode
        """
        self.cur.execute("SELECT Cid, name, semester, credits, prerequisites FROM "+code)
        for ele in self.cur.fetchall():
            print(ele)

    def list_entire_database(self):
        """
        Lists all elements within Database
        """
        for ele in self.list_tables():
            print("***************************************************************************")
            print("\nTABLE: ", ele[0], "\n")
            self.list_elements_in_table(ele[0])


    ##########################################################
    #  Retrieving Courses from Database
    ##########################################################
    def get_course(self, code):
        """
        Gets course item from course database
        """
        table = subject_code(code)
        course_id = subject_id(code)

        try:
            self.cur.execute("SELECT Cid, name, semester, credits, prerequisites FROM " + table + \
                             " WHERE Cid='"+ course_id +"'")
            ele = self.cur.fetchone()
            print(ele)

            course = Course()

            # course.set_course_num(' '.join(heading[0:2]))
            # course.set_name(' '.join(heading[2:]))
            # course.set_credits(find_credit(course_info[line]))
            # course.set_prerequisite(create_prerequisite(prereq))
            # self.add_course(course)
            # course.print_course()
            return course

        except ValueError:
            pass


def subject_code(s):
    """
    Returns subject code from string s
    :param s: string to find subject id
    """
    code = ""
    for letter in s:
        if is_int(letter):
            break
        code += letter
    return code


def subject_id(s):
    """
    Returns Cid from string s
    :param s: string to find subject id
    """
    for letter in range(len(s)):
        if is_int(s[letter]):
            return s[letter:]


def find_c_info(line):
    """
    if line contains course code, 3 digit number. and full course name, return pair of course code and name
    :param line: line to parse
    :param c_code: course code
    :return: <pair>(course code, name)
    """
    first_word = find_successor(line, int_present(line))
    return line[:line.find(first_word)], line[line.find(first_word):]


def find_credit(line):
    """
    If line starts with "Total Credits: ", return number of credits
    :param line: line to parse
    :return: <int> number of credits
    """
    if line.find("Credits") != -1:
        return find_successor(line, "Credits")


def find_prerequisite(line):
    """

    :param line:
    :return: <list> parsed expression for prerequisites
    """
    # if
    if line.find("Prerequisite") != -1:
        return True


def create_prerequisite(line):
    parsed_line = re.findall(r"[\w]+|[()]", line)
    s_arith = []
    expression = []

    i = 0
    while i < len(parsed_line):
        if parsed_line[i] in ["and", "or", "("]:
            s_arith.append(parsed_line[i])

        elif parsed_line[i] == ")":
            popped = s_arith.pop()
            while popped != "(":
                expression.append(popped)
                popped = s_arith.pop()

        else:
            c = combine_course(i, parsed_line)
            expression.append(c[0])
            i = c[1] - 1

        i += 1

    while s_arith:
        expression.append(s_arith.pop())

    return expression


def combine_course(index, parsed_line):
    """

    :param index:
    :param parsed_line:
    :return:
    """
    s = ""
    while index < len(parsed_line) and parsed_line[index] not in ["and", "or", "(", ")"]:
        s += parsed_line[index] + " "
        index += 1

    return s[:len(s) - 1], index
