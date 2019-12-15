from CourseDatabase import *
from Course import *
from CourseGraph import *

from ProgramDatabase import *
from Program import *


class Student:
    def __init__(self, major_list=[], minor_list=[], past_classes=[], semesters_left=8):
        """
        self.programDB: (ProgramDatabase) connection to program dtatbase to retrieve program information
        self.catalogue: (list<Program>) list of programs that student wants to fulfill
        self.graph: (Graph) graph object to create schedule
        """
        # MajorDatabase
        self.programDB = ProgramDatabase()
        self.catalogue = []

        # Graph of requirements
        self.graph = Graph()

        # # Initialize Graph from database
        # self.configure_graph(major_list, minor_list, past_classes)

        coursedb = CourseDatabase()
        new_course = coursedb.get_course("ME201")
        print(new_course)


    def configure_graph(self, major_list=[], minor_list=[], past_classes=[]):
        """
        Configure graph from programs
        """

        for major in major_list:
            m_number, m_name = self.programDB.get_program(major, "Major")
            new_major = Program(m_number, m_name, "Major")
            new_major.print_requirements()
            self.catalogue.append(new_major)

            # for course in new_major.list_courses():
            #     new_course = coursedb.get_course(course)
            #
            #     break

        for minor in minor_list:
            m_number, m_name = self.programDB.get_program(minor, "Minor")
            new_minor = Program(m_number, m_name, "Minor")
            self.catalogue.append(new_minor)



    def add_past_course(self, course_name):
        # set course as taken within
        c_code = course_name.split()[0]
        courseDB = self.all_courses.get(c_code)

        # courseDB.set_complete()
        # self.courses_taken[course_name] = course_name
