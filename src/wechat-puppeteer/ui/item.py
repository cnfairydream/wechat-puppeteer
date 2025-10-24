# -*- coding: utf-8 -*-

import time

from uiautomation import FindControl

from .base import BaseComponent, BaseListItem
from ..exceptions import ListItemNotExist


class SessionItem(BaseListItem):

    def __init__(self, parent: BaseComponent, **kwargs):
        super().__init__(parent, **kwargs)

        self._init()

    def _init(self):
        self.name = FindControl(
            self.control,
            lambda child, depth: child.ControlTypeName == "ButtonControl" and depth == 2,
            foundIndex=1,
        )
        self.time = FindControl(
            self.control,
            lambda child, depth: child.ControlTypeName == "TextControl" and depth == 4,
            foundIndex=2,
        )
        self.content = FindControl(
            self.control,
            lambda child, depth: child.ControlTypeName == "TextControl" and depth == 4,
            foundIndex=3,
        )
        self.is_mute = bool(
            FindControl(
                FindControl(
                    self.control,
                    lambda child, depth: child.ControlTypeName == "PaneControl" and depth == 3,
                    foundIndex=2,
                ),
                lambda child, depth: child.ControlTypeName == "PaneControl" and depth == 1,
                foundIndex=1,
            )
        )
        self.has_msg = FindControl(
            self.control,
            lambda child, depth: child.ControlTypeName == "TextControl" and depth == 2,
            foundIndex=1,
        )
        self.msg_count = int(self.has_msg.Name) if self.has_msg else 0


def ScrollIntoView(item: BaseListItem, equal: bool = False, bias: int = 0):
    item.root.show()
    item_control = item.control
    pane_control = item_control.GetParentControl()

    while (
            item_control.BoundingRectangle.ycenter() < pane_control.BoundingRectangle.top + bias
            or
            item_control.BoundingRectangle.ycenter() >= pane_control.BoundingRectangle.bottom - bias
    ):
        if item_control.BoundingRectangle.ycenter() < pane_control.BoundingRectangle.top + bias:
            # 向上滚动
            while True:
                if not item_control.Exists(0) or not item_control.BoundingRectangle.height():
                    raise ListItemNotExist(f"{item.class_name or item.name or ''} list item not exist！")

                pane_control.WheelUp(wheelTimes=1)
                time.sleep(0.1)

                if equal:
                    if item_control.BoundingRectangle.ycenter() >= pane_control.BoundingRectangle.top + bias:
                        break
                else:
                    if item_control.BoundingRectangle.ycenter() > pane_control.BoundingRectangle.top + bias:
                        break

        elif item_control.BoundingRectangle.ycenter() >= pane_control.BoundingRectangle.bottom - bias:
            # 向下滚动
            while True:
                if not item_control.Exists(0) or not item_control.BoundingRectangle.height():
                    raise ListItemNotExist(f"{item.class_name or item.name or ''} list item not exist！")

                pane_control.WheelDown(wheelTimes=1)
                time.sleep(0.1)

                if equal:
                    if item_control.BoundingRectangle.ycenter() <= pane_control.BoundingRectangle.bottom - bias:
                        break
                else:
                    if item_control.BoundingRectangle.ycenter() < pane_control.BoundingRectangle.bottom - bias:
                        break

        time.sleep(0.3)
