from Design.CourseDatabase import *
from Design.Course import *


def testGetCourse():
    coursedb = CourseDatabase()
    psy101 = coursedb.getCourse("CHS301")
    print(psy101)


testGetCourse()
