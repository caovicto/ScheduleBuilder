from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from course import *

import json

def find_c_info(line, c_code):
    """

    :param line:
    :param c_code:
    :return:
    """
    if len(line) >= 9 and line[:3] == c_code and is_int(line[4:6]) and line[9].isupper():
        return line[:6], line[:9]

def find_credit(line):
    """

    :param line:
    :return:
    """
    if line[:14] == "Total Credits: ":
        return int(line[15])

def find_prerequisite(line):
    """

    :param line:
    :return:
    """
    if line[:12] == "Prerequisite:":
        n_line = next(line)
        prereq = ""
        while n_line != "Description:":
            prereq += n_line
            n_line = next(line)

        stack_prereq = []
        pr = []
        stack_num = 0
        for word in prereq:
            if word == "(":





def parse_file(file_scrape):
    """

    :param file_scrape:
    :return:
    """
    # variables for file scraping
    document = open(file_scrape, 'rb')

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # variables
    course = Course()
    c_code = "CSE" # course code

    # loop for each line in file
    for pg in PDFPage.get_pages(document):
        interpreter.process_page(pg)
        layout = device.get_result()
        for ele in layout:
            if isinstance(ele, LTTextBoxHorizontal):

                for row in ele.get_text().split('\n'):
                    if course.is_complete():
                        course = Course()

                    else:
                        # check if row contains course info
                        if find_c_info(row, c_code):
                            course.set_course_num(find_c_info(row, c_code)[0])
                            course.set_course_num(find_c_info(row, c_code)[1])

                        # check if credits
                        elif find_credit(row):
                            course.set_credits(find_credit(row))

                        elif find_prerequisite()



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


# file_scrape = input("Enter pdf: ")
file_s = "../courses/cse.pdf"
parse_file(file_s)


