# ♥

_FILE_NAME = "input2.txt"
_MAX = 1000


class Solver:
    """
    Probability solver using shortest path
    """
    def __init__(self):
        self.f = None
        self.n = 0
        self.o, self.d = 0, 0
        self.graph = []
        self.length = _MAX

    def read(self, file):
        self.f = open(file, "r")
        self.n = int(self.f.readline())
        self.o, self.d = [int(i) for i in self.f.readline().split()]

    def populate(self):
        for line in self.f:
            li = [int(float(i)*1000) for i in line.split()]
            self.graph.append(li)
        print(self.graph)

    def finalize(self):
        print(self.length)
        self.f.close()

    def minimize(self, dist, browsed):
        """
        Quick minimize function
        :param dist: list of minimal lengths
        :param browsed: list of booleans in which every already browsed node are set to True
        :return: the node in which the path is minimized
        """
        val_min = _MAX
        for i in range(self.n):
            if browsed[i] is False and dist[i] < val_min:
                val_min = dist[i]
                rtrn = i
        return rtrn

    def dijkstra(self):
        """
        Quick dijkstra algo
        :return:
        """
        dist = [_MAX] * self.n
        dist[self.o] = 0
        browsed = [False] * self.n

        for i in range(self.n):
            val = self.minimize(dist, browsed)
            browsed[i] = True

            for j in range(self.n):
                if self.graph[i][j] > 0 and browsed[j] is False and dist[j] > dist[i] + self.graph[i][j]:
                    dist[j] = dist[i] + self.graph[i][j]
        self.length = dist[self.d]/1000

    def print(self):
        """
        Create human-readable table
        :return:
        """
        print("{}".format(self.n))
        print("{} {}".format(self.o, self.d))
        print('{:<3}'.format(""), end="")
        for i in range(self.n):
            print(" | "+'{:<5}'.format(i), end="")
        print(" ")
        i = 0
        for row in self.graph:
            print('{:<3}'.format(i), end="")
            for col in row:
                if col == 0.0:
                    col = ""
                print(" | "+'{:<5}'.format(col), end="")

            print(" ")
            i += 1


if __name__ == '__main__':
    s = Solver()
    s.read(_FILE_NAME)
    s.populate()
    s.dijkstra()
    s.print()
    s.finalize()

