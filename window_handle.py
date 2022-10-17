#!/usr/bin/env python
# coding: utf-8
'''
@Date    : 10/17/2022
@Author  : wp
'''
import win32gui
import win32con
import win32api


hwnd_title = {}

def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


def get_targer_window():
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t == "Your tool":
            # print (h, t)
            x, y, *o = win32gui.GetWindowRect(h)
            win32api.SetCursorPos([x+20, y+30])
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            return


if __name__ == '__main__':
    get_targer_window()
