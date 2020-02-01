from sys import path

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

import numpy as np
import os
import string
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver

from DataStructures.RequirementDict import *


def text_requirements():
    url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=MNUN'
    # url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=UN' Majors
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    # add all majors within page
    for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
        s = ele.get('href')  # text for link
        p_num = int(s[len(s) - 4:len(s)])
        p_name = ele.text.replace('/', ' ')
        print(p_name)

        # file_path = '../Majors/'+p_name+'.txt' Majors
        file_path = '../Minors/'+p_name+'.txt'


        if not os.path.exists(file_path):
            file = open(file_path, "w")

            try:
                # initialize selenium
                url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + str(p_num)
                driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
                driver.get(url)

                # scrape requirement information from website
                info = driver.find_elements_by_xpath("//div[@class='panel-body']")
                paragraphs = info[1].text.split('\n\n')

                for i in range(len(paragraphs)):
                    file.write(paragraphs[i]+'\n')

                file.close()

                file = open(file_path, 'r')
                print(file.read())

                file.close()

                driver.close()


            except IndexError:
                pass


def process(line):
    line = nltk.word_tokenize(line)
    line = nltk.pos_tag(line)
    return line


def parse_text(program, degree):
    # Requirement Dictionary
    ReqDict = RequirementDict()

    file = open('../'+degree+'/'+program+'.txt', "r")
    all_lines = file.read().split('\n')
    ind = 0

    # filter through all lines in file
    while ind < len(all_lines):
        # Degree total credits
        if all_lines[ind].find('Required Credits') == 0:
            ReqDict.set_credit(int(all_lines[ind].split()[2]))


        remove = ['Residency', 'Distribution']
        # Requirement
        if all_lines[ind].find('Requirement') == 0 and not any(word in all_lines[ind] for word in remove):
            # create requirement
            title = all_lines[ind]
            name = title[title.find(':') + 1:]

            # if an alternative requirement
            if all_lines[ind].find('Alternative') != -1:
                key = ReqDict.match(name.split()[-1])
                requirement = ReqDict.find(key)

            # if not alternative requirement
            else:
                requirement = Requirement(name)
                key = name


            ind += 1

            # Requirement Body
            body = ""
            while ind < len(all_lines) and all_lines[ind].find('Requirement') == -1:
                body += all_lines[ind] + '\n'
                # increment until requirement body is completed
                ind += 1


            # collect options for requirement from requirement body
            sub_sections = re.split('\n', body)
            new_sections = []
            j = 0
            while j < len(sub_sections):
                if ":" in sub_sections[j]:
                    sub = sub_sections[j] + " "
                    j += 1
                    while j < len(sub_sections) and ":" not in sub_sections[j]:
                        sub += sub_sections[j] + " "
                        j += 1

                    new_sections.append(sub)
                    j -= 1

                j += 1


            # Every option to fulfil requirement
            for line in new_sections:
                if line.find('from') != -1:
                    # create option
                    parse = process(line)

                    # print('\n', "[" + line + "]")

                    # Option variables
                    num = None
                    type = ""
                    courses = []

                    # find number for credit/course and type
                    for i in range(len(parse)):
                        try:
                            curr = parse[i]
                            post = parse[i+1] if i+1 < len(parse) else None
                            if curr[1] == 'CD' and post and post[1].find('NN') != -1:
                                if post[0].find("course") != -1 or post[0].find("credit") != -1:
                                    type = "course" if post[0].find("course") != -1 else "credit"
                                    num = curr[0]
                                    break

                        except IndexError:
                            pass


                    # finding courses
                    parse = process(line[line.find('from'):]) # strip to find courses or key words
                    for i in range(len(parse)):
                        try:
                            curr = parse[i]
                            post = parse[i+1] if i+1 < len(parse) else None
                            if (curr[1] == '$' or curr[1].find('NN') != -1) and post and post[1] == 'CD':
                                courses.append(curr[0]+post[0])
                                # print(curr[0]+post[0])
                            elif curr[1].find('NN') != -1:
                                courses.append(curr[0])
                                # print(curr[0])

                        except IndexError:
                            pass

                    try:
                        filtered_courses = []
                        for ele in courses:
                            filter = ['course', 'credit', 'number', 'set', 'any', 'track', 'transfer']
                            if not any([x in ele.lower() for x in filter]) and ele not in filtered_courses:
                                filtered_courses.append(ele)

                        option = Option(int(num), type, filtered_courses)
                        requirement.add(option)

                    except (TypeError, ValueError) as e:
                        pass


            # decrement index to account for additional increment
            ReqDict.add_req(requirement)
            # print(ReqDict.find(key))
            ind -= 1

        # increment index to search for requirement titles
        ind += 1

    return ReqDict





