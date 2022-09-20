#!/usr/bin/env python
# coding: utf-8
'''
@Date    : 2022/7/26
@Author  : wp
'''

from threading import Thread
import tkinter as tk
from tkinter import font
from collections import deque
import webbrowser
import os

from pynput.keyboard import Listener, Key

from read_write_config import get_values
from read_write_config import get_setting_value as get_settings
from read_write_config import get_query_value as get_query


class KeyboardListener:

    def __init__(self, app):
        self.pre_key = deque(maxlen=3)
        self.app = app


    def keyboard_listener(self):
        with Listener(on_press=self.on_press) as listen:
            listen.join()


    def on_press(self, key):
        if self.pre_key:
            if key == Key.space and self.pre_key[-1] == Key.alt_l:
                self.app.max_window()

            elif key == Key.alt_l and self.pre_key[-1] == Key.space:
                self.app.max_window()

            elif key == Key.esc:
                self.app.min_window()

            elif key == Key.enter and app.root.state() == "normal":
                self.app.execute_cmd()

            elif key == Key.end and self.pre_key[-1] == Key.shift:
                # self.app.quit()
                self.app.root.destroy()

            elif key == Key.end and self.pre_key[-1] == Key.shift_r:
                print("exit")
                # self.app.quit()
                self.app.root.destroy()

        self.pre_key.append(key)
        # print(f"{key}:{self.pre_key[-1]}")


class Window(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Your tool")
        self.root.attributes("-toolwindow", True)
        self.init_settings()
        self.root.attributes("-topmost", True)

        self.pack()
        self.show_window_in_center()

        # self.root.resizable(False, False)
        self.text = tk.StringVar()
        self.tool_tip_text = tk.StringVar()
        self.all_commands = self.format_cmd_list()
        self.init_window()


    def show_window_in_center(self):
        '''
        窗口弹出位置设定
        :return:
        '''
        width = 700
        height = 80
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # print(screen_height)
        size = '%dx%d+%d+%d' % (width, height, (screen_width - width) / 2, screen_height/3)
        self.root.geometry(size)


    def init_settings(self):
        displayHeader, bgColor, alpha = get_settings("displayHeader").strip(), get_settings("bgColor").strip(), get_settings("alpha").strip()
        if displayHeader != "1":
            # 只有当这个值为1的时候才会显示关闭按钮
            self.root.overrideredirect(True)

        if bgColor:
            self.theme_color = bgColor
            self.root["background"] = self.theme_color

        if alpha:
            self.root.attributes("-alpha", alpha)


    def init_window(self):

        main_area = tk.Frame(self, background=self.theme_color)
        # main_area = tk.Frame(self)
        _font = font.Font(family='Microsoft YaHei UI', size=16)

        self.entry = tk.Entry(main_area, width=55, justify="left", border=0, font=_font, textvariable=self.text)
        self.entry.focus_set()

        isDisplayToolTip = get_settings("displayToolTip")
        if isDisplayToolTip == "1":
            self.entry.bind("<Enter>", self.show_tooltip)
            self.entry.bind("<Leave>", self.hide_tooltip)
        self.entry.pack(pady=11, ipady=12)
        main_area.pack()


    def show_tooltip(self, event):
        self.tool_tip_window = tk.Toplevel(self.root)
        self.tool_tip_window.overrideredirect(True)

        x, y, cx, cy = self.entry.bbox("insert")
        x = x + self.entry.winfo_rootx()
        y = y + cy + self.entry.winfo_rooty() + 65
        self.tool_tip_window.geometry("+%d+%d" % (x, y))

        self.tool_tip = tk.Label(self.tool_tip_window, textvariable=self.tool_tip_text, justify="left",
                      background="#ffffe0", relief="solid", borderwidth=1,
                      font=("tahoma","8","normal"))
        self.tool_tip.pack()


    def hide_tooltip(self, event):
        self.tool_tip_window.destroy()


    def format_cmd_list(self):
        website = get_values(section="website")
        local_file = get_values(section="local_file")
        sys_cmd = get_values(section="cmd")
        all_commands = {**website, **local_file, **sys_cmd}

        tmp_text = ""
        for key in all_commands:
            tmp_text = tmp_text + key + "\n"

        query_items = get_values(section="query").keys()
        for other in query_items:
            tmp_text = tmp_text + other + "\n"

        self.websites = website.keys()
        self.local_files = local_file.keys()
        self.sys_cmd = sys_cmd.keys()
        self.tool_tip_text.set(tmp_text)

        return all_commands


    def execute_cmd(self):

        cmd = self.text.get().strip()
        query_items_prefix= tuple(get_values("query").keys())

        if cmd not in self.all_commands.keys() and not cmd.startswith(query_items_prefix):
            return

        if cmd in self.websites:
            for site in self.all_commands[cmd]:
                self.open_web(site)
                self.min_window()

        try:
            if cmd in self.local_files:
                for file in self.all_commands[cmd]:
                    self.open_local_file(file)
                    self.min_window()
        except OSError:
            self.min_window()


        if cmd in self.sys_cmd:
            for site in self.all_commands[cmd]:
                os.system(site)
                self.min_window()


        if cmd.startswith(query_items_prefix):
            for item in query_items_prefix:
                if cmd.startswith(item):
                    key_word = cmd[len(item):]
                    url = get_query(item).replace("{query}", key_word)
                    self.open_web(url)
                    self.min_window()
                    break

        self.min_window()


    def max_window(self):
        self.root.deiconify()
        self.entry.focus_set()


    def min_window(self):
        if self.text.get() != "":
            self.text.set("")
        else:
            self.root.withdraw()


    def open_web(self, site):
        webbrowser.open(site)
        return


    def open_local_file(self, file):
        os.startfile(file)
        return



if __name__ == '__main__':
    root = tk.Tk()
    app = Window(root)

    listener = KeyboardListener(app)
    listen_thread = Thread(target=listener.keyboard_listener)
    listen_thread.setDaemon(True)
    listen_thread.start()

    app.mainloop()



