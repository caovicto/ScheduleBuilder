import re
import time
import sqlite3
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
        self.path = "/home/victoria/ScheduleBuilder/course_database/db.sqlite3"
        self.create_database()

    def db_connect(self):
        con = sqlite3.connect(self.path)
        return con

    def create_database(self):
        con = self.db_connect()
        cur = con.cursor()


        # entering driver information
        url = 'https://reg.msu.edu/Courses/Search.aspx'
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        driver.get(url)

        selections = driver.find_element_by_id("MainContent_ddlSubjectCode")
        options = [x for x in selections.find_elements_by_tag_name("option")]
        driver.set_script_timeout(300)

        for i in range(1, len(options)):
            subject_element = options[i]
            subject = subject_element.get_attribute("value")

            # add to sql
            course_sql = """
            CREATE TABLE """ + subject + """ (
                id integer PRIMARY KEY,
                name text NOT NULL,
                credits integer NOT NULL,
                prerequisite text) """
            cur.execute(course_sql)

            try:
                # selecting subject code
                # select = "//select[@id='MainContent_ddlSubjectCode']/option[@value='" + subject + "']"
                subject_element.click()

                # submission
                driver.find_element_by_xpath("//input[@id='MainContent_btnSubmit']").click()

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

                # Creating course infromation
                for i in range(len(course_name)):
                    try:
                        course_info = info[i].text.split('\n')
                        heading = course_name[i].text.split()

                        # print(heading)
                        # print(course_info)

                        # start
                        # course = Course()
                        # course.set_course_num(' '.join(heading[0:2]))
                        # course.set_name(' '.join(heading[2:]))

                        # check if credits
                        for line in range(len(course_info)):
                            # print(course_info[line])
                            if find_credit(course_info[line]):
                                # course.set_credits(find_credit(course_info[line]))
                                pass

                            if find_prerequisite(course_info[line]):
                                prereq = course_info[line + 1]
                                # course.set_prerequisite(create_prerequisite(prereq))
                                break

                        # check if row contains course info
                        # self.add_course(course)
                        # course.print_course()

                    except IndexError:
                        break

            except (NoSuchElementException, TimeoutException) as e:
                pass

        driver.quit()

    def add_course(self, course):
        self.table[course.get_course_num()] = course

    def get_table(self):
        return self.table

    def get_course(self, code):
        """
        Gets course item from course database
        """
        if self.table.get(code):
            return self.table[code]


def subject_code(s):
    code = ""
    for letter in s:
        if is_int(letter):
            break
        code += letter

    return code


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
