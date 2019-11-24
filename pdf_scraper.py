# importing parsing modules
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from course import *


#######################################################
# Parsing Information from pdf lines
#######################################################

def find_c_info(line, c_code):
    """
    if line contains course code, 3 digit number. and full course name, return pair of course code and name
    :param line: line to parse
    :param c_code: course code
    :return: <pair>(course code, name)
    """
    first_word = find_successor(line, int_present(line))
    if line.find(c_code) == 0 and int_present(line) and first_word and first_word[0].isupper():
        return c_code+int_present(line), line[line.find(first_word):]


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
            i = c[1]-1

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

    return s[:len(s)-1], index


#######################################################
# Parsing PDF
#######################################################
def parse_file(file_scrape, c_code):
    """

    :param file_scrape:
    :return:
    """
    url = 'https://reg.msu.edu/Courses/Search.aspx'
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    driver.get(url)

    select = "//select[@id='MainContent_ddlSubjectCode']/option[@value='"+c_code+"']"
    driver.find_element_by_xpath(select).click()

    driver.find_element_by_xpath("//input[@id='MainContent_btnSubmit']").click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "MainContent_divSearchResults"))
        )

        course_name = driver.find_elements_by_xpath("//h3")
        info = driver.find_elements_by_xpath("//div[starts-with(@id, 'MainContent_rptrSearchResults_divMainDetails_')]")
        header = info.
        course = Course()
        temp_database = CourseDatabase(c_code)

        for i in range(len(course_name)):
            # print(course_name[i].text, info[i].text)
            course_info = info[i].text.split('\n')

            # start
            course = Course()

            course.set_course_num(find_c_info(course_name[i].text, c_code)[0])
            course.set_name(find_c_info(course_name[i].text, c_code)[1])

            # check if credits
            for line in range(len(course_info)):
                # print(course_info[line])
                if find_credit(course_info[line]):
                    course.set_credits(find_credit(course_info[line]))

                if find_prerequisite(course_info[line]):
                    prereq = course_info[line+1]
                    course.set_prerequisite(create_prerequisite(prereq))
                    break

            # check if row contains course info
            temp_database.add_course(course)
            course.print_course()

    finally:
        driver.quit()


    # print(results.text)
    # for ele in results:
    #     print(ele.get_attribute("innerHTML"))

    # time.sleep(3)

    # for ele in select:
    #     print(ele)
    # select.select_by_visible_text(c_code)
    #
    # results = driver.find_elements_by_xpath("//*[@id='MainContent_divSearchResults']")
    # # print(results)
    # for ele in results:
    #     print(ele.text)
    #



    # # variables for file scraping
    # document = open(file_scrape, 'rb')
    #
    # rsrcmgr = PDFResourceManager()
    # laparams = LAParams()
    # device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # interpreter = PDFPageInterpreter(rsrcmgr, device)
    #
    # # variables

    # window = collections.deque()
    #
    # # loop for each line in file
    # for pg in PDFPage.get_pages(document):
    #     interpreter.process_page(pg)
    #     layout = device.get_result()
    #     waiting = ["|", "/", "-", "\\"]
    #
    #     ind = 0
    #
    #     for ele in layout:
    #         # sys.stdout.write(waiting[ind])
    #         # sys.stdout.flush()
    #         # ind = (ind+1) % 4
    #         if isinstance(ele, LTTextBoxHorizontal):
    #             # splitting by line
    #             for line in ele.get_text().split('\n'):
    #                 window.append(line)
    #
    #     while window:
    #         # sys.stdout.write(waiting[ind])
    #         # sys.stdout.flush()
    #         # ind = (ind+1) % 4
    #
    #         pop = window.popleft()
    #
    # return temp_database



#######################################################
# Extra Information for parsing
#######################################################

def int_present(line):
    """

    :param line:
    :return:
    """
    parsed_line = re.findall(r"[\w]+|[()]", line)
    for ele in parsed_line:
        if is_int(ele):
            return ele

def find_successor(line, word):
    """

    :param line:
    :param word:
    :return:
    """
    parsed_line = re.findall(r"[\w]+|[()]", line)
    for i in range(len(parsed_line)):
        if parsed_line[i] == word and (i+1 < len(parsed_line)):
            return parsed_line[i+1]



def is_int(num):
    """

    :param num:
    :return:
    """
    try:
        int(num)
        return True
    except ValueError:
        return False


def contains_int(s):
    """

    :param s:
    :return:
    """
    for c in s:
        if is_int(c):
            return True

    return False


# file_scrape = input("Enter pdf: ")
file_s = "../courses/cse.pdf"
parse_file(file_s, "CSE")
# for ele in cse_database.get_table():
#     print(cse_database.get_course(ele).print_course())
