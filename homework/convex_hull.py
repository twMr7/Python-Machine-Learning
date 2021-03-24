"""
    convex_hull - example solution for the coding project homework

Author: James Chang <twmr7@outlook.com>
Date: 2021-03-22
"""
#%%
from typing import Tuple
from math import cos, sin, radians, dist
import csv
from random import randint, random, sample
import matplotlib.pyplot as plt

#%%
point2d = Tuple[float, float]

def rotate2d(point: point2d, degree: float) -> point2d:
    """rotate 2D point by specific degree
    """
    x, y = point[0], point[1]
    theta = radians(degree)
    new_x = x * cos(theta) - y * sin(theta)
    new_y = x * sin(theta) + y * cos(theta)
    return (new_x, new_y)

def gen_vertices(n_points: int, output_file='points.csv') -> list:
    """generate convex polygon vertices
    """
    # a initial point on 2D coordinates
    ptSeed = (randint(-100,100) * random(), randint(-100,100) * random())
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        # write header
        field_names = ['x', 'y']
        csvwriter.writerow(field_names)
        vertices = []
        # random sample N points within 360 degrees
        for degree in sample(range(360), k=n_points):
            new_point = rotate2d(ptSeed, degree)
            #print('rotate {}° -> {}'.format(degree, new_point))
            csvwriter.writerow(new_point)
            vertices.append(new_point)
    # return the list of vertices
    return vertices

def read_vertices(input_file='points.csv') -> list:
    """read 2D polygon vertices from csv file
    """
    with open(input_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        vertices = []
        for row in csvreader:
            if type(row[0]) is str or type(row[1]) is str:
                continue
            vertices.append((row[0], row[1]))
    # return the list of vertices
    return vertices

def quick_hull(vertices: list) -> list:
    """sorting convex polygon vertices by QuickHull
    """
    # left and right most points
    a, b = min(vertices), max(vertices)
    #print('two extrems:', a, b)
    subset = list(set(vertices) - set([a, b]))
    return partition(subset, a, b) + \
           partition(subset, b, a)

def partition(points, initial, terminal):
    """Accept a sequence of 2-D test points, 2 known extreme
    vertices, and return a subset of points list contains boundary
    vertices.  Points on the counterclockwise side of the line
    connected by 2 extreme vertices are evaluated by cross
    product of two vectors <p> x <q>, where

    p is the vector <initial point -> terminal point>, and
    q is the vector <initial point -> test point in points set>.

    After evaluating the cross products, another one of the
    extreme (farthest) point is selected with initial and
    terminal vertices to form a triangle. Only points outside
    of this triangle are considered to be the possible boundary
    vertices. Thus, those selected points except the vertices
    of triangle are partitioned recursively by the same routine
    until no any point can be found.

    Parameter:
        points - sequence type of points contains point to be tested
        initial - initial point of vector
        terminal - terminal point of demarcating vector
    Return:
        The stop condition of recursion is when there is no point
        on counterclockwise side of the demarcating vector; i.e.,
        above the line connected by 2 extreme vertices, the
        terminal vertex is return then.  Eventually, terminal
        vertex of each recursion should converge to form half
        of convex hull vertices. Concatnate 'upper' and 'lower'
        half of hull to get a full convex hull.
    """
    vectorize = lambda i,t : (t[0]-i[0], t[1]-i[1])
    crossproduct = lambda u,v : u[0]*v[1] - u[1]*v[0]
    xydiff = lambda p : abs(p[0]-initial[0]) + abs(p[1]-initial[1])

    # find points above (left to) the line by cross product
    aboveline, colinear, xprodMax = [], [], 0
    demarcater = vectorize(initial, terminal)
    #xprod = [crossproduct(bl2tr, vectorize(bl, p)) for p in subset]
    # sort cross-product descending
    #idxSort = sorted(range(len(xprod)), key=xprod.__getitem__)[::-1]
    for point in points:
        xprod = crossproduct(demarcater, vectorize(initial, point))
        if xprod > 0:
            # keep the extreme point as first element
            if xprod > xprodMax:
                xprodMax = xprod
                aboveline.insert(0, point)
            else:
                aboveline.append(point)
        elif xprod == 0:
            colinear.append(point)

    if len(aboveline) == 0:
        # points with zero cross product are on the same boundary,
        # but we need to return in the order of distance for perimeter
        # to be correctly measured.
        if len(colinear) > 0:
            # ascending sort by distance from initial vertex
            colinear = [v for k,v in sorted([(xydiff(p),p) for p in colinear])]
            colinear.append(terminal)
            return colinear
        else:
            return [terminal]

    elif len(aboveline) == 1:
        # only one point above the line, it is convex hull vertex,
        # just return it followed by terminal vertex right away.
        return [aboveline[0], terminal]
    #else:
    #    print('\t>> Above', aboveline)

    return partition(aboveline[1:], initial, aboveline[0]) + \
           partition(aboveline[1:], aboveline[0], terminal)

def calc_perimeter(vertices: list) -> float:
    """calculate perimeter of the convex hull
    """
    perimeter = 0.0
    for p,q in zip(vertices[:-1], vertices[1:]):
        perimeter += dist(p, q)
    return perimeter

def plot_polygon(vertices: list) -> None:
    """plot polygon from the vertices list.
    """
    # assumed vertices are sorted
    X, Y = zip(*vertices)
    fig, ax = plt.subplots()
    ax.plot(X, Y, 'o')
    ax.plot(X, Y, ':')
    ax.set_title('Perimeter = {}'.format(calc_perimeter(vertices)))
    plt.show()

#%%
if __name__ == "__main__":
    import argparse
    # setup options
    parser = argparse.ArgumentParser(prog='convex_hull', description='''
        convex_hull generates 2D random points that are vertices of a convex polygon.
            Generated points are written to a csv file and can be read back for processing.
        ''')
    parser.add_argument('operation', type=str, metavar='OP', choices=['gen','read'],
        help='''The operation mode, either generating new points or read it back.''')
    parser.add_argument('-n', '--num_points', type=int, metavar='N', default=10,
        help='''Specify the number of point to generate. (default = 10).''')
    parser.add_argument('-f', '--file_name', type=str, metavar='NAME', default='points.csv',
        help='''Specify the file name to write generated points or read points back.''')
    parser.add_argument('-p', '--plot_polygon', action='store_true',
        help='''Option to plot the polygon after read back points.''')
    
    # parse command line arguments
    args = parser.parse_args()

    #print('Debug args:', args.operation, args.num_points, args.output_file)
    if args.operation == 'gen':
        # restrict the lower bound
        args.num_points = max(args.num_points, 3)
        vertices = gen_vertices(args.num_points, args.file_name)
        [print(p) for p in vertices]
    elif args.operation == 'read':
        vertices = read_vertices(args.file_name)
        [print(p) for p in vertices]
        vertices_sort = quick_hull(vertices)
        if args.plot_polygon:
            plot_polygon(vertices_sort + [vertices_sort[0]])
