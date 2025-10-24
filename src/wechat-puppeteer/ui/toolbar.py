# -*- coding: utf-8 -*-

import uiautomation

from .base import BaseButton, BaseComponent, BaseToolBar


class NavigationToolBar(BaseToolBar):

    def __init__(self, parent: BaseComponent, **kwargs):
        super().__init__(parent, name=self.i18n.get("导航"), **kwargs)

        self._init()

    def _init(self):
        self.my_button = BaseButton(self)
        self.chat_button = BaseButton(self, name=self.i18n.get("聊天"))
        self.contact_button = BaseButton(self, name=self.i18n.get("通讯录"))
        self.favorite_button = BaseButton(self, name=self.i18n.get("收藏"))
        self.file_button = BaseButton(self, name=self.i18n.get("聊天文件"))
        self.moment_button = BaseButton(self, name=self.i18n.get("朋友圈"))
        self.video_button = BaseButton(self, name=self.i18n.get("视频号"))
        self.topic_button = BaseButton(self, name=self.i18n.get("看一看"))
        self.browser_button = BaseButton(self, name=self.i18n.get("搜一搜"))
        self.mini_program_button = BaseButton(self, name=self.i18n.get("小程序面板"))
        self.mobile_button = BaseButton(self, name=self.i18n.get("手机"))
        self.setting_button = BaseButton(self, name=self.i18n.get("设置及其他"))

    def switch_to_chat_panel(self):
        self.chat_button.control.Click()

    def switch_to_contact_panel(self):
        self.contact_button.control.Click()

    def switch_to_favorites_panel(self):
        self.favorite_button.control.Click()

    def switch_to_files_panel(self):
        self.file_button.control.Click()

    def switch_to_browser_panel(self):
        self.browser_button.control.Click()

    # 是否有新消息
    def has_new_message(self):
        icon = uiautomation.Bitmap.FromControl(self.chat_button.control).ToPILImage()
        return any(p[0] > p[1] and p[0] > p[2] for p in icon.getdata())

    def has_new_friend(self):
        icon = uiautomation.Bitmap.FromControl(self.contact_button.control).ToPILImage()
        return any(p[0] > p[1] and p[0] > p[2] for p in icon.getdata())
