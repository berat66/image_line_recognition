#!/usr/bin/python3
"""
DOCSTRING
"""
import cv2
import numpy as np
from PIL import ImageGrab
import win32gui
import time

import win32gui, win32ui, win32con, win32api

def screenshot_test():
    hwin = win32gui.GetDesktopWindow()
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()

    handle = hwin
    rectangle = win32gui.GetWindowRect(hwin)
    return rectangle
    print(rectangle)
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, 1280, 720)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (1920, top), win32con.SRCCOPY)
    bmp.SaveBitmapFile(memdc, 'screenshot.bmp')

def get_lines(img):
    # img = cv2.imread('input/2.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    _, thres = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    minLineLength = 20
    maxLineGap = 5
    threshold = 50
    lines = cv2.HoughLinesP(thres, rho=1, theta=np.pi / 180, threshold=threshold, minLineLength=minLineLength,
                            maxLineGap=maxLineGap)
    print(lines)
    img_len = max(img.shape)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                A = np.array([[x1, 1], [x2, 1]]).reshape(2, 2)
                b = np.array([y1, y2]).reshape(2, 1)
                try:
                    x = np.linalg.solve(A, b)
                    x1 = 0
                    y1 = int((x1 * x[0] + x[1])[0])
                    x2 = img_len
                    y2 = int((x2 * x[0] + x[1])[0])
                    print(x1, y1, x2, y2)
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                except Exception as e:
                    print(e)
    return img


def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def enum_win(hwnd, windows_list):
    win_text = win32gui.GetWindowText(hwnd)
    windows_list.append((hwnd, win_text))


def main():
    # Detect the window with Tetris game
    windows_list = []
    toplist = []
    win32gui.EnumWindows(enum_win, windows_list)

    # Game handle
    game_hwnd = 0
    for (hwnd, win_text) in windows_list:
        if "Samsung" in win_text:
            print(hwnd, win_text)
            game_hwnd = hwnd
            break


    while True:
        rectangle = screenshot_test()
        print(rectangle)

        # Take screenshot
        xoff = 1920/9
        yoff = 1080/5
        rectangle = (xoff, yoff, 1920-xoff, 1080-60) # left, top, width, height
        screenshot = ImageGrab.grab(rectangle)
        img = np.array(screenshot)
        ori = img
        # img = cv2.imread('input/2.jpg')
        img = get_lines(img)
        # imS = cv2.resize(img, (1920, 1080))
        img = resize_with_aspect_ratio(img, height=800)
        cv2.imshow("Screen", img)
        cv2.waitKey(50)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # screenshot_test()
    main()