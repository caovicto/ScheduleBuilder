from Utilities.PriorityHeap import *
from Course import *

class Graph:
    class Vertex:
        def __init__(self, item):
            """
            :param item: (Course) course item
            """
            self.item = item

            self.in_edges = {}
            self.num_in = 0

            self.out_edges = {}
            self.num_out = 0

            # retrieve information from items

        def get_item(self):
            """

            """
            return self.item

        ##############################
        #     IN EDGE FUNCTIONS
        ##############################

        def all_in_edges(self):
            """

            """
            temp = []
            for ele in self.in_edges:
                if ele:
                    temp.append(ele)
            return temp

        def num_in(self):
            """

            """
            return self.num_in

        def add_in_edge(self, edge):
            """

            """
            if isinstance(edge, Graph.Edge) and not self.in_edges.get(edge.get_source()):
                self.in_edges[edge.get_source()] = edge
                self.num_in += 1

        def delete_in_edge(self, edge):
            """

            """
            if isinstance(edge, Graph.Edge) and not self.in_edges.get(edge.get_source()):
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
        self.vertex_list = {}

    def all_vertices(self):
        """

        """
        temp = []
        for ele in self.vertex_list:
            if ele:
                temp.append(ele)

        return temp

    def add_vertex(self, v):
        """

        """
        if isinstance(v, Graph.Vertex) and not self.vertex_list.get(v.get_item()):
            del self.vertex_list[v.get_item()]

    def add_to_graph(self, course):
        """

        """
        pass


def TopologicalSort(g):
    """

    """
    copy_g = g
    heap = PriorityHeap()
    for ele in copy_g.all_vertices():
        heap.push(ele.in_num(), ele)



def remove_top(heap):
    """

    """
    num_zero = heap.all_mins()

    for i in range(num_zero):
        popped = heap.pop()
        # remove in edge incident from out edge destination
        for ele in popped.all_out_edges():
            dest = ele.get_dest()
            dest.delete_in_edge(popped)

            heap.change_priority()


