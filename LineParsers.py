import re
import string


####################################
#    STRING FUNCTIONS
###################################

def find_all_codes(line):
    """

    :param line:
    :return: (tuple)
    """
    parsed = line.split()
    l_courses = []
    t_string = ""
    num = 0

    # finding requirement within line
    for i in range(len(parsed)):
        word = parsed[i]

        # collecting course code
        if word[0].isupper() and contains_int(word):
            code = word.translate(str.maketrans('', '', string.punctuation))
            l_courses.append(code)

        # collecting number of credits/courses
        elif word.islower() and ("credit" in word or "course" in word):
            t_string = word[0:6]

            # find number for requirement
            if parsed[i-1].isdigit():
                num = int(parsed[i-1])
            elif (i+1) < len(parsed) and parsed[i+1].isdigit():
                num = int(parsed[i+1])

    return num, t_string, l_courses


def remove_titles(paragraph):
    """
    Strips titles from lines in paragraph
    :param paragraph: lots of text
    :return: (list) information lines
    """
    removed_titles = []

    # looping through block of text
    for row in paragraph.split('\n'):
        # removing titles
        if row.find(':') != -1:
            removed_titles.append(row[row.find(':')+1:])
        else:
            removed_titles.append(row)

    return removed_titles


def int_present(line):
    """
    Finds first int within the line
    :param line: string to parse
    :return: (int) first int found
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



####################################
#    CHAR FUNCTIONS
###################################

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

