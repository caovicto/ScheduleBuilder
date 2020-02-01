class Semester:
    def __init__(self, credit_max=17):
        """
        self.credit_max: (int) maximum credits per sem
        self.credits: (int) total credits in semester
        self.schedule: (list<Courses>) list of courses in the semester
        """
        self.credit_max = credit_max
        self.credits = 0
        self.schedule = []

    def __str__(self):
        courses = ""
        for ele in self.schedule:
            courses += str(ele) + '\n'
        s = "Credits: " + str(self.credits) + '\n' + courses

        return s


    def add_course(self, course):
        """
        :param course: (Course) course object to add to schedule
        """
        self.schedule.append(course)
        self.credits += course.credit_average()

    def potential_class(self, course):
        if self.credits+course.credit_average() > self.credit_max:
            return False
        else:
            return True




