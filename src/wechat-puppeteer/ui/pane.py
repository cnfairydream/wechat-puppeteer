# -*- coding: utf-8 -*-

import re
import logging
import time

from .base import BaseComponent, BasePane, BaseButton, BaseEdit, BaseList, BaseToolBar, BaseListItem
from .item import SessionItem, ScrollIntoView

from ..exceptions import SessionNotExist, FriendNotExist


class UpgradePane(BasePane):

    def __init__(self, parent: BaseComponent, **kwargs):
        super().__init__(parent, class_name="UpdateWnd", name=self.i18n.get("升级"), **kwargs)

        self._init()

    def _init(self):
        self.yes_icon = BaseButton(self, name=self.i18n.get("更新"))
        self.no_icon = BaseButton(self, name=self.i18n.get("暂不更新"))
        self.ignore_icon = BaseButton(self, name=self.i18n.get("该版本不再提醒"))

    def start(self):
        self.yes_icon.control.Click()

    def stop(self):
        self.no_icon.control.Click()

    def ignore(self):
        self.ignore_icon.control.Click()


class SessionPane(BasePane):

    def __init__(self, parent: BaseComponent, **kwargs):
        super().__init__(parent, **kwargs)

        self._init()

    def _init(self):
        self.search_box = BaseEdit(self, name=self.i18n.get("搜索"))
        self.session_list = BaseList(self, name=self.i18n.get("会话"))

    def get_session(self) -> list[SessionItem]:
        if self.session_list.control.Exists(0):
            return [
                SessionItem(self, depth=1, index=i)
                for i, child in enumerate(self.session_list.control.GetChildren())
                if
                child.Name != self.i18n.get("折叠置顶聊天") and not re.match(self.i18n.get("re_置顶聊天"), child.Name)
            ]

        return []

    def roll_up(self, n: int = 5):
        self.control.MiddleClick()
        self.control.WheelUp(wheelTimes=n)

    def roll_down(self, n: int = 5):
        self.control.MiddleClick()
        self.control.WheelDown(wheelTimes=n)

    def switch_chat(
            self,
            keywords: str,
            exact: bool = False,
            force: bool = False,
            force_wait: float | int = 0.5
    ):
        logging.debug(f"切换聊天窗口: {keywords}, {exact}, {force}, {force_wait}")

        self.root.show()
        sessions = self.get_session()
        for session in sessions:
            if (
                    keywords == session.name
                    and session.control.BoundingRectangle.height()
            ):
                session.control.Click()
                return keywords

        self.search_box.control.RightClick()
        SetClipboardText(keywords)
        menu = CMenuWnd(self)
        menu.select('粘贴')

        search_result = self.control.ListControl(RegexName='.*?IDS_FAV_SEARCH_RESULT.*?')

        if force:
            time.sleep(force_wait)
            self.searchbox.SendKeys('{ENTER}')
            return ''

        t0 = time.time()
        while time.time() - t0 < WxParam.SEARCH_CHAT_TIMEOUT:
            results = []
            search_result_items = search_result.GetChildren()
            highlight_who = re.sub(r'(\s+)', r'</em>\1<em>', keywords)
            for search_result_item in search_result_items:
                item_name = search_result_item.Name
                if (
                        search_result_item.ControlTypeName == 'PaneControl'
                        and search_result_item.TextControl(Name='聊天记录').Exists(0)
                ) or item_name == f'搜索 {keywords}':
                    break
                elif (
                        search_result_item.ControlTypeName == 'ListItemControl'
                        and search_result_item.TextControl(Name=f"微信号: <em>{keywords}</em>").Exists(0)
                ):
                    logging.debug(f"{keywords} 匹配到微信号：{item_name}")
                    search_result_item.Click()
                    return item_name
                elif (
                        search_result_item.ControlTypeName == 'ListItemControl'
                        and search_result_item.TextControl(Name=f"昵称: <em>{highlight_who}</em>").Exists(0)
                ):
                    logging.debug(f"{keywords} 匹配到昵称：{item_name}")
                    search_result_item.Click()
                    return item_name
                elif (
                        search_result_item.ControlTypeName == 'ListItemControl'
                        and search_result_item.TextControl(Name=f"群聊名称: <em>{highlight_who}</em>").Exists(0)
                ):
                    logging.debug(f"{keywords} 匹配到群聊名称：{item_name}")
                    search_result_item.Click()
                    return item_name
                elif (
                        search_result_item.ControlTypeName == 'ListItemControl'
                        and keywords == item_name
                ):
                    logging.debug(f"{keywords} 完整匹配")
                    search_result_item.Click()
                    return keywords
                elif (
                        search_result_item.ControlTypeName == 'ListItemControl'
                        and keywords in item_name
                ):
                    results.append(search_result_item)

        if exact:
            logging.debug(f"{keywords} 未精准匹配，返回None")
            if search_result.Exists(0):
                search_result.SendKeys('{Esc}')
            return None
        if results:
            logging.debug(f"{keywords} 匹配到多个结果，返回第一个")
            results[0].Click()
            return results[0].Name

        if search_result.Exists(0):
            search_result.SendKeys('{Esc}')

    def open_separate_window(self, name: str):
        logging.debug(f"打开独立窗口: {name}")

        sessions = self.get_session()
        for session in sessions:
            if session.name == name:
                logging.debug(f"找到会话: {name}")
                while session.control.BoundingRectangle.height():
                    try:
                        session.control.click()
                        session.control.double_click()
                    except Exception:
                        pass
                    time.sleep(0.1)

        raise SessionNotExist(f"未找到会话: {name}")

    def back_to_top(self):
        logging.debug("回到会话列表顶部")

        first_session_name = self.session_list.control.GetChildren()[0].Name
        while True:
            self.control.WheelUp(wheelTimes=3)
            time.sleep(0.1)

            if self.session_list.control.GetChildren()[0].Name == first_session_name:
                break

            first_session_name = self.session_list.control.GetChildren()[0].Name


class ChatPane(BasePane):

    def __init__(self, parent: BaseComponent, **kwargs):
        super().__init__(parent, **kwargs)

        self._init()

    def _init(self):
        self.message_list = BaseList(self, name=self.i18n.get("消息"))
        self.edit_box = BaseEdit(self, name=self.i18n.get("输入"))
        self.send_button = BaseButton(self, name=self.i18n.get("发送"))
        self.toolbar = BaseToolBar(self, depth=9, index=1)

        self._empty = False  # 用于记录是否为完全没有聊天记录的窗口，因为这种窗口之前有不会触发新消息判断的问题
        if (cid := self.id) and cid not in USED_MSG_IDS:
            USED_MSG_IDS[self.id] = tuple((i.runtimeid for i in self.msgbox.GetChildren()))
            if not USED_MSG_IDS[cid]:
                self._empty = True

    def _update_used_msg_ids(self):
        USED_MSG_IDS[self.id] = tuple((i.runtimeid for i in self.msgbox.GetChildren()))

    def _open_chat_more_info(self):
        for chatinfo_control, depth in uia.WalkControl(self.control):
            if chatinfo_control.Name == self._lang('聊天信息'):
                chatinfo_control.Click()
                break
        else:
            return WxResponse.failure('未找到聊天信息按钮')
        return ChatRoomDetailWnd(self)

    def _activate_editbox(self):
        if not self.edit_box.control.HasKeyboardFocus:
            self.edit_box.control.MiddleClick()

    @property
    def id(self):
        if self.msgbox.Exists(0):
            return self.msgbox.runtimeid
        return None

    @property
    def used_msg_ids(self):
        return USED_MSG_IDS[self.id]

    def get_info(self):
        chat_info = {}
        walk = uia.WalkControl(self.control)
        for chat_name_control, depth in walk:
            if isinstance(chat_name_control, uia.TextControl):
                break
        if (
                not isinstance(chat_name_control, uia.TextControl)
                or depth < 8
        ):
            return {}

        # chat_name_control = self.control.GetProgenyControl(11)
        chat_name_control_list = chat_name_control.GetParentControl().GetChildren()
        chat_name_control_count = len(chat_name_control_list)

        if chat_name_control_count == 1:
            if self.control.ButtonControl(Name='公众号主页', searchDepth=9).Exists(0):
                chat_info['chat_type'] = 'official'
            else:
                chat_info['chat_type'] = 'friend'
            chat_info['chat_name'] = chat_name_control.Name
        elif chat_name_control_count >= 2:
            try:
                second_text = chat_name_control_list[1].Name
                if second_text.startswith('@'):
                    chat_info['company'] = second_text
                    chat_info['chat_type'] = 'service'
                    chat_info['chat_name'] = chat_name_control.Name
                else:
                    chat_info['group_member_count'] = \
                        int(second_text.replace('(', '').replace(')', ''))
                    chat_info['chat_type'] = 'group'
                    chat_info['chat_name'] = \
                        chat_name_control.Name.replace(second_text, '')
            except:
                chat_info['chat_type'] = 'friend'
                chat_info['chat_name'] = chat_name_control.Name

            ori_chat_name_control = \
                chat_name_control.GetParentControl(). \
                    GetParentControl().TextControl(searchDepth=1)
            if ori_chat_name_control.Exists(0):
                chat_info['chat_remark'] = chat_info['chat_name']
                chat_info['chat_name'] = ori_chat_name_control.Name
        self._info = chat_info
        return chat_info

    def input_at(self, at_list: str | list[str]):
        if isinstance(at_list, str):
            at_list = [at_list]

        self.show()
        self._activate_editbox()
        for friend in at_list:
            self.edit_box.control.SendKeys('@' + friend.replace(' ', ''))
            at_pane = AtPane(self.root)
            at_pane.select(friend)

    def clear_edit(self):
        self.show()
        self.edit_box.control.Click()
        self.edit_box.control.SendKeys('{Ctrl}a', waitTime=0)
        self.edit_box.control.SendKeys('{DELETE}')

    def send_text(self, content: str):
        self.show()
        t0 = time.time()
        while True:
            if time.time() - t0 > 10:
                raise TimeoutError

            SetClipboardText(content)
            self._activate_editbox()
            self.edit_box.control.SendKeys('{Ctrl}v')
            if self.edit_box.control.GetValuePattern().Value.replace('￼', '').strip():
                break
            self.edit_box.control.SendKeys('{Ctrl}v')
            if self.edit_box.control.GetValuePattern().Value.replace('￼', '').strip():
                break
            self.edit_box.control.RightClick()
            menu = CMenuWnd(self)
            menu.select('粘贴')
            if self.edit_box.control.GetValuePattern().Value.replace('￼', '').strip():
                break

        t0 = time.time()
        while self.edit_box.control.GetValuePattern().Value:
            if time.time() - t0 > 10:
                raise TimeoutError

            self._activate_editbox()
            self.send_button.control.Click()

            if not self.edit_box.control.GetValuePattern().Value:
                return

            elif not self.edit_box.control.GetValuePattern().Value.replace('￼', '').strip():
                self.send_text(content)

    def send_message(self, content: str, at: list[str] | str | None = None):
        if not content and not at:
            raise ValueError(f"参数 `content` 和 `at` 不能同时为空")

        self.clear_edit()

        if at:
            self.input_at(at)

        return self.send_text(content)



    def get_msgs(self):
        if self.msgbox.Exists(0):
            return [
                parse_msg(msg_control, self)
                for msg_control
                in self.msgbox.GetChildren()
                if msg_control.ControlTypeName == 'ListItemControl'
            ]
        return []

    def get_new_msgs(self):
        if not self.msgbox.Exists(0):
            return []
        msg_controls = self.msgbox.GetChildren()
        now_msg_ids = tuple((i.runtimeid for i in msg_controls))
        if not now_msg_ids:  # 当前没有消息id
            return []
        if self._empty and self.used_msg_ids:
            self._empty = False
        if not self._empty and (
                (not self.used_msg_ids and now_msg_ids)  # 没有使用过的消息id，但当前有消息id
                or now_msg_ids[-1] == self.used_msg_ids[-1]  # 当前最后一条消息id和上次一样
                or not set(now_msg_ids) & set(self.used_msg_ids)  # 当前消息id和上次没有交集
        ):
            # wxlog.debug('没有新消息')
            return []

        used_msg_ids_set = set(self.used_msg_ids)
        last_one_msgid = max(
            (x for x in now_msg_ids if x in used_msg_ids_set),
            key=self.used_msg_ids.index, default=None
        )
        new1 = [x for x in now_msg_ids if x not in used_msg_ids_set]
        new2 = now_msg_ids[now_msg_ids.index(last_one_msgid) + 1:] \
            if last_one_msgid is not None else []
        new = [i for i in new1 if i in new2] if new2 else new1
        USED_MSG_IDS[self.id] = tuple(self.used_msg_ids + tuple(new))[-100:]
        new_controls = [i for i in msg_controls if i.runtimeid in new]
        self.msgbox.MiddleClick()
        return [
            parse_msg(msg_control, self)
            for msg_control
            in new_controls
            if msg_control.ControlTypeName == 'ListItemControl'
        ]

    def get_msg_by_id(self, msg_id: str):
        if not self.msgbox.Exists(0):
            return []
        msg_controls = self.msgbox.GetChildren()
        if control_list := [i for i in msg_controls if i.runtimeid == msg_id]:
            return parse_msg(control_list[0], self)

    def _get_tail_after_nth_match(self, msgs, last_msg, n):
        matches = [
            i for i, msg in reversed(list(enumerate(msgs)))
            if msg.content == last_msg
        ]
        if len(matches) >= n:
            wxlog.debug(f'匹配到基准消息：{last_msg}')
        else:
            split_last_msg = last_msg.split('：')
            nickname = split_last_msg[0]
            content = ''.join(split_last_msg[1:])
            matches = [
                i for i, msg in reversed(list(enumerate(msgs)))
                if msg.content == content
                   and msg.sender_remark == nickname
            ]
            if len(matches) >= n:
                wxlog.debug(f'匹配到基准消息：<{nickname}> {content}')
            else:
                wxlog.debug(f"未匹配到基准消息，以最后一条消息为基准：{msgs[-1].content}")
                matches = [
                    i for i, msg in reversed(list(enumerate(msgs)))
                    if msg.attr in ('self', 'friend')
                ]
        try:
            index = matches[n - 1]
            return msgs[index:]
        except IndexError:
            wxlog.debug(f"未匹配到第{n}条消息，返回空列表")
            return []

    def get_next_new_msgs(self, count=None, last_msg=None):
        # 1. 消息列表不存在，则返回空列表
        if not self.msgbox.Exists(0):
            wxlog.debug('消息列表不存在，返回空列表')
            return []

        # 2. 判断是否有新消息按钮，有的话点一下
        load_new_button = self.control.ButtonControl(RegexName=self._lang('re_新消息按钮'))
        if load_new_button.Exists(0):
            self._show()
            wxlog.debug('检测到新消息按钮，点击加载新消息')
            load_new_button.Click()
            time.sleep(0.5)
        msg_controls = self.msgbox.GetChildren()
        USED_MSG_IDS[self.id] = tuple((i.runtimeid for i in msg_controls))
        msgs = [
            parse_msg(msg_control, self)
            for msg_control
            in msg_controls
            if msg_control.ControlTypeName == 'ListItemControl'
        ]

        # 3. 如果有“以下是新消息”标志，则直接返回该标志下的所有消息即可
        index = next((
            i for i, msg in enumerate(msgs)
            if self._lang('以下为新消息') == msg.content
        ), None)
        if index is not None:
            wxlog.debug('获取以下是新消息下的所有消息')
            return msgs[index:]

        # 4. 根据会话列表传入的消息数量和最后一条新消息内容来判断新消息
        if count and last_msg:
            # index = next((
            #     i for i, msg in enumerate(msgs[::-1])
            #     if last_msg == msg.content
            # ), None)

            # if index is not None:
            wxlog.debug(f'获取{count}条新消息，基准消息内容为：{last_msg}')
            return self._get_tail_after_nth_match(msgs, last_msg, count)

    def get_group_members(self):
        self.show()
        roominfoWnd = self._open_chat_more_info()
        return roominfoWnd.get_group_members()


class AtPane(BasePane):

    def __init__(self, parent: ChatPane, **kwargs):
        super().__init__(parent, class_name="ChatContactMenu", **kwargs)

    def select(self, friend):
        at_list = BaseList(self)
        if len(at_list) == 1:
            at_list.control.GetChildren()[0].Click()
        else:
            friend_ = friend.replace(" ", "")
            at_item = BaseListItem(at_list, name=friend_)
            ScrollIntoView(at_item)
            at_item.control.Click()
