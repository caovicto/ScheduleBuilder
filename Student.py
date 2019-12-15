from CourseDatabase import *
from Course import *
from CourseGraph import *

from ProgramDatabase import *
from Program import *


class Student:
    def __init__(self, major_list=[], minor_list=[], past_classes=[], semesters_left=8):
        """

        """
        # CourseDatabase
        self.courseDB = CourseDatabase()

        new_course = self.courseDB.get_course("CSE320")
        print(new_course)

        # # MajorDatabase
        self.programDB = ProgramDatabase()
        self.catalogue = []
        #
        # # Graph of requirements
        # self.graph = Graph()

        # Initialize Graph from database
        # self.configure_graph(major_list, minor_list, past_classes)


    def configure_graph(self, major_list=[], minor_list=[], past_classes=[]):
        """
        Configure graph from programs
        """
        for major in major_list:
            m_number, m_name = self.programDB.get_major(major)


    def add_past_course(self, course_name):
        # set course as taken within
        c_code = course_name.split()[0]
        courseDB = self.all_courses.get(c_code)

        # courseDB.set_complete()
        # self.courses_taken[course_name] = course_name
