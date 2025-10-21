# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LANG: str = "zh_CN"
