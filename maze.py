import numpy as np

from astar import AStar
import math
import cv2


def make_maze(w=30, h=30):
    from random import shuffle, randrange
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    result = ''
    for (a, b) in zip(hor, ver):
        result = result + (''.join(a + ['\n'] + b)) + '\n'
    return result.strip()


def drawmaze(maze, set1=[], c='#'):
    set1 = list(set1)
    lines = maze.strip().split('\n')
    width = len(lines[0])
    height = len(lines)
    result = ''
    for j in range(height):
        for i in range(width):
            if (i, j) in set1:
                result = result + c
            else:
                result = result + lines[j][i]
        result = result + '\n'
    return result


class MazeSolver(AStar):

    def __init__(self, maze):
        self.lines = maze.strip().split('\n')
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def heuristic_cost_estimate(self, n1, n2):
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        return 1

    def neighbors(self, node):
        x, y = node
        return [(nx, ny) for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if
                0 <= nx < self.width and 0 <= ny < self.height and self.lines[ny][nx] == ' ']


size = 20
m = make_maze(size, size)

w = len(m.split('\n')[0])
h = len(m.split('\n'))

start = (1, 1)
goal = (w - 2, h - 2)

foundPath = list(MazeSolver(m).astar(start, goal))

img = np.zeros((100, 100, 3), np.uint8)
cv2.namedWindow('image')

drawmaze(m, list(foundPath))

cv2.imshow('image', img)
cv2.waitKey(1)

cv2.destroyAllWindows()
