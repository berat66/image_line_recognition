#!/usr/bin/python3
"""
DOCSTRING
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('input/2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thres = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
out_image = cv2.cvtColor(thres, cv2.COLOR_GRAY2RGB)

minLineLength = 20
maxLineGap = 5
threshold = 50
lines = cv2.HoughLinesP(thres, rho=1, theta=np.pi / 180, threshold=threshold, minLineLength=minLineLength,
                        maxLineGap=maxLineGap)
print(lines)
img_len = max(img.shape)
print(img.shape)
for line in lines:
    for x1, y1, x2, y2 in line:
        A = np.array([[x1, 1], [x2, 1]]).reshape(2, 2)
        b = np.array([y1, y2]).reshape(2, 1)
        x = np.linalg.solve(A, b)
        print(x)

        x1 = 0
        y1 = x1 * x[0] + x[1]
        x2 = img_len
        y2 = x2 * x[0] + x[1]
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 1)

cv2.imwrite('threshold.jpg', thres)
cv2.imwrite('gray.jpg', gray)
cv2.imwrite('houghlines3.jpg', img)