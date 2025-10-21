# -*- coding: utf-8 -*-

from i18n_modern import I18nModern
from uiautomation import Control

from ..config import Settings
from ..misc.file import get_locales_dir


class NavigationBox:
    def __init__(self, control: Control, parent: Control, i18n: I18nModern = None):
        self.control: Control = control
        self.root = parent.root
        self.parent = parent
        self.top_control = control.GetTopLevelControl()

        locales = get_locales_dir() / Settings.LANG / "NAVIGATION_BOX.json"
        self._i18n = i18n if i18n else I18nModern(Settings.LANG, locales=str(locales))
        self._init()

    def _init(self):
        self.my_icon = self.control.ButtonControl()
        self.chat_icon = self.control.ButtonControl(Name=self._i18n.get('聊天'))
        self.contact_icon = self.control.ButtonControl(Name=self._i18n.get('通讯录'))
        self.favorites_icon = self.control.ButtonControl(Name=self._i18n.get('收藏'))
        self.files_icon = self.control.ButtonControl(Name=self._i18n.get('聊天文件'))
        self.moments_icon = self.control.ButtonControl(Name=self._i18n.get('朋友圈'))
        self.video_icon = self.control.ButtonControl(Name=self._i18n.get('视频号'))
        self.stories_icon = self.control.ButtonControl(Name=self._i18n.get('看一看'))
        self.browser_icon = self.control.ButtonControl(Name=self._i18n.get('搜一搜'))
        self.mini_program_icon = self.control.ButtonControl(Name=self._i18n.get('小程序面板'))
        self.phone_icon = self.control.ButtonControl(Name=self._i18n.get('手机'))
        self.settings_icon = self.control.ButtonControl(Name=self._i18n.get('设置及其他'))

    def switch_to_chat_panel(self):
        self.chat_icon.Click()

    def switch_to_contact_panel(self):
        self.contact_icon.Click()

    def switch_to_favorites_panel(self):
        self.favorites_icon.Click()

    def switch_to_files_panel(self):
        self.files_icon.Click()

    def switch_to_browser_panel(self):
        self.browser_icon.Click()

    # 是否有新消息
    def has_new_message(self):
        from wxauto.utils.win32 import capture

        rect = self.chat_icon.BoundingRectangle
        bbox = rect.left, rect.top, rect.right, rect.bottom
        img = capture(self.root.HWND, bbox)
        return any(p[0] > p[1] and p[0] > p[2] for p in img.getdata())
