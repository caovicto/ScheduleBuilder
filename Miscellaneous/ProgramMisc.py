def initialize_requirements(self):
    """
    Get requirements for program
    """
    # initialize selenium
    url = 'https://reg.msu.edu/AcademicPrograms/ProgramDetail.aspx?Program=' + self.program_number
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    driver.get(url)

    # scrape requirement information from website
    info = driver.find_elements_by_xpath("//div[@class='panel-body']")
    paragraphs = info[1].text.split('\n\n')

    counter = 0

    # parse website information
    for i in range(len(paragraphs)):
        # finds total credits for program
        if paragraphs[i].find("Required Credits:") != -1:
            self.credits = find_total_credits(paragraphs[i])
            print("CREDITS", self.credits, "\n")

        # str
        else:
            # print(paragraphs[i])
            raw_courses = remove_titles(paragraphs[i])
            req = self.Requirement()

            # print(raw_courses, '\n')

            for row in raw_courses:
                info = find_all_code_requirement(row)

                if len(info[2]) != 0 and info[0] != 0:
                    new_req = self.ReqSet(info[0], info[1], info[2])
                    req.add_req(new_req)

            # add requirement to requirement list
            self.requirements.append(req)

    driver.close()