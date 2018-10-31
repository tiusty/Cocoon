class clientSchedulerAlgorithm:

    def find_global_min(self, homes_matrix):
        '''
        Find the global minimum of the homes_matrix, basically by just finding the smallest point in the matrix and
        returning its index
        :param homes_matrix: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in
        favorited list
        :return: starting_point: the Global Minimum. This is the smallest possible distance, so the algorithm will start
        from this address
        '''
        min_time = 1000000000
        starting_point = -1
        for i in range(len(homes_matrix)):
            for j in range(len(homes_matrix[0])):
                if homes_matrix[i][j] < min_time and homes_matrix[i][j] != 0:
                    min_time = homes_matrix[i][j]
                    starting_point = i

        return starting_point

    def calculate_path(self, homes_matrix):
        '''
        Algorithm steps:
        1. Add global minimum to shortest path
        2. Calculate the smallest distance from the global minimum
        3. Make global minimum that index
        :param homes_matrix: The matrix calcualted using DistanceWrapper() with distances between every pair of homes in
        favorited list
        :return: shortest_path: list of indices that show the shortest possible path using the homes_matrix.
        '''

        global_minimum = self.find_global_min(homes_matrix)
        shortest_path = []
        while (len(shortest_path) != len(homes_matrix)):
            shortest_path.append(global_minimum)
            local_min = 10000000
            global_min_temp = global_minimum
            for i in range(len(homes_matrix[global_min_temp])):
                if i not in shortest_path:
                    if homes_matrix[global_min_temp][i] < local_min:
                        local_min = homes_matrix[global_min_temp][i]
                        global_minimum = i

        return shortest_path
