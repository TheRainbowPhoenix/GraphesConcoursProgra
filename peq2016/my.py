import copy
from operator import itemgetter
import math

_FILE_NAME = "input2.txt"

_COLOR_SECOND = "48bcd1"
_COLOR_PRIMARY = "e1cf0f"
_COLOR_BACKGROUND = "272327"

_HEADER = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"{} {} {} {}\">"
_FOOTER = "</svg>"
_BG = "<path fill=\"#"+_COLOR_BACKGROUND+"\" d=\"M{0} {1}h{2}v{3}h-{2}z\" color=\"#000\"/>"
_CIRCLE = "<circle cx=\"{0}\" cy=\"{1}\" r=\"{2}\" fill=\"#c3c3be\" color=\"#000\"/>"
_LINE_L = "<path fill=\"#{0}\" stroke=\"#{0}\" stroke-opacity=\"{1}\" stroke-linecap=\"round\" stroke-width=\"{6}\" " \
          "d=\"M{2} {3}l{4} {5}\" " "color=\"#000\" overflow=\"visible\" " \
          "style=\"isolation:auto;mix-blend-mode:normal\"/> "
_LINE_H = "<path fill=\"#{0}\" stroke=\"#{0}\" stroke-opacity=\"{1}\" stroke-linecap=\"round\" stroke-width=\"{5}\" " \
          "d=\"M{2} {3}h{4}\" " "color=\"#000\" overflow=\"visible\" style=\"isolation:auto;mix-blend-mode:normal\"/> "
_LINE_V = "<path fill=\"#{0}\" stroke=\"#{0}\" stroke-opacity=\"{1}\" stroke-linecap=\"round\" stroke-width=\"{5}\" " \
          "d=\"M{2} {3}v{4}\" " "color=\"#000\" overflow=\"visible\" style=\"isolation:auto;mix-blend-mode:normal\"/> "
_ENDL = "\n"
_TAB = "\t"

X_MAX: int = 0
X_MIN: int = 0
Y_MAX: int = 0
Y_MIN: int = 0

Distances = {}
Browsed = []

_BASE_HUE = 131 / 255


def init():
    """
    Initialize the drawing output
    """
    global X_MAX
    global X_MIN
    global Y_MAX
    global Y_MIN
    global MAX_D
    global OUT
    global N
    f = open(_FILE_NAME, "r")
    N = int(f.readline())
    lines = [tuple(int(i) for i in line.rstrip('\n').split(' ')) for line in f]

    x_min = min(lines, key=itemgetter(0))[0]
    y_min = min(lines, key=itemgetter(1))[1]

    lines = [(j[0] - x_min, j[1] - y_min) for j in lines]

    X_MAX = max(lines, key=itemgetter(0))[0]
    X_MIN = 0
    Y_MAX = max(lines, key=itemgetter(1))[1]
    Y_MIN = 0
    MAX_D = (math.sqrt((Y_MAX - Y_MIN) ** 2 + (X_MAX - X_MIN) ** 2))

    OUT = ""
    dif = 4*int(X_MAX/100)
    OUT += _HEADER.format(X_MIN - dif, Y_MIN - dif, X_MAX + 2*dif, Y_MAX + 2*dif) + _ENDL
    OUT += _TAB + _BG.format(X_MIN - dif, Y_MIN - dif, X_MAX + 2*dif, Y_MAX + 2*dif) + _ENDL

    return lines


def dist2(lines):
    """
    Search for the shortest path
    """
    global MAX_D
    global Distances
    prop = {}
    brow = []
    spanning = True

    line_item = lines[0]

    d2 = {k: v for k, v in filter(lambda t: line_item in t[0], Distances.items())}

    min_node = min(d2, key=d2.get)

    brow.append(min_node[0])
    brow.append(min_node[1])
    prop[min_node] = Distances.pop(min_node)

    while spanning:

        v_min = MAX_D
        k_min = ()

        for _ in brow:

            for item in Distances.items():
                k, v = item
                if (k[0] in brow and k[1] not in brow) or (k[1] in brow and k[0] not in brow):
                    if v < v_min:
                        k_min = k
                        v_min = v
        if k_min != ():
            if k_min[0] not in brow:
                brow.append(k_min[0])
            if k_min[1] not in brow:
                brow.append(k_min[1])
            prop[k_min] = Distances.pop(k_min)

        if len(prop) == len(lines) - 1:
            spanning = False

    for i in prop:
        line_item = i[0]
        node_min = i[1]
        add_line(_COLOR_PRIMARY, 1, line_item[0], line_item[1], node_min[0] - line_item[0], node_min[1] - line_item[1])

    return prop


def browse(lines):
    """
    Browse the graph and extract the distances. Colors can be configured
    """
    global OUT
    global MAX_D
    global Browsed
    global Distances

    li = copy.deepcopy(lines)
    # dt = 1 / (math.sqrt(MAX_D))
    dt = 0.2

    for l in li:
        Browsed.append(l)
        for e in li:
            if e not in Browsed:
                dx, dy = e[0] - l[0], e[1] - l[1]

                d = math.sqrt(dx ** 2 + dy ** 2)

                Distances[(l, e)] = d

                hue = (d / MAX_D)
                hue = dt / math.sqrt(hue) - dt
                # hue = (hue)**4
                # col = ''.join([hex(int(i*255))[2:] for i in colorsys.hsv_to_rgb(hue, .6, .6)])
                col = _COLOR_SECOND
                add_line(col, hue, l[0], l[1], dx, dy)


def circle(lines):
    global OUT
    global X_MAX
    rc = float(X_MAX/100)
    for l in lines:
        OUT += _TAB + _CIRCLE.format(l[0], l[1], rc) + _ENDL


def finalize():
    global OUT
    OUT += _FOOTER + _ENDL


def add_line(col, hue, x, y, dx, dy):
    global OUT
    global X_MAX
    width = float(X_MAX/100)
    if dx == 0:
        if dy == 0:
            pass
        else:
            OUT += _TAB + _LINE_V.format(col, hue, x, y, dy, width) + _ENDL
    else:
        if dy == 0:
            OUT += _TAB + _LINE_H.format(col, hue, x, y, dx, width) + _ENDL
        else:
            OUT += _TAB + _LINE_L.format(col, hue, x, y, dx, dy, width) + _ENDL


def calculate_length(prop):
    sz = 0
    for i in prop:
        sz += prop[i]
    return sz

if __name__ == '__main__':
    print("Rendering . . .")

    lin = init()
    browse(lin)
    prop = dist2(lin)
    circle(lin)
    finalize()

    svg = open("out.svg", "w+")
    svg.write(OUT)
    svg.close()

    print("Shortest path length = {}".format(calculate_length(prop)))

    print("Done !")
