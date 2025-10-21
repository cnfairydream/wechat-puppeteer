# -*- coding: utf-8 -*-
import time

import uiautomation

# time.sleep(5)

for child in uiautomation.GetRootControl().GetChildren():
    # print(child, child.ProcessId)
    if child.ControlTypeName == "WindowControl":
        # if child.ClassName == "ChatWnd":
        #     for control, d in uiautomation.WalkControl(child, includeTop=True):
        #         print(d, control)
        #
        #     uiautomation.Bitmap.FromControl(child.ButtonControl(Name="我在本群的昵称")).ToFile("xxx.bmp")

        # if child.ClassName == "FileListMgrWnd":
        #     for control, d in uiautomation.WalkControl(child, includeTop=True):
        #         print(d, control)
        #
        #     uiautomation.Bitmap.FromControl(child.ButtonControl(Name="清空")).ToFile("xxx.bmp")

        # if child.ClassName == "mmui::FramelessMainWindow":
        #     for control, d in uiautomation.WalkControl(child, includeTop=True):
        #         print(d, control)
        #     # print(child)
        #     child.GroupControl(ClassName="mmui::MessageView")
        #     uiautomation.Bitmap.FromControl(child.ToolBarControl()).ToFile("xxx.bmp")

        # if child.ClassName == "Qt51514QWindowIcon":
        #     print(child, child.ProcessId)
        #     uiautomation.Bitmap.FromControl(child.ToolBarControl(ClassName="mmui::XButton", Name="快捷操作")).ToFile("xxx.bmp")

        if child.ClassName == "WeChatMainWndForPC":
            for control, d in uiautomation.WalkControl(child, includeTop=True):
                print(d, control)

        #     # print(child.ButtonControl(Name="关闭"))
        #     uiautomation.Bitmap.FromControl(child.ToolBarControl(Name="导航")).ToFile("xxx.bmp")

        # if child.ClassName == "mmui::MainWindow":
        #     for control, d in uiautomation.WalkControl(child, includeTop=True):
        #         print(d, control)
        #
        #     uiautomation.Bitmap.FromControl(child.ButtonControl(ClassName="mmui::XButton", Name="快捷操作")).ToFile("xxx.bmp")

        # 菜单栏
        # if control.ControlTypeName == "ToolBarControl" and control.ClassName == "mmui::MainTabBar" and control.Name == "导航":
        #     uiautomation.Bitmap.FromControl(control).ToFile("xxx.bmp")

        # 微信、通讯录、收藏、朋友圏、视频号、搜一搜、小程序面板
        # if control.ControlTypeName == "ButtonControl" and control.ClassName == "mmui::XTabBarItem" and control.Name == "小程序面板":
        #     uiautomation.Bitmap.FromControl(control).ToFile("xxx.bmp")

        # 手机、更多
        # if control.ControlTypeName == "ButtonControl" and control.ClassName == "mmui::XButton" and control.Name == "更多":
        #     uiautomation.Bitmap.FromControl(control).ToFile("xxx.bmp")

        # 工具栏
        # if control.ControlTypeName == "ToolBarControl" and control.ClassName=="mmui::TitleBar":
        #     uiautomation.Bitmap.FromControl(control).ToFile("xxx.bmp")

        # 最大化、最小化、关闭
        # if control.ControlTypeName == "ButtonControl" and control.ClassName=="mmui::XButton" and control.Name=="最小化":
        #     uiautomation.Bitmap.FromControl(control).ToFile("xxx.bmp")
