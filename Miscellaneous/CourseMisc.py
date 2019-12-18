def complete_course(l_courses, code):
    """

    """
    if type(l_courses) is list:
        for i in range(len(l_courses)):
            if type(l_courses[i]) is str and l_courses[i] == code:
                l_courses[i] = None
            elif type(l_courses[i]) is list:
                complete_course(l_courses[i], code)


def check_prereqs(l_courses):
    """

    """
    if type(l_courses) is list:
        for i in range(len(l_courses)):
            if type(l_courses[i]) is list and None not in l_courses:
                return False


def extra_prereq(courses):
    """
    "Solves" post fix course arithmetic
    """
    stack = []
    for ele in courses:
        if ele == "and":
            first = stack.pop()
            second = stack.pop()
            if type(first) is list and type(first[0]) == type(second):
                first.append([second])
            else:
                first = [[first], [second]]
            stack.append(first)

        elif ele == "or":
            first = stack.pop()
            second = stack.pop()
            if type(first) is list and type(first[0]) == type(second):
                first.append(second)
            else:
                first = [first, second]
            stack.append(first)


        else:
            stack.append(ele)

    courses = stack[0]