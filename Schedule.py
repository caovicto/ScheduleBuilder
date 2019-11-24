from CourseDatabase import *
from Course import *
from Major import *


class Schedule:
    def __init__(self):
        self.majordb = MajorDatabase()
        self.all_courses = {}

    def create_schedule(self, stuinfo):
        self.majordb.get_major(stuinfo.major_name).get_requirements()


class Student:
    def __init__(self, major_name):
        self.major_name = major_name





