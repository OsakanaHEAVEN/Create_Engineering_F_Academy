"""標準ライブラリだけで、同じインスタンスを共有する意味を確かめる。"""
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Album:
    names: list[str] = field(default_factory=list)

    def append(self, name: str) -> None:
        self.names.append(name)


class CanAppend(Protocol):
    def append(self, name: str) -> None: ...


def record(album: CanAppend, name: str) -> None:
    album.append(name)


first = Album()
alias = first
second = Album()
record(alias, "board.png")
print(first.names, second.names, alias is first)
assert first.names == ["board.png"] and second.names == []
