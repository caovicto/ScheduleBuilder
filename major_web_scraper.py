import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup

from major import Major
from major import MajorDatabase

url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=UN'
response = requests.get(url)


majordb = MajorDatabase()

soup = BeautifulSoup(response.text, "html.parser")
for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
    s = ele.get('href')
    m = Major(s[len(s) - 4:len(s)], ele.text)

    m.get_requirements()
    break
    # m.print_major()


chosen_major = input("Enter Major: ")





