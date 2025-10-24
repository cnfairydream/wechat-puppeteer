# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import win32gui
import uiautomation
from i18n_modern import I18nModern
from uiautomation import FindControl

from ..config import Settings
from ..exceptions import (
    ButtonNotExist,
    EditNotExist,
    ListNotExist,
    ListItemNotExist,
    PanelNotExist,
    ToolBarNotExist,
    WindowNotExist,
)
from ..misc.file import get_locales_dir


class BaseComponent(ABC):

    def __init__(self, parent: BaseComponent, i18n: I18nModern | None = None, **kwargs):
        self.root = getattr(parent, "root", None)
        self.parent = parent
        self.control = None

        self.class_name = kwargs.get("class_name", None)
        self.name = kwargs.get("name", None)

        self.index = kwargs.get("index", None)
        self.depth = kwargs.get("depth", None)
        if (self.index is None) == (self.depth is None):
            raise ValueError("depth and index must be specified")

        locales = get_locales_dir() / Settings.LANG
        self.i18n = i18n or I18nModern(Settings.LANG, locales=str(locales))

        self._find_component()

    @abstractmethod
    def _find_component(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.control == other.control

    def show(self):
        handle = self.control.GetTopLevelControl().NativeWindowHandle
        win32gui.ShowWindow(handle, 1)
        win32gui.SetWindowPos(handle, -1, 0, 0, 0, 0, 3)
        win32gui.SetWindowPos(handle, -2, 0, 0, 0, 0, 3)
        self.control.Show()

    @property
    def pid(self):
        return self.control.ProcessId

    def close(self):
        self.control.SendKeys('{Esc}')


class BaseWindow(BaseComponent):

    def __init__(self, parent: BaseComponent, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = self

    def _find_component(self):
        try:
            base_control = self.parent.control if self.parent.control else uiautomation.GetRootControl()

            if self.class_name or self.name:
                self.control = base_control.WindowControl(ClassName=self.class_name, Name=self.name)
            elif self.index and self.depth:
                compare = lambda child, depth: (
                        child.ControlTypeName == "WindowControl" and child.ClassName == "" and depth == self.depth
                )
                self.control = FindControl(
                    base_control,
                    compare=compare,
                    foundIndex=self.index,
                )
            else:
                raise LookupError

        except LookupError:
            raise WindowNotExist(f"{self.class_name or self.name or ''} window not exist")


class BasePane(BaseComponent):

    def _find_component(self):
        try:
            base_control = self.parent.control if self.parent.control else uiautomation.GetRootControl()

            if self.class_name or self.name:
                self.control = base_control.PaneControl(ClassName=self.class_name, Name=self.name)
            elif self.index and self.depth:
                compare = lambda child, depth: (
                        child.ControlTypeName == "PaneControl" and child.ClassName == "" and depth == self.depth
                )
                self.control = FindControl(
                    base_control,
                    compare=compare,
                    foundIndex=self.index,
                )
            else:
                raise LookupError

        except LookupError:
            raise PanelNotExist(f"{self.class_name or self.name or ''} panel not exist！")


class BaseToolBar(BaseComponent):

    def _find_component(self):
        try:
            base_control = self.parent.control if self.parent.control else uiautomation.GetRootControl()

            if self.class_name or self.name:
                self.control = base_control.ToolBarControl(ClassName=self.class_name, Name=self.name)
            elif self.index and self.depth:
                compare = lambda child, depth: (
                        child.ControlTypeName == "ToolBarControl" and child.ClassName == "" and depth == self.depth
                )
                self.control = FindControl(
                    base_control,
                    compare=compare,
                    foundIndex=self.index,
                )
            else:
                raise LookupError

        except LookupError:
            raise ToolBarNotExist(f"{self.class_name or self.name or ''} toolbar not exist！")


class BaseButton(BaseComponent):

    def _find_component(self):
        try:
            base_control = self.parent.control if self.parent.control else uiautomation.GetRootControl()

            if self.class_name or self.name:
                self.control = base_control.ButtonControl(ClassName=self.class_name, Name=self.name)
            elif self.index and self.depth:
                compare = lambda child, depth: (
                        child.ControlTypeName == "ButtonControl" and child.ClassName == "" and depth == self.depth
                )
                self.control = FindControl(
                    base_control,
                    compare=compare,
                    foundIndex=self.index,
                )
            else:
                raise LookupError

        except LookupError:
            raise ButtonNotExist(f"{self.class_name or self.name or ''} button not exist！")


class BaseEdit(BaseComponent):

    def _find_component(self):
        try:
            base_control = self.parent.control if self.parent.control else uiautomation.GetRootControl()

            if self.class_name or self.name:
                self.control = base_control.EditControl(ClassName=self.class_name, Name=self.name)
            elif self.index and self.depth:
                compare = lambda child, depth: (
                        child.ControlTypeName == "EditControl" and child.ClassName == "" and depth == self.depth
                )
                self.control = FindControl(
                    base_control,
                    compare=compare,
                    foundIndex=self.index,
                )
            else:
                raise LookupError

        except LookupError:
            raise EditNotExist(f"{self.class_name or self.name or ''} edit not exist！")


class BaseList(BaseComponent):

    def _find_component(self):
        try:
            base_control = self.parent.control if self.parent.control else uiautomation.GetRootControl()

            if self.class_name or self.name:
                self.control = base_control.ListControl(ClassName=self.class_name, Name=self.name)
            elif self.index and self.depth:
                compare = lambda child, depth: (
                        child.ControlTypeName == "ListControl" and child.ClassName == "" and depth == self.depth
                )
                self.control = FindControl(
                    base_control,
                    compare=compare,
                    foundIndex=self.index,
                )
            else:
                raise LookupError

        except LookupError:
            raise ListNotExist(f"{self.class_name or self.name or ''} list not exist！")

    def __len__(self):
        return len(self.control.GetChildren())


class BaseListItem(BaseComponent):

    def _find_component(self):
        try:
            base_control = self.parent.control if self.parent.control else uiautomation.GetRootControl()

            if self.class_name or self.name:
                self.control = base_control.ListItemControl(ClassName=self.class_name, Name=self.name)
            elif self.index and self.depth:
                compare = lambda child, depth: (
                        child.ControlTypeName == "ListItemControl" and child.ClassName == "" and depth == self.depth
                )
                self.control = FindControl(
                    base_control,
                    compare=compare,
                    foundIndex=self.index,
                )
            else:
                raise LookupError

        except LookupError:
            raise ListItemNotExist(f"{self.class_name or self.name or ''} list item not exist！")
