# 一枚を取り込み、SQLiteから読み戻す

[本編に戻る　3　一枚の画像とSQLite](../course/remember.md)

ファイル選択画面を閉じるところから始めます。選んだ場所、保存したコピー、一覧の文字列を区別すると、同じ写真がコードのどこに現れるか追いやすくなります。

## 写真と目録に異なる仕事をさせる

本棚に本を置き、目録には置き場所を書くのと同じように、画像はファイルに保存し、その場所は `images` という表に書きます。同名の `board.png` を2回受け取っても、別のUUIDを付けるので別々の管理コピーになる。目録は名前や説明を検索できる。一方、目録を巻き戻しても棚の本は自動的には元に戻らない。SQLiteのトランザクションの境界はDBの内側にある。

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

### 同じIDの古いレコードAとBを別々に読み、Aでcaptionを保存した直後にBでcategoryを保存すると？

B側にも読込時点のcaptionが入っている。更新句にcaptionもあるのでAの編集が失われうる。後述の契約は列を分け、版番号を照合する。

### コピー作成直後の電源断と、SQLiteのINSERT失敗は同じ経路を通るか。

INSERT例外ならPythonの補償削除が走りうる。電源断ではexceptを実行できず孤児ファイルが残りうる。新設計には起動時の検出・隔離がある。

---

[次へ　既存DBの移行](../reference/schema.md)　·　[概論へ](../index.md)
