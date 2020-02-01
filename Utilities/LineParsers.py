import re
import string


####################################
#    STRING FUNCTIONS
###################################
def find_total_credits(line):
    words = line.split()
    for i in range(len(line)):
        if words[i] == "Credits:":
            return int(words[i + 1])


def find_all_code_requirement(line):
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
            if parsed[i - 1].isdigit():
                num = int(parsed[i - 1])
            elif (i + 1) < len(parsed) and parsed[i + 1].isdigit():
                num = int(parsed[i + 1])

    return num, t_string, l_courses


def combine_text(line):
    """
    Used in
    """
    new_line = []

    for i in range(len(line)):
        if line[i].lower() == "designated":
            new_line.append(' '.join(line[i:line.index("test")]).lower())

        else:
            new_line.append(line[i])

    return new_line

def get_all_courses(line):
    """
    returns list of all raw courses in line
    :param line: (string) line to find courses in
    [Course.py]
    """
    ret_array = []
    line = line.translate(str.maketrans('', '', string.punctuation))
    parsed = line.split()

    for i in range(len(parsed)):
        if parsed[i].isupper() and len(parsed[i]) >1:
            try:
                ret_array.append(parsed[i]+parsed[i+1])
            except IndexError:
                pass
            i += 1

    return ret_array





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
            removed_titles.append(row[row.find(':') + 1:])
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
        if parsed_line[i] == word and (i + 1 < len(parsed_line)):
            return parsed_line[i + 1]


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

def combine_course(index, parsed_line):
    """

    :param index:
    :param parsed_line:
    :return:
    """
    s = ""
    start = index
    while index < len(parsed_line) and parsed_line[index] not in ["and", "or", "(", ")"]:
        if contains_int(parsed_line[index]) or parsed_line[index].isupper():
            s += parsed_line[index]
            index += 1
        else:
            s = ' '.join(parsed_line[start:index+1])
            index += 1

    return s[:len(s)], index

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
