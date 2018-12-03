import sys
from queue import Queue

import numpy as np

import cv2

drawing = False
mode = False
ix, iy = -1, -1


def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)


img = np.zeros((100, 100, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

length = 130

cv2.circle(img, (50, 10), 5, (0, 0, 255), -1)
cv2.circle(img, (50, 90), 5, (0, 255, 0), -1)

grid = np.zeros((20, 20))


def dot(x, y, back):
    cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
    print(x, y)
    for i in [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]:
        if back == (-1, 1) and i == (1, -1):
            continue
        if back == (0, 1) and i == (0, -1):
            continue
        if back == (1, 1) and i == (-1, -1):
            continue
        if back == (1, 0) and i == (-1, 0):
            continue
        if back == (1, -1) and i == (-1, 1):
            continue
        if back == (0, -1) and i == (1, 1):
            continue
        if back == (-1, -1) and i == (1, 1):
            continue
        if back == (-1, 0) and i == (1, 0):
            continue
        nx = x + i[0] * length
        ny = y + i[1] * length
        if nx > 512 or ny > 512:
            continue
        if nx < 0 or ny < 0:
            continue
        # if img[nx, ny, 2] == 255:
        #     return
        dot(nx, ny, i)


# sys.setrecursionlimit(1500000)
# dot(256, 256, ())

# find = False
# while find:
#     pass

while True:
    cv2.imshow('image', cv2.resize(img, (0, 0), fx=10, fy=10))
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
