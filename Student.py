from CourseDatabase import *
from Course import *
from Major import *
from CourseGraph import *


class Student:
    def __init__(self, major_list=[], minor_list=[], semesters_left=8):
        # MajorDatabase of all Majors
        self.majorDB = MajorDatabase()
        self.catalogue = [["Majors"], ["Minors"]]
        self.catalogue[0].extend(major_list)
        self.catalogue[1].extend(minor_list)

        # Dictionary of course databases needed for major
        self.graph = Graph()
        for ele in range(0, 2):
            for i in range(1, len(self.catalogue[ele])):
                m = self.majorDB.get_major(self.catalogue[ele][i])  # major object
                self.graph.add_to_graph(m.list_classes())

        # elements to add to graph
        self.courses_taken = {}

        self.g = Graph()

        self.semesters_left = semesters_left

    # def create_schedule(self):

    def add_past_course(self, course_name):
        # set course as taken within
        c_code = course_name.split()[0]
        courseDB = self.all_courses.get(c_code)

        courseDB.set_complete()
        self.courses_taken[course_name] = course_name
