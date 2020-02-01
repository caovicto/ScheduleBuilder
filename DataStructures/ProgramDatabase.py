import os

from DataStructures.Program import *


class ProgramDatabase:
    def __init__(self):
        self.path = "/home/victoria/ScheduleBuilder/Databases/Programdb.sqlite3"
        #
        # self.connection = sqlite3.connect(self.path)
        # self.cur = self.connection.cursor()

        self.initializeMajorsFile()


    ###############################################################
    #          Initializing Databse Functions
    ###############################################################

    def create_database(self):
        """
        DO NOT USE UNLESS RECREATING DATABASE
        """
        self.initialize_database()
        self.initialize_majors()
        self.initialize_minors()

        self.list_entire_database()

    def initialize_database(self):
        """
        Generates table within
        :param name: name of the table
        """
        major_sql = """
        CREATE TABLE Major (
            name text NOT NULL,
            requirements text NOT NULL); """

        self.cur.execute(major_sql)

        minor_sql = """
        CREATE TABLE Minor (
            name text NOT NULL,
            requirements text NOT NULL); """

        self.cur.execute(minor_sql)

        self.connection.commit()
    #
    # def initialize_majors(self):
    #     """
    #     Adds all majors
    #     """
    #     url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=UN'
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #
    #     # add all majors within page
    #     for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
    #         s = ele.get('href')  # text for link
    #         p_num = int(s[len(s) - 4:len(s)])
    #         p_name = ele.text.replace('/', ' ')
    #         # print(p_name)
    #
    #         try:
    #             # initialize selenium
    #             url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + str(p_num)
    #             driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    #             driver.get(url)
    #
    #             # scrape requirement information from website
    #             info = driver.find_elements_by_xpath("//div[@class='panel-body']")
    #             paragraphs = info[1].text.split('\n\n')
    #
    #             self.add_program(p_name, '\n'.join(paragraphs), 'Major')
    #
    #             driver.close()
    #
    #
    #         except IndexError:
    #             pass
    #
    #
    #     self.connection.commit()

    def initializeMajorsFile(self):
        for filename in os.listdir("../Majors"):
            path = "Majors/"+filename
            print(path)
            f = open(path)
            for ele in f:
                print(ele)

            break


    #
    # def initialize_minors(self):
    #     # Scraping minors from website
    #     url = 'https://reg.msu.edu/AcademicPrograms/Programs.aspx?PType=MNUN'
    #     response = requests.get(url)
    #
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     # add all majors within page
    #     for ele in soup.findAll('a', attrs={'href': re.compile("^ProgramDetail")}):
    #         s = ele.get('href')  # text for link
    #         p_num = int(s[len(s) - 4:len(s)])
    #         p_name = ele.text.replace('/', ' ')
    #         # print(p_name)
    #
    #         try:
    #             # initialize selenium
    #             url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + str(p_num)
    #             driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    #             driver.get(url)
    #
    #             # scrape requirement information from website
    #             info = driver.find_elements_by_xpath("//div[@class='panel-body']")
    #             paragraphs = info[1].text.split('\n\n')
    #
    #             self.add_program(p_name, '\n'.join(paragraphs), 'Minor')
    #
    #             driver.close()
    #
    #
    #         except IndexError:
    #             pass
    #
    #     self.connection.commit()

    def add_program(self, p_name, text, p_type):
        """
        Adds program name as key, program object as value
        :param program: program Object
        """
        try:
            insert_sql = "INSERT INTO " + p_type + " (name, requirements) " + \
                         "VALUES (?, ?)"

            self.cur.execute(insert_sql,
                             (p_name, text))

            self.connection.commit()

        except sqlite3.OperationalError:
            pass



    ###############################################################
    #               Database Functions
    ###############################################################

    def list_elements_in_table(self, program):
        """
        lists all elements form table with name cCode
        """
        self.cur.execute("SELECT name, requirements FROM " + program)
        for ele in self.cur.fetchall():
            print(ele)

    def list_entire_database(self):
        """
        Lists all elements within Database
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for ele in self.cur.fetchall():
            print("***************************************************************************")
            print("\nTABLE: ", ele[0], "\n")
            self.list_elements_in_table(ele[0])

    def get_majors(self):
        """
        Lists all elements within Database
        """
        major_list = []
        self.cur.execute("SELECT name FROM Major")
        for ele in self.cur.fetchall():
            major_list.append(ele[0])

        return major_list

    def get_minors(self):
        """
        Lists all elements within Database
        """
        minor_list = []
        self.cur.execute("SELECT name FROM Minor")
        for ele in self.cur.fetchall():
            minor_list.append(ele[0])

        return minor_list

    def get_program(self, p_name, p_type):
        """
        Gets program from database
        """
        try:
            self.cur.execute("SELECT name, requirements FROM " + p_type +
                             " WHERE name='" + p_name + "'")
            ele = self.cur.fetchone()

            return ele[1]

        except sqlite3.OperationalError:
            pass
            # self.cur.execute("SELECT Pid, name FROM " + p_type)
            # for ele in self.cur.fetchall():
            #     if ele[1].find(p_name):
            #         new_program = Program(ele[0], ele[1], p_type, ele[2])
            #
            #         parse = ele[3].split('\n')
            #         for i in range(len(parse)):
            #             if parse[i].find("Requirement"):
            #                 req = Program.Requirement(parse[i][:parse[i].find("Requirement")])
            #                 inc = 1
            #
            #                 while i + inc < len(parse) and not parse[i + inc].find("Requirement"):
            #                     split_requirement = parse[i + inc].split('|')
            #                     try:
            #                         new_req = new_program.ReqSet(split_requirement[0], split_requirement[1],
            #                                                      split_requirement[2].split())
            #                         req.add_req(new_req)
            #                     except IndexError:
            #                         pass
            #                     inc += 1
            #
            #                 new_program.add_requirement(req)
            #
            #         return new_program

            return None
