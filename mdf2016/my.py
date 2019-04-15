import copy
from operator import itemgetter
import math
import colorsys

_FILE_NAME = "input4.txt"

_HEADER = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"{} {} {} {}\">"
_FOOTER = "</svg>"
_BG = "<path fill=\"#272327\" d=\"M{0} {1}h{2}v{3}h-{2}z\" color=\"#000\"/>"
_CIRCLE = "<circle cx=\"{0}\" cy=\"{1}\" r=\".15\" fill=\"#c3c3be\" color=\"#000\"/>"
_LINE_L = "<path fill=\"#{0}\" stroke=\"#{0}\" stroke-opacity=\"{1}\" stroke-linecap=\"round\" stroke-width=\".1\" " \
          "d=\"M{2} {3}l{4} {5}\" " "color=\"#000\" overflow=\"visible\" " \
          "style=\"isolation:auto;mix-blend-mode:normal\"/> "
_LINE_H = "<path fill=\"#{0}\" stroke=\"#{0}\" stroke-opacity=\"{1}\" stroke-linecap=\"round\" stroke-width=\".1\" " \
          "d=\"M{2} {3}h{4}\" " "color=\"#000\" overflow=\"visible\" style=\"isolation:auto;mix-blend-mode:normal\"/> "
_LINE_V = "<path fill=\"#{0}\" stroke=\"#{0}\" stroke-opacity=\"{1}\" stroke-linecap=\"round\" stroke-width=\".1\" " \
          "d=\"M{2} {3}v{4}\" " "color=\"#000\" overflow=\"visible\" style=\"isolation:auto;mix-blend-mode:normal\"/> "
_ENDL = "\n"
_TAB = "\t"

X_MAX = 0
X_MIN = 0
Y_MAX = 0
Y_MIN = 0

Distances = {}
Browsed = []

_BASE_HUE = 131 / 255

# ''.join([hex(int(i*255))[2:] for i in colorsys.hsv_to_rgb(131/255, .6, .6)])


def init():
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

    X_MAX = max(lines, key=itemgetter(0))[0]
    X_MIN = min(lines, key=itemgetter(0))[0]
    Y_MAX = max(lines, key=itemgetter(1))[1]
    Y_MIN = min(lines, key=itemgetter(1))[1]
    MAX_D = (math.sqrt((Y_MAX - Y_MIN) ** 2 + (X_MAX - X_MIN) ** 2))

    OUT = ""
    OUT += _HEADER.format(X_MIN - 1, Y_MIN - 1, X_MAX + 2, Y_MAX + 2) + _ENDL
    OUT += _TAB + _BG.format(X_MIN - 1, Y_MIN - 1, X_MAX + 2, Y_MAX + 2) + _ENDL

    return lines

def dist2(lines):
    global MAX_D
    global Distances
    prop = {}
    brow = []
    spanning = True

    l = lines[0]

    print(Distances)

    d2 = {k: v for k, v in filter(lambda t: l in t[0], Distances.items())}

    min_node = min(d2, key=d2.get)
    dmin = Distances[min_node]
    print(dmin)

    #minval = 1
    #print(list(filter(lambda x: Distances[x] == minval, Distances)))

    #min(Distances, key=itemgetter(0))[0]

    brow.append(min_node[0])
    brow.append(min_node[1])
    prop[min_node] = Distances.pop(min_node)


    while(spanning):
        dmin = MAX_D
        #min_node = l[0]

        v_min = MAX_D
        k_min = ()

        for li in brow:

            for item in Distances.items():
                k, v = item
                if (k[0] in brow and k[1] not in brow) or (k[1] in brow and k[0] not in brow):
                    if v < v_min:
                        k_min = k
                        v_min = v
        if(k_min != ()):
            if k_min[0] not in brow:
                brow.append(k_min[0])
            if k_min[1] not in brow:
                brow.append(k_min[1])
            prop[k_min] = Distances.pop(k_min)

        print(k_min, v_min)

            #d2 = {k: v for k, v in filter(lambda t: li in t[0] and t[0][0] not in brow, Distances.items())}
            #t_node = min(d2, key=d2.get)
            #tmin = Distances[t_node]
            #if tmin < dmin:
                #min_node = t_node
                #dmin = tmin
        #d2 = {k: v for k, v in filter(lambda t: l in t[0], Distances.items())}
        #min_node = min(d2, key=d2.get)
        #print(Distances[min_node])


        #prop[min_node] = Distances.pop(min_node)

        if len(prop) == len(lines) - 1:
            spanning = False

    print("p> ",prop)
    for i in prop:
        l = i[0]
        nmin = i[1]
        #print(l, min)
        add_line("e1cf0f", 1, l[0], l[1], nmin[0] - l[0], nmin[1] - l[1])


def dist(lines):
    global OUT
    global MAX_D
    dists = {}
    brow = []

    for l in lines:
        dmin = MAX_D
        min = l[0]

        for e in lines:
            #if e != l and e not in brow:
            if e != l:
                dx, dy = e[0] - l[0], e[1] - l[1]
                d = math.sqrt(dx ** 2 + dy ** 2)

                # if (l, e) not in all and (e, l) not in all:
                    # all[(l, e)] = d

                #if d < dmin and (l, e) not in brow and (e, l) not in brow and not (True in [e == n[1] for n in brow]):
                if d < dmin and (l, e) not in brow and (e, l) not in brow and not (True in [e == n[1] for n in brow]) and not (True in [e == n[0] for n in brow]):
                    min = e
                    dmin = d

                pass
            else:
                print("> ", e)
                pass
        print("=================")

        if isinstance(l, tuple) and isinstance(min, tuple):
            brow.append((l, min))
            dists[(l, min)] = dmin
            #add_line("e1cf0f", 1, l[0], l[1], min[0] - l[0], min[1] - l[1])
            print(dmin, min)
    print(brow)
    #print(all)
    print(dists)
    for i in dists:
        l = i[0]
        min = i[1]
        #print(l, min)
        add_line("e1cf0f", 1, l[0], l[1], min[0] - l[0], min[1] - l[1])
    # print(Distances)


def browse(lines):
    global OUT
    global MAX_D
    global Browsed
    global Distances

    li = copy.deepcopy(lines)
    #dt = 1 / (math.sqrt(MAX_D))
    dt = 0.2

    for l in li:
        min = ()
        dmin = 0
        Browsed.append(l)
        for e in li:
            if e not in Browsed:
                dx, dy = e[0] - l[0], e[1] - l[1]

                d = math.sqrt(dx ** 2 + dy ** 2)

                Distances[(l, e)] = d

                if dmin == 0:
                    dmin = d
                    min = e
                if d < dmin:
                    min = e
                    dmin = d

                hue = (d / MAX_D)
                hue = dt / math.sqrt(hue) - dt
                # hue = (hue)**4
                # col = ''.join([hex(int(i*255))[2:] for i in colorsys.hsv_to_rgb(hue, .6, .6)])
                col = "48bcd1"
                add_line(col, hue, l[0], l[1], dx, dy)
        # li.remove(l)

        # if min != ():
            # add_line("e1cf0f", 1, l[0], l[1], min[0]-l[0], min[1]-l[1])

        #print(dmin, min)


def circle(lines):
    global OUT
    for l in lines:
        OUT += _TAB + _CIRCLE.format(l[0], l[1]) + _ENDL


def finalize():
    global OUT
    OUT += _FOOTER + _ENDL


def add_line(col, hue, x, y, dx, dy):
    global OUT
    if dx == 0:
        if dy == 0:
            pass
        else:
            OUT += _TAB + _LINE_V.format(col, hue, x, y, dy) + _ENDL
    else:
        if dy == 0:
            OUT += _TAB + _LINE_H.format(col, hue, x, y, dx) + _ENDL
        else:
            OUT += _TAB + _LINE_L.format(col, hue, x, y, dx, dy) + _ENDL


if __name__ == '__main__':
    global OUT
    lin = init()
    browse(lin)
    #dist(lin)

    dist2(lin)

    circle(lin)
    finalize()

    svg = open("out.svg", "w+")
    svg.write(OUT)
    svg.close()