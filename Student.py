from CourseDatabase import *
from Course import *
from Major import *
from CourseGraph import *


class Student:
    def __init__(self, major_name, semesters_left=8):
        # MajorDatabase of all Majors
        self.majorDB = MajorDatabase()
        # Dictionary of course databases needed for major
        self.all_courses = {}

        # elements to add to graph
        self.major_name = major_name
        self.courses_taken = {}

        self.g = Graph()


        self.semesters_left = semesters_left


    def create_schedule(self):
        self.majorDB.get_major(self.major_name).get_requirements()

    def add_past_course(self, course_name):
        # set course as taken within
        c_code = course_name.split()[0]
        courseDB = self.all_courses.get(c_code)

        courseDB.set_complete()
        self.courses_taken[course_name] = course_name









