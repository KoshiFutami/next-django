"""犬種マスタ（Breed）。PK は code（整数）。DB でも code を主キーにできる。"""

from dataclasses import dataclass

from showcase.domain.exceptions import DomainValidationError


@dataclass(slots=True)
class Breed:
    """マスタ 1 行。識別子は code（整数）のみ。"""

    code: int
    name: str
    sort_order: int = 0

    @classmethod
    def create(cls, *, code: int, name: str, sort_order: int = 0) -> "Breed":
        if not isinstance(code, int) or code <= 0:
            raise DomainValidationError("breed_code_invalid")
        n = (name or "").strip()
        if not n:
            raise DomainValidationError("breed_name_empty")
        if sort_order < 0:
            raise DomainValidationError("breed_sort_order_negative")
        return cls(code=code, name=n, sort_order=sort_order)
