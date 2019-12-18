from Course import *

class Semester:
    def __init__(self, credit_max):
        """
        self.credit_max: (int) maximum credits per sem
        self.credits: (int) total credits in semester
        self.schedule: (list<Courses>) list of courses in the semester
        """
        self.credit_max = credit_max
        self.credits = 0
        self.schedule = []
        self.full = False

    def add_course(self, course):
        """
        :param course: (Course) course object to add to schedule
        """
        if self.credits+course.credit_average() <= self.credit_max:
            self.schedule.append(course)
            self.credits += course.credit_average()

        else:
            self.full = True

