# ♥

_FILE_NAME = "input4.txt"

_COLOR_SECOND = "48bcd1"
_COLOR_PRIMARY = "e1cf0f"
_COLOR_BACKGROUND = "272327"

_HEADER = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"{} {} {} {}\">"
_FOOTER = "</svg>"
_BG = "<path fill=\"#"+_COLOR_BACKGROUND+"\" d=\"M{0} {1}h{2}v{3}h-{2}z\" color=\"#000\"/>"
_BEGIN = "<circle cx=\"1\" cy=\"1\" r=\".15\" fill=\"none\" stroke=\"#c3c3be\" stroke-width=\".1\" color=\"#000\"/>"
_CIRCLE = "<circle cx=\"{0}\" cy=\"{1}\" r=\".15\" fill=\"#c3c3be\" color=\"#000\"/>"

_HEAT_LINE = "<path fill=\"#"+_COLOR_SECOND+"\" fill-opacity=\".14\" d=\"M{} {}H{}V{}h{}\" color=\"#000\" overflow=\"visible\" style=\"isolation:auto;mix-blend-mode:normal\"/>"

_ENDL = "\n"
_TAB = "\t"

def make_output(_o):
    svg = open("out.svg", "w+")
    svg.write(_o)
    svg.close()


class Solver:
    """
    Longest path on a given circuit
    """

    def __init__(self):
        self.f = None
        self.n = 0
        self.graph = []
        self.heat = []

    def read(self, file):
        self.f = open(file, "r")
        self.n = int(self.f.readline())
        for li in self.f:
            self.graph.append([False if i == '.' else True for i in li.strip()])
            self.heat.append([0 for _ in range(self.n)])

    def build_svg_base(self, _o):
        _o += _HEADER.format(0, 0, self.n + 2, self.n + 2) + _ENDL
        _o += _TAB + _BG.format(0, 0, self.n + 2, self.n + 2) + _ENDL
        return _o

    def add_svg_points(self, _o):
        _o += _TAB + _BEGIN + _ENDL
        for x in range(self.n):
            for y in range(self.n):
                if self.graph[y][x] is True:
                    _o += _TAB + _CIRCLE.format(x+1, y+1) + _ENDL
        return _o;

    def calculate_heat(self):
        """
        Calculate heat as an integer : The higher it is, the more door are crossed

        y : vertical position
        x : horizontal position

        it looks at the previous cases and took the max heat (cumulative)

        0 2
        1 X  => X will be 2 because max(zone) = 2

        In case the boat move down from the "2", the maximum will be 2

        Additionally, if the case is a point it will increase. This task is an post-maximum because otherwise we'd
        increase a null case.

        Because it's a cumulative based-algorithm, the maximum will be at the last column, last case

        :return: None
        """
        for y in range(self.n):
            for x in range(self.n):
                if y != 0:
                    if x != 0:
                        self.heat[y][x] = max([self.heat[y-1][x], self.heat[y][x-1], self.heat[y][x]])
                    else:
                        self.heat[y][x] = max([self.heat[y - 1][x], self.heat[y][x]])
                else:
                    if x != 0:
                        self.heat[y][x] = max([self.heat[y][x - 1], self.heat[y][x]])
                if self.graph[y][x] is True:
                    self.heat[y][x] += 1

    def layer_heat(self, layer, _o):
        """
        Add an heat layer to the output file
        :param layer: the layer index
        :param _o: the input
        :return: the modified output
        """
        ly = [[1 if i >= layer else 0 for i in j] for j in self.heat]

        sz = 11
        x = 0
        for li in ly:
            if 1 in li:
                y = li.index(1)
                dy = 10 - y
                _o += _TAB + _HEAT_LINE.format(sz, x + 1, sz - dy, x + 2, dy) + _ENDL
            x += 1
        return _o;

    def add_heat(self, _o):
        """
        create heats layers to the file
        :param _o: the original output
        :return: the modified output
        """

        heat_max = self.heat[self.n-1][self.n-1]

        print(" {} )".format(heat_max))

        for i in range(heat_max):
            if i % 10 is 0:
                print("{} / {}".format(i, heat_max))
            _o = self.layer_heat(i+1, _o)

        print("the max is {}".format(heat_max))

        return _o

    def end_svg_base(self, _o):
        _o += _FOOTER + _ENDL
        return _o

    def print(self):
        print(self.graph)
        print(self.heat)

    def finalize(self):
        self.f.close()


if __name__ == '__main__':
    OUT = ""

    print("Initializing files . . .")
    s = Solver()
    s.read(_FILE_NAME)
    OUT = s.build_svg_base(OUT)

    s.calculate_heat()
    print("Heat calculated. Adding.")
    print("Rendering . . . (", end="")
    OUT = s.add_heat(OUT)

    #s.print()

    OUT = s.add_svg_points(OUT)

    OUT = s.end_svg_base(OUT)
    s.finalize()
    make_output(OUT)
