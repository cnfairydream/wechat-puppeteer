# -*- coding: utf-8 -*-
import win32api
import win32con
import win32process
import win32gui
from tenacity import retry
from contextlib import suppress


def show_app_from_tray():
    pids = win32process.EnumProcesses()
    for pid in pids:
        print(pid)

show_app_from_tray()


import psutil


# def get_handle_by_process_name():
#     for proc in psutil.process_iter(["pid", "name"]):
#         if proc.info["name"] and proc.info["name"] == "WeChat.exe":
#             with suppress(psutil.NoSuchProcess):
#                 return win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, proc.pid)
#
#     return None
#
# win32gui.ShowWindow(get_handle_by_process_name(),win32con.SW_RESTORE)
