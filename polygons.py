from argparse import ArgumentParser
from math import floor
import sys, os

## find the next point, r is row, c is column, d is direction, return (r_n, c_n, d_n).
## start searching next point from 90 degrees anticlockwise to the previous one

def next(r, c, d):
    D = {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (1, -1), 4: (0, -1), 5: (-1, -1), 6: (-1, 0), 7: (-1, 1)}

    for i in range(6):
        d_n = (d - 2 + i) % 8       
        r_n, c_n = r + D[d_n][0], c + D[d_n][1]

        if 0 <= r_n < len(l) and 0 <= c_n < len(l[0]) and l[r_n][c_n] == 1:
            return r_n, c_n, d_n

#    with open(txt_file_name, 'w') as f:
#        f.write('Cannot get polygons as expected.\n')

    print('Cannot get polygons as expected.')
    sys.exit()



## find polygon start from a point (r, c) which value is 1, return list and turn all points in it to 0.
## 0 is the initial direction, not necessary to be the real one

def polygon(r, c):
    p_list = [(r, c, 0)]            
    p_n = next(r, c, 0)

    while p_n:
        if p_n[0:2] != p_list[0][0:2]:
            p_list.append(p_n)
            p_n = next(*p_n)
        else:
            p_list[0] = p_n
            break
    
    
    i = 0
    while i < len(p_list) - 2:          # everytime when p_list changes, the index will change, redo check
        mark = 0
        for i in range(len(p_list) - 1):
            for j in range(i + 1, len(p_list)):
                if p_list[i][0: 2] == p_list[j][0: 2]:
                    p_list = p_list[: i + 1] + p_list[j + 1:]
                    mark = 1
                if mark == 1:
                    break
            if mark == 1:
                break
    
    if len(p_list) < 3:
#        with open(txt_file_name, 'w') as f:
#            f.write('Cannot get polygons as expected.\n')

        print('Cannot get polygons as expected.')
        sys.exit()

    for i in p_list:
        l[i[0]][i[1]] = 0

    return p_list


## find the vertex points of polygon p
def vertexs(p):
    pp = p + [p[0]]
    p_vertexs = []
    for i in range(len(p)):
        if pp[i][2] != pp[i + 1][2]:
            p_vertexs.append(p[i])
    return p_vertexs


## find the points in polygon, p for polygon, v for vertex

def points(p, v):
    points_in = []
    p_cor = [m[:2] for m in p]
    pp = [p[-1]] + p + [p[0]]
    p_pro = []

    for i in range(1, len(pp) - 1):
        if pp[i] in v:
            if pp[i - 1][0] > pp[i][0]:
                p_pro.append(pp[i])
            if pp[i + 1][0] > pp[i][0]:
                p_pro.append(pp[i])
        else:
            if pp[i][2] == 0 or pp[i][2] == 4:
                pass
            else:
                p_pro.append(pp[i])

    for i in range(len(l)):
        for j in range(len(l[0])):
            if (i, j) not in p_cor:
                left_points = len([m for m in p_pro if m[0] == i and m[1] < j])
                if left_points % 2 == 1:
                    points_in.append((i, j))

    return points_in


## calculate perimeter: p for polygon

def perimeter(p):
    a = len([i for i in p if i[2] % 2 == 0])
    b = len([i for i in p if i[2] % 2 == 1])
    if a == 0:
        return f'{b}*sqrt(.32)'
    if b == 0:
        return f'{a * 0.4:.1f}'
    return f'{a * 0.4:.1f} + {b}*sqrt(.32)'



## calculate area: p for polygon, v for vertexs, i for point_in

def area(p, v, i):
    return round((len(i) + (len(p) - len(v)) * 1/2 + (len(v) - 2) * 1/2) * 0.16, 2)



## rotation: v for vertex

def rotation(v):
    v_qty = len(v)
    vv = v + [v[0]]
    if v_qty % 2 == 0:
        if len(set([(v[i][0] +  v[i + int(v_qty/2)][0], v[i][1] + v[i + int(v_qty/2)][1]) for i in range(int(v_qty/2))])) == 1:
            if v_qty % 4 == 0:
                if all([all([(v[i][0] - v[i - 1][0]) ** 2 + (v[i][1] - v[i - 1][1]) ** 2 == (vv[i + m][0] - vv[i + m - 1][0]) ** 2 + (vv[i + m][1] - vv[i + m - 1][1]) ** 2 \
                        for m in range(int(v_qty/4), v_qty, int(v_qty/4))]) \
                        and len(set([(vv[i + n][2] - vv[i + n + int(v_qty/4)][2]) % 8 for n in range(0, int(v_qty * 3/4), int(v_qty/4))])) == 1 \
                        and ([(vv[i][2] - vv[i + int(v_qty/4)][2]) % 8 for n in range(0, v_qty, int(v_qty/4))][0] == 2 or 6)\
                        for i in range(int(v_qty/4))]):                     # use v for v[-1], use vv for vv(v_qty)
                    return 4
            return 2
    return 1


## convex: v for vertex

def convex(v):
    vv = v + [v[0]]
    return 'yes' if sum([(vv[i + 1][2] - vv[i][2]) % 8 for i in range(len(v))]) == 8 else 'no'



####################################### main ###########################################
## all_polygon = [(0 -- all border points -- rcd, 1 -- all vertexs -- rcd, 2 -- all in points -- rc, 3 -- depth, 4 -- color
## 5 -- perimeter, 6 -- area, 7 -- convex, 8 -- rotations), (...), ...]

parser = ArgumentParser()
parser.add_argument('--file', dest = 'file_name', required = True)
parser.add_argument('-print', dest = 'option', action = 'store_true')
args = parser.parse_args()

file_name = args.file_name.split('.')[0].split('/')[-1]
txt_file_name = file_name + '_output.txt'
tex_file_name = file_name + '.tex'


option = args.option


try:

    l = []
    with open(file_name + '.txt', 'r') as f:
        for line in f:
            line = line.split()
            if line:
                l.append(line)

    l = [[int(i) for n in m for i in n] for m in l]
    if not all([n == 0 or n == 1 for m in l for n in m]):
        raise ValueError
    if len(set([len(i) for i in l])) != 1 or len(l) < 2 or len(l) > 50 or len(l[0]) < 2 or len(l[0]) > 50:
        raise ValueError
except:
#    with open(txt_file_name, 'w') as f:
#        f.write('Incorrect input.\n')

    print('Incorrect input.')
    sys.exit()


all_polygon = []
for i, m in enumerate(l):
    for j, n in enumerate(m):
        if n == 1:
            cur_polygon = polygon(i, j)
            if cur_polygon:
                cur_vertex = vertexs(cur_polygon)
                cur_point_in = points(cur_polygon, cur_vertex)
                cur_area = area(cur_polygon, cur_vertex, cur_point_in)
                cur_perimeter = perimeter(cur_polygon)
                cur_area = area(cur_polygon, cur_vertex, cur_point_in)
                cur_rotation = rotation(cur_vertex)
                cur_convex = convex(cur_vertex)
                all_polygon.append([cur_polygon, cur_vertex, cur_point_in, 0, 0, cur_perimeter, cur_area, cur_convex, cur_rotation])

qty = len(all_polygon)

for i in range(qty):            # for depth
    for j in range(qty):
        if i != j:
            if (set([m[0:2] for m in all_polygon[j][0]]) | set([n[0:2] for n in all_polygon[j][2]])) <= set(all_polygon[i][2]):
                all_polygon[j][3] += 1
                

all_area = [i[6] for i in all_polygon]
max_area = max(all_area)
min_area = min(all_area)

if max_area == min_area:
    for i in range(qty):
        all_polygon[i][4] = 0

else:
    for i in range(qty):            # for color
        all_polygon[i][4] = floor((round(max_area - all_polygon[i][6], 2) / round(max_area - min_area, 2) * 100) + 0.5)


## genertate .txt

if not option:

#    with open(txt_file_name, 'w') as f:
#        for i, m in enumerate(all_polygon):
#            f.write(f'Polygon {i + 1}:\n'
#                    f'    Perimeter: {m[5]}\n'
#                    f'    Area: {m[6]:.2f}\n'
#                    f'    Convex: {m[7]}\n'
#                    f'    Nb of invariant rotations: {m[8]}\n'
#                    f'    Depth: {m[3]}\n')

    for i, m in enumerate(all_polygon):
        print(f'Polygon {i + 1}:')
        print(f'    Perimeter: {m[5]}')
        print(f'    Area: {m[6]:.2f}')
        print(f'    Convex: {m[7]}')
        print(f'    Nb of invariant rotations: {m[8]}')
        print(f'    Depth: {m[3]}')


    
## generate .tex

else:

    all_polygon_sorted_depth = sorted(all_polygon, key = lambda x: x[3])

    with open(tex_file_name, 'w') as f:
        f.write(r'''\documentclass[10pt]{article}
\usepackage{tikz}
\usepackage[margin=0cm]{geometry}
\pagestyle{empty}

\begin{document}

\vspace*{\fill}
\begin{center}
\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]''')
    
        f.write('\n')
        f.write(f'\draw[ultra thick] (0, 0) -- ({len(l[0]) - 1}, 0) -- ({len(l[0]) - 1}, \
{len(l) - 1}) -- (0, {len(l) - 1}) -- cycle;')

        depth_print = -1

        for i in range(qty):
            if all_polygon_sorted_depth[i][3] != depth_print:
                f.write('\n')
                depth_print = all_polygon_sorted_depth[i][3]
                f.write(f'%Depth {depth_print}')  
            f.write('\n') 
            x = [str((m[1], m[0])) for m in all_polygon_sorted_depth[i][1]]
            x = ' -- '.join(x)
            f.write(f'\\filldraw[fill=orange!{all_polygon_sorted_depth[i][4]}!yellow] {x} -- cycle;')

        f.write('\n')
        f.write(r'''\end{tikzpicture}
\end{center}
\vspace*{\fill}

\end{document}''')
        f.write('\n')
    

#    os.system('pdflatex ' + tex_file_name)
#    for file in (file_name + ext for ext in ('.aux', '.log')):
#        os.remove(file)

                

        









    





