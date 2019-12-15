import re

def create_prerequisite(index, parsed_line, expression, paren):
    """

    :param index:
    :param parsed_line:
    :param expression:
    :param paren:
    :return:
    """
    # break out if fully done with parsing expression
    if index == len(parsed_line):
        return

    # recusive call for sub expression
    elif parsed_line[index] == "(":
        paren.append("(")
        expression.extend([create_prerequisite(index+1, parsed_line, expression, paren)])

        find_paren = False
        while parsed_line[index] != ")" and not find_paren:
            if parsed_line[index] == ")":
                find_paren = True
            index += 1

        create_prerequisite(index+1, parsed_line, expression, paren)


    # base case
    else:
        last = index+1
        while last != len(parsed_line) and parsed_line[last] not in ["(", ")"]:
            last += 1

        sub_expression = []

        # if only one expression
        if last == index + 2:
            if paren:
                paren.pop()
                return combine_course(index, parsed_line)
            else:
                expression.append(combine_course(index, parsed_line))

        # if multiple expression
        else:
            # if ands
            if "and" in parsed_line[index:last]:
                # combine sub expression
                while index != last:
                    if parsed_line[index] == "concurrently":
                        sub_expression.append("concurrently")

                    elif len(parsed_line[index]) == 3 or len(parsed_line[index]) == 2:
                        sub_expression.append([combine_course(index, parsed_line)])
                        index += 1

                    elif (parsed_line[index].islower() or not contains_int(parsed_line[index])) and parsed_line[index] != "and":
                        break

                    index += 1

            # if ors
            else:
                # combine sub expression
                while index != last:
                    if parsed_line[index] == "concurrently":
                        sub_expression.append("concurrently")

                    elif len(parsed_line[index]) == 3 or len(parsed_line[index]) == 2 and parsed_line[index] != "or":
                        sub_expression.append(combine_course(index, parsed_line))
                        index += 1

                    elif (parsed_line[index].islower() or not contains_int(parsed_line[index])) and parsed_line[index] != "or":
                        break

                    index += 1

            # add sub_expression to
            if paren:
                paren.pop()
                return sub_expression
            else:
                expression.extend(sub_expression)


        # recursive call if not stack call
        create_prerequisite(last, parsed_line, expression, paren)


def combine_course(index, parsed_line):
    """

    :param index:
    :param parsed_line:
    :return:
    """
    return parsed_line[index]+" "+parsed_line[index+1]

def contains_int(s):
    """

    :param s:
    :return:
    """
    for c in s:
        if is_int(c):
            return True

    return False

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

s = "(EGR 100 or ECE 101) and ((MTH 132 or concurrently) or (MTH 152H or concurrently) or (LB 118 or concurrently))"
parsed_line = re.findall(r"[\w]+|[()]", s)
# parsed_line = ["(", "MTH", "103", "or", "MTH", "102B", ")", "and", "(", "CSE", "100", "and", "CSE", "102", ")"]
expression = []
paren = []
create_prerequisite(0, parsed_line, expression, paren)
for ele in expression:
    print(ele)
