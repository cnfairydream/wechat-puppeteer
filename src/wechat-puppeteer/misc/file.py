# -*- coding: utf-8 -*-

from pathlib import Path


def get_locales_dir() -> Path:
    cur_dir = Path(__file__).parent
    return cur_dir.parent / "locales"
