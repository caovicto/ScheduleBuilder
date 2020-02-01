from Utilities.PriorityHeap import *
from DataStructures.CourseDatabase import *



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

        def __gt__(self, other):
            return self.course.get_code() > other.course.get_code()

        def __lt__(self, other):
            return self.course.get_code() < other.course.get_code()

        def __str__(self):
            s = str(self.course) + '\n' + \
                "prerequisites completed: " + str(self.course.is_prereq_completed()) + "\n" + \
                "in " + str(self.get_in()) + ": " + ' '.join(self.all_in_edges()) + '\n' + \
                "out: " + str(self.get_out()) + ": " + ' '.join(self.all_out_edges())

            return s

        def is_complete(self):
            return self.course.is_completed()

        def is_prerequisite_complete(self):
            return self.course.prereq_completed


        def get_code(self):
            """

            """
            return self.course.get_code()

        def get_credit(self):
            return self.course.credit_average()

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

        def get_in(self):
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

        def delete_in_edge(self, source):
            """

            """
            if self.in_edges.get(source):
                # set prereq as complete, if completed all prereqs, set prereq as complete
                self.course.complete_prereq(source)
                if self.course.is_prereq_completed():
                    del self.in_edges[source]
                    self.num_in = 0

                else:
                    del self.in_edges[source]
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

        def get_out(self):
            """

            """
            return self.num_out

        def add_out_edge(self, edge):
            """

            """
            if isinstance(edge, Graph.Edge) and not self.out_edges.get(edge.get_dest()):
                self.out_edges[edge.get_dest()] = edge
                self.num_out += 1

        def delete_out_edge(self, dest):
            """

            """
            if self.out_edges.get(dest):
                del self.out_edges[dest]
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

        # Open classes
        self.required = {}
        self.not_required = {}

    def __str__(self):
        s = ""
        for ele in self.vertex_list.values():
            s += str(ele)
        return s

    def all_vertices(self):
        """

        """
        temp = []
        for ele in self.vertex_list.values():
            if ele:
                temp.append(ele)

        return temp

    def get_vertex(self, code):
        return self.vertex_list.get(code.upper())

    def delete_edge(self, code):
        vert = self.get_vertex(code)
        if vert:
            for pre in vert.in_edges:
                try:
                    self.get_vertex(pre).delete_out_edge(code)
                except None:
                    pass

            for post in vert.out_edges:
                try:
                    self.get_vertex(post).delete_in_edge(code)
                except None:
                    pass

            del self.vertex_list[code]

    def add_to_graph(self, code, requirement):
        """
        :param code: (string) code for course
        """
        code = code.upper()
        if self.get_vertex(code) is None:
            new_course = self.courseDB.get_course(code)
            # if new_course:
            if new_course:
                new_vert = Graph.Vertex(new_course)
                # add new vertex to list
                self.vertex_list[code] = new_vert


    def update_all_edges(self):
        # add all prerequisite edges if they exist
        for ele in self.vertex_list.values():
            for course in ele.course.get_list_prerequisites():
                if self.get_vertex(course):
                    prereq_edge = Graph.Edge(course, ele.get_code())
                    ele.add_in_edge(prereq_edge)

        # update all edges
        for dest in self.vertex_list.values():
            for src in dest.all_in_edges():
                vert = self.get_vertex(src)
                if vert:
                    vert.add_out_edge(Graph.Edge(src, dest.get_code()))


    # def alias_writing(self):
    #     tier_one_writing = ["WRA101"]
    #     for course in tier_one_writing:
    #         vert = self.get_vertex(course)
    #         if vert and self.get_vertex("COMPLETION OF TIER I WRITING REQUIREMENT"):
    #             vert.out_edges.update(self.get_vertex("COMPLETION OF TIER I WRITING REQUIREMENT").out_edges)
    #             for ele in self.get_vertex("COMPLETION OF TIER I WRITING REQUIREMENT").out_edges:
    #                 dest = self.get_vertex(ele)
    #                 dest.add_in_edge(Graph.Edge(course, ele))


    def complete_course(self, code):
        """
        :return: returns list of edges to update
        """
        # r
        if code in ["WRA101"]:
            self.complete_course("COMPLETION OF TIER I WRITING REQUIREMENT")

        self.remove_from_list(code)

        completed_course = self.get_vertex(code)
        completed_course.course.complete()

        # deleting all outgoing edges
        for dest in completed_course.out_edges:
            vert = self.get_vertex(dest)
            vert.delete_in_edge(code)
            self.add_to_list(vert)


        for source in self.get_vertex(code).all_in_edges():
            self.complete_course(source)
            vert = self.get_vertex(source)
            vert.delete_out_edge(code)


    def create_potential(self):
        for course in self.vertex_list.values():
            self.add_to_list(course)


    def add_to_list(self, vert):
        if not vert.is_complete() and vert.course.name != "" and vert.is_prerequisite_complete():
            if vert.is_requirement() and self.required.get(vert.get_code()) is None:
                self.required[vert.get_code()] = vert.get_code()

            elif vert.get_out() != 0 and self.required.get(vert.get_code()) is None:
                self.not_required[vert.get_code()] = vert.get_code()


    def remove_from_list(self, code):
        try:
            del self.required[code]
        except KeyError:
            pass
        try:
            del self.not_required[code]
        except KeyError:
            pass

    def all_required(self):
        total = 0
        for ele in self.vertex_list.values():
            if ele.is_requirement():
                print(ele)
                total += ele.get_credit()

        print(total)
