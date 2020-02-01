from DataStructures.CourseGraph import *

from DataStructures.ProgramDatabase import *

from DataStructures.Semester import *


class Student:
    def __init__(self, reqdict=[]):
        """
        self.programDB: (ProgramDatabase) connection to program dtatbase to retrieve program information
        self.catalogue: (list<Program>) list of programs that student wants to fulfill
        self.graph: (Graph) graph object to create schedule
        """
        # MajorDatabase
        self.programDB = ProgramDatabase()
        self.ReqDict = reqdict

        # Graph of requirements
        self.graph = Graph()

        self.total_credits = 0

        self.sem_list = [Semester()]

        # Initialize Graph from database
        self.configure_graph()

        coursedb = CourseDatabase()
        coursedb.list_entire_database()

    def addMajor(self, majorName):
        ele = self.programDB.get_program(majorName, "Major")
        print(ele)

    def configure_graph(self):
        """
        Configure graph from programs
        """
        # # add all courses in list of requirements to graph
        # priority = 0
        # for course in :
        #     # print(self.graph.vertex_list)
        #     self.graph.add_to_graph(course)
        #     self.graph.get_vertex(course).set_requirement()
        #     priority += 1
        #
        # # updates graph from completed class info
        # self.complete_list()
        #
        # for ele in self.graph.all_vertices():
        #     print(ele, '\n')



    def complete_list(self):
        """
        adds and completes courses within list to graph
        """

        # update all graph edges
        self.graph.update_all_edges()

    def topological_sort(self):
        self.graph.create_potential()
        self.add_classes()
        # self.graph.all_required()

    def add_classes(self):
        pass
        # required_list = sorted(self.graoh.required, key=self.graph.required.get, reverse=True)
        # for ele in list(self.graph.required):
        #     print(self.graph.required.values())
        #     self.graph.complete_course(ele)
        #
        #     popped = self.graph.get_vertex(ele)
        #
        #     self.total_credits += popped.course.credit_average()
        #
        #     if self.sem_list[-1].potential_class(popped.course):
        #         self.sem_list[-1].add_course(popped.course)
        #     else:
        #         self.sem_list.append(Semester())
        #         self.sem_list[-1].add_course(popped.course)
        #
        #
        # if len(self.graph.required) != 0:
        #     self.add_classes()
        #
        # for ele in list(self.graph.not_required):
        #     print(self.graph.not_required.values())
        #     self.graph.complete_course(ele)
        #
        #     popped = self.graph.get_vertex(ele)
        #
        #     self.total_credits += popped.course.credit_average()
        #
        #     if self.sem_list[-1].potential_class(popped.course):
        #         self.sem_list[-1].add_course(popped.course)
        #     else:
        #         self.sem_list.append(Semester())
        #         self.sem_list[-1].add_course(popped.course)
        #
        #     if len(self.graph.required) != 0:
        #         self.add_classes()


    def get_major_options(self):
        return self.programDB.get_majors()


def eligible_course(vert):
    if vert.is_requirement():
        return True
    return False
