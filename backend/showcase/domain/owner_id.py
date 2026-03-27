"""飼い主（Owner）を他集約から参照するときの識別子（値オブジェクト）。"""

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class OwnerId:
    """Owner 集約の外部参照用 ID。UUID をラップして取り違えを防ぐ。"""

    value: UUID

    @classmethod
    def generate(cls) -> "OwnerId":
        return cls(value=uuid4())
