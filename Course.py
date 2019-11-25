class Course:
    def __init__(self, c_num = "", name = "", cred=0, pr=[]):
        self.course_num = c_num
        self.name = name
        self.credits = cred

        self.pr_arith = pr
        self.prereqs = []
        self.postreqs = []

        self.completed = False

    # setting functions
    def set_course_num(self, c_num):
        """

        :param c_num:
        :return:
        """
        self.course_num = c_num

    def set_name(self, new_name):
        """

        :param new_name:
        :return:
        """
        self.name = new_name

    def set_credits(self, new_credits):
        """

        :param new_credits:
        :return:
        """
        self.credits = new_credits

    def set_prerequisite(self, pq):
        """

        :param pq:
        :return:
        """
        self.prereq = pq

    # getting functions
    def get_course_num(self):
        """

        :return:
        """
        return self.course_num

    def get_name(self):
        """

        :return:
        """
        return self.name

    def get_credits(self):
        """

        :return:
        """
        return self.credits

    def get_prerequisite(self):
        """

        :return:
        """
        return self.prereq

    def generate_prereqs(self):
        pass

    # information completion
    def set_complete(self):
        """

        :return:
        """
        self.completed = True

    # printing
    def print_course(self):
        """

        :return:
        """
        print(self.get_course_num(), ": ", self.get_name())
        print("Credits: ", self.get_credits())
        print("Prerequisites: ", self.get_prerequisite())

