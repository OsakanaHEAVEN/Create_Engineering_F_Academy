# 3　一枚の画像とSQLite｜関数を越えて値を追う

[第2章](operate.md)で画面が渡した `Path(name)` を、今度は `core/repository.py` の側から見ます。例には `board.png` を使います。パスは「ファイルの場所」を表す値です。関数にパスを渡すだけで、画像の中身までPythonの変数に読み込まれるわけではありません。

## `import_file` の入口から `return item` まで

| コードに現れる値 | この例での中身 | 次に読むコード |
|---|---|---|
| `source = Path(path)` | 選んだ `board.png` の場所 | `source.is_file()` が存在を確かめ、`Image.open(source)` が中身を開く |
| `image_format` と `ext` | Pillowが読み取った `"PNG"` と、それに対応する `".png"` | `target` のファイル名に使う。元の拡張子だけで形式を決めていない |
| `image_id` と `target` | 新しいIDと `images/<ID>.png` | `shutil.copy2(source, target)` が管理用コピーを作る。画像本体を書き込むのはここ |
| `item` | `models.ImageRecord`。`original_name="board.png"`、`stored_path` はコピーの絶対パス、`category="other"` | `self.save(item)` がこの記録をDBに書く。成功すると `import_file` が `item` を返す |

`save` と `import_file` は親子の呼び出しですが、戻り値は違います。`save` は書き込みを終えると `None` を返します。`import_file` は手元にある `item` をそのまま呼び出し元へ返せます。コピー後、記録の生成や保存中に例外が起きると `import_file` は管理用コピーを削除して例外を送り直します。コピーとSQLiteへの書き込みは別の操作なので、二つの操作の間にプロセスが突然終了すれば、コピーだけが残る可能性があります。[取込・保存処理](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L44-L90)

## オブジェクト、SQLの一行、画面の一行

一枚の記録に `tags=["回路", "板書"]` を持たせると、Pythonでは「要素が二つのリスト」です。`save` は `asdict(record)` で各項目を辞書に取り出し、`json.dumps(fields["tags"], ensure_ascii=False)` でリストを文字列に変換し、SQLiteの `tags_json` 列に渡します。DB側に入っているのは `["回路", "板書"]` という文字の並びです。角括弧も引用符もデータの一部です。

逆向きに `list_images(None)` を呼ぶと、`SELECT` が返した各行から `json.loads(row["tags_json"])` がリストを復元し、`ImageRecord(...)` が新しいオブジェクトを作ります。`None` は全分類、`"notes"` を渡せば `WHERE category=?` による絞り込みです。画面はその一覧から `original_name`、分類キーに対応する表示名、`caption` を読みます。タグ自体はここで表示しません。[型の定義](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/models.py#L16-L28)・[読み出し](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L92-L116)・[画面への反映](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L64-L70)

## 実物で観察する　代入した直後、いつ表示に反映されるか

```python
item = repo.import_file(source)
item.caption = "RC回路の板書"
before = repo.get(item.id)
repo.save(item)
after = repo.get(item.id)
```

最初の `get` は、同じIDを持つ別のPythonオブジェクトをDBから作ります。その時点ではDBの説明はまだ空文字です。`save` の後でも、すでに読み出した `before.caption` は空文字のままです。もう一度読み直した `after.caption` に初めて新しい説明が入ります。GUIが取込時の戻り値を捨てて一覧を読み直す理由も、これでコードから説明できます。画面が表示するのは、現在の絞り込みに合い、DBに保存された記録です。

[実行例　handoff.py](../labs/handoff.py) は一時フォルダに本物のPNGとDBを作り、この順序で呼び出します。出力の `same_object=False` は、同じIDであっても `before` と `item` が別の実体であることを示します。実行すると、同じIDを次の三つの表し方で比較できます。

```text
imagebox.core.models.ImageRecord
before='', same_object=False
save=None, DB=["回路", "板書"], Python=['回路', '板書']
before='', after='RC回路の板書'
```

[実行環境とコマンド](../reference/setup.md)・[トランザクションと削除を詳しく読む](../lessons/03-storage.md)・[新しいスキーマへの移行](../reference/schema.md)

[前へ　2　起動とイベント](operate.md)　·　[次へ　4　データ型と契約](meaning.md)
