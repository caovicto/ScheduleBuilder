from selenium import webdriver


class CourseDict:
    def __init__(self):
        self.coursedict = {}

        file = open('../Dictionary/CourseDict.txt', 'r')
        for line in file.read().split('\n'):
            try:
                parse = line.split()
                code = parse[0]
                name = ' '.join(parse[1:])

                self.coursedict[code] = name

            except IndexError:
                pass

        file.close()

        # for key, value in self.coursedict.items():
        #     print(key, ':', value)


def create_file():
    # entering driver information
    url = 'https://reg.msu.edu/Courses/Search.aspx'
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    driver.get(url)

    selections = driver.find_element_by_id("MainContent_ddlSubjectCode")
    options = [x for x in selections.find_elements_by_tag_name("option")]

    file = open('../Dictionary/CourseDict.txt', 'w')

    # looping through all subjects
    for text in range(1, len(options)):
        # collect subject code
        subject_element = options[text]
        name = subject_element.get_attribute("text")

        file.write(name+'\n')


    file.close()

    print("\n\nDONE\n\n")
    driver.quit()


# create_file()
coursedict = CourseDict()
