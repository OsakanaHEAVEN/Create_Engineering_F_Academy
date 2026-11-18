# 3　板書のPNGが、ファイルとDBの一行になるまで

**到達点**　通常GUIで取り込んだ写真について、元のファイル、管理コピー、メモリ上の値、DB行を区別し、どの障害でどれが残るかを説明する。前提は第2講の `self.repo`。

## 写真と目録に異なる仕事をさせる

本棚の本に相当するのが画像バイト、目録に相当するのが `images` 表である。同名の `board.png` を2回受け取っても、別のUUIDを付けるので別々の管理コピーになる。目録は名前や説明を検索できる。一方、目録を巻き戻しても棚の本は自動的には元に戻らない。SQLiteのトランザクションの境界はDBの内側にある。

### ダイアログの文字列からImageRecordへ

`getOpenFileNames` が返すパス一覧の各要素は文字列。`add_image` は各名前を `Path` に変換し、`import_file` に渡す。Pillowでファイルを開き `verify()`、形式がJPEG・PNG・WebPのいずれかかを確かめ、検出形式から拡張子を決める。以下の `P` は実行時に `uuid4().hex` が返す32桁の略記である。[MainWindow.add_image](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L72-L84) [ImageRepository.import_file](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L44-L70)

| 境界 | 入力 | 次に渡す値・書込み |
|---|---|---|
| 形式検査 | `D:/class/board.png` | `PNG` → `.png` |
| ファイル | UUID `P` と管理ルート | `copy2` が `images/P.png` を作成 |
| Python | ファイルと時刻 | `ImageRecord(id=P, stored_path=絶対パス, original_name="board.png", created_at=UTC文字列)`。category初期値 `other` |
| SQL | `asdict(record)` | プレースホルダー `?` に値を束縛。`tags` のリストは `json.dumps` でTEXTに変換 |
| 一覧 | `WHERE category=?` または条件なし | `sqlite3.Row` を列名で読み、`json.loads` でリストに戻して新しいレコードを生成 |
| 画面 | `refresh()` | `board.png  /  その他  /  `。表示の変更は自動保存されない |

SQLの `INSERT ... ON CONFLICT(id) DO UPDATE` は新IDなら追加し、既存IDなら指定した列を更新する。元名・保存パス・作成日時は更新句にない。一方category・caption等をまとめて上書きするので、古いレコードを二人が編集すると相手の値が消えうる。`get(id)` は現実装では `list_images()` の全行を順に比較する。主キーがあってもこの呼び方だけでは直接検索にならない。[ImageRepository.save](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L72-L90) [ImageRepository.get](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L112-L116)

## 小実験　閉じて開き直す

[実験ファイル　import_trace.py](../labs/import_trace.py)

```python
"""元アプリの旧Repositoryを一時ディレクトリで呼ぶ。"""
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from imagebox.core.repository import ImageRepository

with TemporaryDirectory() as tmp:
    root = Path(tmp)
    source = root / "board.png"
    Image.new("RGB", (32, 24), "white").save(source)
    repo = ImageRepository(root / "managed")
    try:
        row = repo.import_file(source)
        row.tags.append("回路")
        repo.save(row)
        raw = repo.conn.execute(
            "SELECT category,tags_json FROM images WHERE id=?", (row.id,)
        ).fetchone()
        print(raw["category"], raw["tags_json"], repo.get(row.id).tags)
        copy = Path(row.stored_path)
        assert source.exists() and copy.exists() and copy != source
    finally:
        repo.close()
    reopened = ImageRepository(root / "managed")
    try:
        assert reopened.get(row.id).tags == ["回路"]
        assert reopened.delete_category("other") == 1
        print(source.exists(), copy.exists(), reopened.get(row.id))
    finally:
        reopened.close()
```

`repo.save(row)` 前の `row.tags.append` はメモリだけを変える。保存後の1行目は `other ["回路"] ['回路']`。二つの括弧の中身は似ていても、中央はSQLの文字列、右はPythonのリストだ。接続を閉じ、新しいRepositoryで取得できたことで、元のインスタンスに依存しない保存を確かめられる。最後は `True False None`。

### 例外とディスクの境界

`with self.conn` は、この接続で開始したトランザクションを正常終了時にコミットし、例外時にロールバックする。接続自体は別途閉じる。コピー後の `save` が例外を出すと `except` が管理コピーを消して再送出する。一方、`copy2` はこのtryの外側であり、プロセス停止にも後始末の機会は保証されない。一括削除は全パスを検査し、DB行を削除・コミットしてから `unlink` する。ここで失敗すれば「一覧にないコピー」が残りうる。[ImageRepository.delete_category](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L118-L132) [Pythonの接続コンテキスト](https://docs.python.org/3.12/library/sqlite3.html#how-to-use-the-connection-context-manager)

<details markdown="1">
<summary>同じIDの古いレコードAとBを別々に読み、Aでcaptionを保存した直後にBでcategoryを保存すると？</summary>

B側にも読込時点のcaptionが入っている。更新句にcaptionもあるのでAの編集が失われうる。後述の契約は列を分け、版番号を照合する。

</details>

<details markdown="1">
<summary>コピー作成直後の電源断と、SQLiteのINSERT失敗は同じ経路を通るか。</summary>

INSERT例外ならPythonの補償削除が走りうる。電源断ではexceptを実行できず孤児ファイルが残りうる。新設計には起動時の検出・隔離がある。

</details>

次の章では、この実装が新しい `RepositoryPort` の代わりになる条件を調べる。

---

[前へ　2　起動とイベント](02-boot.md)　·　[次へ　保存設計演習　DB移行](../reference/schema.md)
