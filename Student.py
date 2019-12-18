from CourseDatabase import *
from Course import *
from CourseGraph import *

from ProgramDatabase import *
from Program import *

from Utilities.PriorityHeap import *

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

        self.total_credits = 0

        # # Initialize Graph from database
        self.configure_graph(major_list, minor_list, past_classes)

        #


        courseDB = CourseDatabase()
        # me201 = courseDB.get_course("ME201")
        # print(me201.prerequisites.get_courses())
        #
        # me201.complete_prereq("CEM141")
        # print(me201.is_completed())
        #
        # me201.complete_prereq("MTH234")
        # print(me201.is_completed())
        #
        # me201.complete_prereq("PHY183")
        # print(me201.is_completed())



    def configure_graph(self, major_list=[], minor_list=[], past_classes=[]):
        """
        Configure graph from programs
        """
        # add all majors to program list
        for major in major_list:
            m_number, m_name = self.programDB.get_program(major, "Major")
            new_major = Program(m_number, m_name, "Major")
            new_major.print_requirements()
            self.catalogue.append(new_major)
            self.total_credits += new_major.credits

            # add all courses in list of requirements to graph
            for course in new_major.list_possible_classes():
                self.graph.add_to_graph(course)

        # add all minors to program list
        for minor in minor_list:
            m_number, m_name = self.programDB.get_program(minor, "Minor")
            new_minor = Program(m_number, m_name, "Minor")
            self.catalogue.append(new_minor)
            self.total_credits += new_major.credits

            for course in new_minor.list_possible_classes():
                self.graph.add_to_graph(course)


    def complete_course(self, code):
        # set course as taken within
        if self.graph.get_vertex(code):


    def TopologicalSort(self):
        self.graph.update_all_edges()

        for ele in self.graph.all_vertices():
            print(ele.course)
            print("in", ele.in_edges, ele.num_in)
            print("out", ele.out_edges, ele.num_out)

        # heap = PriorityHeap()
        # for val in self.graph.vertex_list.values():
        #     heap.push(val.num_in, val)
        #
        # for i in range(len(heap)):
        #     print(heap.remove_top())


    def get_major_options(self):
        return self.programDB.get_majors()


