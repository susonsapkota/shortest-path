import numpy as np


class Dijkstra:

    def __init__(self, vertices, edges):
        """
        :param vertices: list of vertices point
        :param edges: list of edges point

        Constructor method that initializes the vertices as well as the edges
        """
        self.vertices = vertices
        self.edges = edges
        self.size = len(self.vertices)

    def build_adj_matrix(self):
        """
        This method creates the matrix of sort which has the distance from each point
        :return: The adjacent matrix which is the the matrix containing  distance between two points
        """

        # creating zero matrix with the size of vertices available
        matrix = np.zeros((self.size, self.size))
        for edg in self.edges:
            start = self.vertices[edg[0]]
            end = self.vertices[edg[1]]
            # calculating the distance
            distance = ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
            # creating matrix to return
            i = edg[0]
            j = edg[1]
            # to - from the location will have same distance
            matrix[i, j] = distance
            matrix[j, i] = distance
        return matrix

    def find_shortest_route(self, start, end, matrix):
        """
        :param start: start point
        :param end: end point
        :param matrix: matrix containing  distance between two points
        :return: path_point : points leading to the shortest path
        """

        beginning = start
        checked_list = np.zeros(self.size)  # for storing already checked points
        distance_from_origin = np.ones(self.size) * np.inf
        # setting distance to be 0 at origin and path to be -1
        distance_from_origin[start] = 0
        short_path_from_origin = np.ones(self.size) * (-1)

        # Going through all the points to find the shortest path from starting point to each points
        while checked_list[start] == 0:
            checked_list[start] = 1
            nb_point = []
            for ind in range(len(matrix)):
                if matrix[start][ind] != 0:
                    nb_point.append(ind)
            # again checking if there is shortest path from the current point
            for second_ind in range(len(nb_point)):
                new_dist = distance_from_origin[start] + matrix[start][nb_point[second_ind]]
                if new_dist < distance_from_origin[nb_point[second_ind]]:
                    distance_from_origin[nb_point[second_ind]] = new_dist
                    short_path_from_origin[nb_point[second_ind]] = start

            # cehcking the minium distance from the origin
            num_min = 1000000
            index_num_min = -1
            for dis in range(len(distance_from_origin)):
                # have to make sure the points are not duplicate
                if distance_from_origin[dis] < num_min and checked_list[dis] == 0:
                    num_min = distance_from_origin[dis]
                    index_num_min = dis
            start = index_num_min

        # finally returning the sets of path that makes to the
        path_points = [end]
        while short_path_from_origin[end] != beginning:
            path_points.append(short_path_from_origin[end])
            end = int(short_path_from_origin[end])
        path_points.append(beginning)
        return path_points
