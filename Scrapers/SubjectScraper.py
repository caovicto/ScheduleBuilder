import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def collectSubjects():
    # entering driver information
    url = 'https://reg.msu.edu/Courses/Search.aspx'
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    driver.get(url)

    selections = driver.find_element_by_id("MainContent_ddlSubjectCode")
    options = [x for x in selections.find_elements_by_tag_name("option")]
    driver.set_script_timeout(300)

    file = open("../Files/Subject.txt", "w")

    # looping through all subjects
    for text in range(1, len(options)):
        # collect subject code
        subject_element = options[text]
        subject = subject_element.get_attribute("value")
        print(subject_element.text.split())
        file.write(subject_element.text+"\n")


    file.close()
    driver.quit()



collectSubjects()
