# Pythonが入口を見つけるまで

[本編に戻る　3　ボタンから処理へ](../course/operate.md)

画面の起動を追っていて、なぜこのファイルが最初に動くのか気になったら、コマンドの最後の一語に注目してみましょう。

## コマンドからモジュールへ

本体は `src/imagebox` の下にある。`src` はパッケージを置く棚、`imagebox` は棚に置かれた一冊、`core/repository.py` はその中の一章、と考えよう。Pythonの特徴は、章を開くとトップレベルの文が実行されることだ。本のページと違い、読む順序がプログラムの状態を変える。

本体の `pyproject.toml` は配布名を `create-engineering-f`、探索位置を `src`、Pythonを3.12系に指定する。`pip install -e .` は、作業中のソースをその環境からimportできるようにする。配布名とimport名は異なる。教材だけを読む場合は[閲覧方法](../index.md)、実コードを動かす場合は[実験準備](../reference/setup.md)に従う。[pyproject.toml](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/pyproject.toml)

| Windowsで打つもの | 実行されるもの | 残るもの |
|---|---|---|
| `py -3.12 -m venv .venv` | 指定したPythonの標準モジュールvenv | 専用のPythonとパッケージ置き場 |
| `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"` | その環境のpip | PySide6・Pillowと開発用依存等 |
| `.\.venv\Scripts\python.exe -m imagebox` | パッケージの `__main__.py` | 起動したウィンドウ、初期化された保存領域 |

`import imagebox` は最初に `__init__.py` を評価する。このファイルには説明文字列しかない。`-m imagebox` では続いて `__main__.py` のトップレベルで `sys`、`QApplication`、`MainWindow` を読み、`def main` で関数オブジェクトを作り、末尾の条件が成立して初めて `main()` を呼ぶ。`from imagebox.__main__ import main` ではそのモジュール名は `imagebox.__main__` となるため条件が偽になる。通常、同じインタープリターで二度importしても既に読み込んだモジュールを再利用する。[src/imagebox/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/__init__.py) [main](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/__main__.py#L9-L13)

## 値が「どこにあるか」を読む

`class` は型の定義、`Album()` は一つの実体の生成。`first` が指す実体と `alias` が指す実体は同じである。`album.append(name)` と呼ぶと、メソッドにはその実体が第1引数 `self` として渡る。`first.names` を変えれば、同じ実体を参照する側にも見える。この関係が、後の `MainWindow.repo` と `FakeSearch.repository` を読む基礎になる。

[実験ファイル　objects.py](../labs/objects.py)

```python
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
```

| 実行直後 | first.names | alias.names | second.names |
|---|---|---|---|
| `second = Album()` | `[]` | `[]` | `[]` |
| `record(alias, "board.png")` | `["board.png"]` | `["board.png"]` | `[]` |

`@dataclass` はフィールドから初期化メソッドなどを作る。`default_factory=list` は実体を新しく作るたびに空リストを用意する。`CanAppend` は引数に要求する操作を記述した型。型注釈を書いても、自動変換もメソッドの追加も起きない。[契約の章](04-contract.md)で本体の例へ戻る。

## 二つの呼び方を比べる

### alias = Album() に変えると何が変わるか。どの行が失敗するか。

三つの名前が別々の実体を指す。record は alias のリストだけを変え、print は `[] [] False` を出す。first.names の検査で AssertionError になる。関数の引数は共有した実体への参照を受け取っていた。

### import には成功するのにウィンドウが出ない。故障だろうか。

`import imagebox` だけなら正常。入口を実行したか、main を単に読み込んだかを先に確かめる。ModuleNotFoundError の場合は使用中の Python と editable install の対象を確認する。

---

[前へ　既存DBの移行](../reference/schema.md)　·　[次へ　Qtの起動と終了](02-boot.md)　·　[概論へ](../index.md)
