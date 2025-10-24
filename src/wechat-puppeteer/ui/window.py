# -*- coding: utf-8 -*-

import logging

import uiautomation

from .base import BasePane, BaseWindow
from .pane import ChatPane, SessionPane
from .toolbar import NavigationToolBar

from ..exceptions import WindowNotExist


class ChatWindow(BaseWindow):
    def __init__(self, nickname: str, **kwargs):
        super().__init__(self, class_name="ChatWnd", name=nickname, **kwargs)

        self._init()

    def _init(self):
        self.chat_pane = ChatPane(self, depth=1, index=1)
        # self.message_list = BaseList(self, name=self.i18n.get("消息"))
        # self.edit_box = BaseEdit(self, name=self.i18n.get("输入"))
        # self.send_button = BaseButton(self, name=self.i18n.get("发送"))
        # self.toolbar = BaseToolBar(self, depth=10, index=1)
        self.name = self.control.Name


class ChatRoomWindow(ChatWindow):
    ...


class MainWindow(BaseWindow):

    def __init__(self, **kwargs):
        super().__init__(self, class_name="WeChatMainWndForPC", name="微信", **kwargs)

        self._init()

    def _init(self):
        main_pane = BasePane(self, depth=1, index=1)
        self.navigation_toolbar = NavigationToolBar(main_pane)
        self.session_pane = SessionPane(main_pane, depth=2, index=1)
        self.chat_pane = BasePane(main_pane, depth=2, index=2)
        self.nickname = self.navigation_toolbar.my_button.Name

    # def _get_chatbox(
    #         self,
    #         nickname: str = None,
    #         exact: bool = False
    # ) -> ChatBox:
    #     if nickname and (chatbox := WeChatSubWnd(nickname, self, timeout=0)).control:
    #         return chatbox.chatbox
    #     else:
    #         if nickname:
    #             switch_result = self.sessionbox.switch_chat(keywords=nickname, exact=exact)
    #             if not switch_result:
    #                 return None
    #         if self.chatbox.msgbox.Exists(0.5):
    #             return self.chatbox

    def switch_chat(
            self,
            keywords: str,
            exact: bool = False,
            force: bool = False,
            force_wait: float | int = 0.5
    ):
        return self.session_pane.switch_chat(keywords, exact, force, force_wait)

    def open_separate_window(self, keywords: str) -> ChatWindow | ChatRoomWindow | None:
        if window := get_chat_window(keywords):
            logging.debug(f"{keywords} 获取到已存在的子窗口: {window}")
            return window

        self.show()

        if nickname := self.session_pane.switch_chat(keywords):
            logging.debug(f"{keywords} 切换到聊天窗口: {nickname}")
            if window := get_chat_window(keywords):
                logging.debug(f"{nickname} 获取到已存在的子窗口: {window}")
                return window
            else:
                keywords = nickname

        if result := self.session_pane.open_separate_window(keywords):
            find_nickname = result['data'].get('nickname', keywords)
            return WeChatSubWnd(find_nickname, self)

    def _get_next_new_message(self, filter_mute: bool = False):
        def get_new_message(session):
            last_content = session.content
            new_count = session.new_count
            chat_name = session.name
            session.click()
            return self.chat_pane.get_next_new_msgs(new_count, last_content)

        def get_new_session(filter_mute):
            sessions = self.session_pane.get_session()
            if sessions[0].name == self._lang('折叠的群聊'):
                self.navigation_panel.chat_icon.DoubleClick()
                sessions = self.session_pane.get_session()
            new_sessions = [
                i for i in sessions
                if i.isnew
                   and i.name != self._lang('折叠的群聊')
            ]
            if filter_mute:
                new_sessions = [i for i in new_sessions if i.ismute == False]
            return new_sessions

        if new_msgs := self.chat_pane.get_new_msgs():
            logging.debug("获取当前页面新消息")
            return new_msgs
        elif new_sessions := get_new_session(filter_mute):
            logging.debug("当前会话列表获取新消息")
            return get_new_message(new_sessions[0])
        else:
            self.session_pane.back_to_top()
            if new_sessions := get_new_session(filter_mute):
                logging.debug("当前会话列表获取新消息")
                return get_new_message(new_sessions[0])
            else:
                self.navigation_panel.chat_icon.DoubleClick()
            if new_sessions := get_new_session(filter_mute):
                logging.debug("翻页会话列表获取新消息")
                return get_new_message(new_sessions[0])
            else:
                logging.debug("没有新消息")
                return []

    def get_next_new_message(self, filter_mute: bool = False):
        if filter_mute and not self.navigation_panel.has_new_message():
            return {}
        new_msgs = self._get_next_new_message(filter_mute)
        if new_msgs:
            chat_info = self.chat_pane.get_info()
            return {
                'chat_name': chat_info['chat_name'],
                'chat_type': chat_info['chat_type'],
                'msg': new_msgs
            }
        else:
            return {}


def get_all_chat_window() -> list[ChatWindow | ChatRoomWindow]:
    return [
        ChatWindow(i.Name) if i.ButtonControl(Name="视频聊天").Exists(0) else ChatRoomWindow(i.Name)
        for i in uiautomation.GetRootControl().GetChildren() if i.ClassName == "ChatWnd"
    ]


def get_chat_window(who: str) -> ChatWindow | ChatRoomWindow:
    exist = uiautomation.GetRootControl().WindowControl(ClassName="ChatWnd", Name=who).Exists(0)
    if exist:
        window = uiautomation.GetRootControl().WindowControl(ClassName="ChatWnd", Name=who)
        if window.ButtonControl(Name="视频聊天").Exists(0):
            return ChatWindow(window.Name)
        else:
            return ChatRoomWindow(window.Name)

    raise WindowNotExist(f"{who}聊天窗口不存在在！")
