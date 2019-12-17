from Utilities.PriorityHeap import *
from Course import *
from CourseDatabase import *


class Graph:
    class Vertex:
        def __init__(self, course):
            """
            self.item: (Course) course object
            self.in_edges: (dict<edges>) list of incoming edges
            self.num_in: (int) number of incoming edges
            self.out_edges: (dict<edges>) list of outgoing edges
            self.num_out: (int) number of outgoing edges
            """
            self.course = course

            self.in_edges = {}
            self.num_in = 0

            self.out_edges = {}
            self.num_out = 0

            # retrieve information from items

        def get_code(self):
            """

            """
            return self.course.get_code()

        ##############################
        #     IN EDGE FUNCTIONS
        ##############################

        def all_in_edges(self):
            """
            :return: (list<edges) incoming edges list
            """
            temp = []
            for ele in self.in_edges:
                if ele:
                    temp.append(ele)
            return temp

        def num_in(self):
            """
            :return: (int) private variable of incoming edges
            """
            return self.num_in

        def add_in_edge(self, edge):
            """
            :param edge: (Edge) edge to add to list
            """
            if self.in_edges.get(edge.get_source()) is None:
                self.in_edges[edge.get_source()] = edge
                self.num_in += 1

        def delete_in_edge(self, edge):
            """

            """
            if self.in_edges.get(edge.get_source()):
                del self.in_edges[edge.get_source()]
                self.num_in -= 1

        ##############################
        #     OUT EDGE FUNCTIONS
        ##############################

        def all_out_edges(self):
            """

            """
            temp = []
            for ele in self.out_edges:
                if ele:
                    temp.append(ele)
            return temp

        def num_out(self):
            """

            """
            return self.num_out

        def add_out_edge(self, edge):
            """

            """
            if isinstance(edge, Graph.Edge) and not self.out_edges.get(edge.get_dest()):
                self.out_edges[edge.get_dest()] = edge
                self.num_out += 1

        def delete_out_edge(self, edge):
            """

            """
            if isinstance(edge, Graph.Edge) and not self.out_edges.get(edge.get_dest()):
                del self.out_edges[edge.get_dest()]
                self.num_out -= 1

    class Edge:
        def __init__(self, source, dest):
            """
            self.source: (string) code for source vertex
            self.dest: (string) code for destination vertex
            """
            self.source = source
            self.dest = dest

        def get_dest(self):
            """

            """
            return self.dest

        def get_source(self):
            """

            """
            return self.source

    def __init__(self):
        """
        self.courseDB: (CourseDatabase) connection to course database to retrieve course information
        """
        # CourseDatabase
        self.courseDB = CourseDatabase()

        # Vertex list
        self.vertex_list = {}

    def all_vertices(self):
        """

        """
        temp = []
        for ele in self.vertex_list:
            if ele:
                temp.append(ele)

        return temp

    def get_vertex(self, code):
        return self.vertex_list.get(code)

    def add_to_graph(self, code):
        """
        :param code: (string) code for course
        """
        if code and self.get_vertex(code) is None:
            new_course = self.courseDB.get_course(code)
            if new_course:
                new_vert = Graph.Vertex(new_course)
                # add new vertex to list
                self.vertex_list[code] = new_vert

                for ele in new_course.get_list_prerequisites():
                    prereq_edge = Graph.Edge(ele, code)
                    new_vert.add_in_edge(prereq_edge)
                    self.add_to_graph(ele)

    def update_all_edges(self):
        # for all vertex items in list
        for dest in self.vertex_list.values():
            for src in dest.all_in_edges():
                vert = self.get_vertex(src)
                vert.add_out_edge(Graph.Edge(src, dest.get_code()))
