import time
from selenium import webdriver


class Major:
    class Requirement:
        def __init__(self):
            self.number = 0
            self.req_list = []

    def __init__(self, p_number, n):
        self.program_number = p_number
        self.name = n
        self.credits = 0
        self.requirements = {}
        self.alias = []

    def get_number(self):
        return self.program_number

    def get_requirements(self):
        url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + self.get_number()
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        driver.get(url)

        results = driver.find_elements_by_xpath("//*[@id='MainContent_divDnData']")
        # header = driver.find_elements_by_xpath("//strong")
        info = driver.find_elements_by_xpath("//div[@class='panel-body']")
        # for ele in info:
        #     print(ele.text)
        # print(results)


        for i in range(len(info)):
            # if info[i].text.find("Required Credits:") != -1:
            #     n = info[i].text.split()
            #     print(n[2])
            # else:
            #     print(info[i].text)
            print(info[i].text)



        driver.close()

        time.sleep(5)




    def print_major(self):
        print(self.name)


class MajorDatabase:
    def __init(self):
        self.table = {}

    def add_major(self, major):
        name = major.name

        if not self.table.get(name):
            self.table[name] = major

    def find_course(self, n):
        found = self.table.get(n)
        if not found:
            for alt in self.alias:
                found = self.table.get(alt)
                if found:
                    break

        return found

    def print_database(self):
        print(self.table)


