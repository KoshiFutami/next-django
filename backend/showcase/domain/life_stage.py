"""犬のライフステージを表すEnum値オブジェクト。"""

from enum import Enum

class LifeStage(Enum):
    """犬のライフステージを表すEnum（表示名付き）。"""
    NOT_YET_BORN = ("not_yet_born", "未誕生")
    NEWBORN = ("newborn", "新生児")
    YOUNG = ("young", "若犬")
    ADULT = ("adult", "成犬")

    def __init__(self, code: str, display_name: str):
        self._code = code
        self._display_name = display_name

    @property
    def code(self) -> str:
        return self._code

    @property
    def display_name(self) -> str:
        return self._display_name
