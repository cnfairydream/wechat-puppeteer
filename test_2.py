# -*- coding: utf-8 -*-
import itertools
import time

import uiautomation
from uiautomation import Control, FindControl
from win32gui import FindWindow

from wxauto.utils import capture


# time.sleep(5)


def show_element_tree(control: Control, depth: int = 0):
    def impl(x: Control, i: int):
        if i <= depth and x.GetChildren():
            for v in x.GetChildren():
                print(i, i * 2 * " ", v)
                impl(v, i + 1)

    print(0, control)
    impl(control, 1)


def GetAllProgeny(control: Control) -> list[list[Control]]:
    """
    Get all progeny controls.
    Return List[List[Control]], a list of list of `Control` subclasses.
    """
    all_elements = []

    def find_all_elements(element, depth=0):
        children = element.GetChildren()
        if depth == len(all_elements):
            all_elements.append([])
        all_elements[depth].append(element)
        for child in children:
            find_all_elements(child, depth + 1)
        return all_elements

    return find_all_elements(control)


def GetProgenyControl(control: Control, depth: int = 1, index: int = 0, control_type: str = None) -> Control | None:
    """
    Get the nth control in the mth depth.
    depth: int, starts with 0.
    index: int, starts with 0.
    control_type: `Control` or its subclass, if not None, only return the nth control that matches the control_type.
    Return `Control` subclass or None.
    """
    progeny = GetAllProgeny(control)
    try:
        controls = progeny[depth]
        if control_type:
            controls = [child for child in controls if child.ControlTypeName == control_type]
        if index < len(progeny):
            return controls[index]
    except IndexError:
        return None


# handle = FindWindow("WeChatMainWndForPC", None)
# control = uiautomation.ControlFromHandle(handle)
#
# print(control)
# for i in control.GetChildren():
#     print(1, "  ", i)
#     for j in i.GetChildren():
#         print(2, "    ", j)
#         for k in j.GetChildren():
#             print(3, "      ", k)
#             for l in k.GetChildren():
#                 print(4, "        ", l)
#                 for m in l.GetChildren():
#                     print(5, "          ", m)
#                     for n in m.GetChildren():
#                         print(6, "            ", n)
#
# print()

# chat = uiautomation.GetRootControl().WindowControl(ClassName="ChatWnd", Name="李倩")
# for i in chat.GetChildren():
#     print(i)
# chat_pane = FindControl(chat, lambda child, depth: child.ControlTypeName == "PaneControl" and child.ClassName== "" and depth == 1, foundIndex=1)
# toolbar = FindControl(chat_pane, lambda child, depth: child.ControlTypeName == "ToolBarControl" and child.ClassName== ""and depth == 9, foundIndex=1)
# print(toolbar)

# print(chat_pane)
# show_element_tree(chat_pane, depth=10)
# uiautomation.Bitmap.FromControl(chat).ToFile("xxx.bmp")
# show_element_tree(chat, depth=10)
# msg_box = chat.ListControl(Name="消息")
# uiautomation.Bitmap.FromControl(msg_box).ToFile("xxx.bmp")
# show_element_tree(msg_box, depth=10)
# toolbar = FindControl(chat, lambda child, depth: child.ControlTypeName == "ToolBarControl" and depth == 10, foundIndex=1)
# print(toolbar)
# uiautomation.Bitmap.FromControl(toolbar).ToFile("xxx.bmp")

# pane = FindControl(main, lambda child, depth: child.ControlTypeName == "PaneControl" and child.ClassName== "" and depth == 1, foundIndex=1)
# show_element_tree(pane, depth=2)
#
# main_pane = [i for i in main.GetChildren() if not i.ClassName][0]
# navigation_pane = FindControl(main_pane, foundIndex=1, compare=lambda child, depth: depth == 2)
# print(main_pane.ToolBarControl(Name="导航"))


wechat = uiautomation.GetRootControl().WindowControl(ClassName="WeChatMainWndForPC", Name="微信")
# show_element_tree(wechat, depth=5)
main_pane = [i for i in wechat.GetChildren() if not i.ClassName][0]

# show_element_tree(navigation_pane, 5)
#
# icon = navigation_pane.ButtonControl(Name="聊天")
# rect = icon.BoundingRectangle
# bbox = rect.left, rect.top, rect.right, rect.bottom
# img = capture(icon.GetTopLevelControl().NativeWindowHandle, bbox)
# img.save("vvv.bmp", format="BMP")
# # print(icon._bitmap)
#
# vvv = uiautomation.Bitmap.FromControl(icon).ToPILImage()
# print(any(p[0] > p[1] and p[0] > p[2] for p in vvv.getdata()))

# session_pane = FindControl(main_pane, lambda child, depth: child.ControlTypeName == "PaneControl" and depth == 2, foundIndex=1)
# print(session_pane)
#
chat_pane = FindControl(main_pane, lambda child, depth: child.ControlTypeName == "PaneControl" and depth == 2,
                        foundIndex=2)
# show_element_tree(chat_pane, depth=20)
# toolbar = FindControl(chat_pane, lambda child, depth: child.ControlTypeName == "ToolBarControl" and child.ClassName== ""and depth == 9, foundIndex=1)
# print(toolbar)

edit_box = chat_pane.EditControl()
print(edit_box)
edit_box.Show()
if not edit_box.HasKeyboardFocus:
    edit_box.MiddleClick()

edit_box.SendKeys("@周少")

at_box = wechat.PaneControl(ClassName="ChatContactMenu")
print(at_box)
if at_box.Exists(0):
    at_list = at_box.ListControl().GetChildren()
    if len(at_list) == 1:
        at_list[0].Click()

edit_box.SendKeys('{Ctrl}a', waitTime=0)
edit_box.SendKeys('{DELETE}')

if uiautomation.SetClipboardText("你好"):
    print(uiautomation.GetClipboardText())
    edit_box.SendKeys('{Ctrl}v')
    print(edit_box.GetValuePattern().Value)

# at_pane = wechat.PaneControl(ClassName="ChatContactMenu")
# show_element_tree(at_pane, depth=10)
# print(chat_pane)
# show_element_tree(chat_pane, 10)
# uiautomation.Bitmap.FromControl(chat_pane).ToFile("xxx.bmp")

# navigation_panel, session_panel, chat_panel = main_panel.GetFirstChildControl().GetChildren()

# print(navigation_panel)
# print(session_panel)
# print(chat_panel)

# show_element_tree(session_panel)

# chat_list = session_panel.ListControl(Name="会话")

# show_element_tree(chat_list)
# xxx = chat_list.GetChildren()[7]
# print(xxx.GetParentControl())
# print(xxx)
# show_element_tree(xxx)
# print()
# print(xxx.GetFirstChildControl())

# content = GetProgenyControl(xxx, 4, -1, "TextControl")
# print(content)
# title = GetProgenyControl(xxx, 2, 0, "ButtonControl")
# print(title)
# is_mute = GetProgenyControl(xxx, 4, -1, "PaneControl")
# print(is_mute)
# if is_mute:
#     uiautomation.Bitmap.FromControl(is_mute).ToFile("xxx.bmp")
# has_msg = GetProgenyControl(xxx, 2, -1, "TextControl")
# print(has_msg)
# if has_msg:
#     uiautomation.Bitmap.FromControl(has_msg).ToFile("xxx.bmp")

# show_element_tree(xxx.GetChildren()[0].GetChildren()[2])
#
# uiautomation.Bitmap.FromControl(xxx.GetChildren()[0].GetChildren()[2]).ToFile("xxx.bmp")

# uiautomation.Bitmap.FromControl(xxx.GetChildren()[0].GetChildren()[1].GetChildren()[1].GetChildren()[1]).ToFile("xxx.bmp")

# print(FindControl(xxx, lambda child, depth: child.ControlTypeName == "ButtonControl" and depth == 2, foundIndex=1))
# print(FindControl(xxx, lambda child, depth: child.ControlTypeName == "TextControl" and depth == 4, foundIndex=3))
#
# has_msg = FindControl(xxx, lambda child, depth: child.ControlTypeName == "TextControl" and depth == 2, foundIndex=1)
# print(has_msg)
# if has_msg:
#     uiautomation.Bitmap.FromControl(has_msg).ToFile("xxx.bmp")
#
# is_mute = FindControl(
#     FindControl(xxx, lambda child, depth: child.ControlTypeName == "PaneControl" and depth == 3, foundIndex=2),
#     lambda child, depth: child.ControlTypeName == "PaneControl" and depth == 1,
#     foundIndex=1,
# )
# print(is_mute)
# if is_mute:
#     uiautomation.Bitmap.FromControl(is_mute).ToFile("xxx.bmp")

# show_element_tree()

# print(chat_list.GetChildren()[0])


# for control, d in uiautomation.WalkControl(session_panel, includeTop=False):
#     print(d, control)

# for i in navigation_panel.GetChildren():
#     print(1, "  ", i)
#     print(i.Name)
#     for j in i.GetChildren():
#         print(2, "    ", j)
#         print(j.Name)
#         for k in j.GetChildren():
#             print(3, "      ", k)
#             print(k.Name)
#             for l in k.GetChildren():
#                 print(4, "        ", l)
#                 print(l.Name)

# upgrade_panel = [i for i in main.GetChildren() if i.ClassName == "UpdateWnd"][0]
# print(upgrade_panel)
# for control, d in uiautomation.WalkControl(upgrade_panel, includeTop=False):
#     print(d, control)


# for i in session_panel.GetChildren():
#     print(1, "  ", i)
#     for j in i.GetChildren():
#         print(2, "    ", j)
#         for k in j.GetChildren():
#             print(3, "      ", k)
#             for l in k.GetChildren():
#                 print(4, "        ", l)
#                 for m in l.GetChildren():
#                     print(5, "          ", m)
#                     for n in m.GetChildren():
#                         print(6, "            ", n)

# setting_panel = [i for i in main.GetChildren() if i.ClassName == "SetMenuWnd"][0]
# print(setting_panel)


# for i in control.GetChildren():
#     print(1, "  ", i)
#     for j in i.GetChildren():
#         print(2, "    ", j)
#         for k in j.GetChildren():
#             print(3, "      ", k)
#             for l in k.GetChildren():
#                 print(4, "        ", l)
#                 for m in l.GetChildren():
#                     print(5, "          ", m)
#                     for n in m.GetChildren():
#                         print(6, "            ", n)
