# 4　データ型と契約｜同じ名前の記録を見分ける

ここからは `core/contracts.py` を開きます。第3章に登場した `ImageRecord` と同じ名前のクラスがありますが、こちらは写真の処理がどこまで進んだかも表します。二つを区別する一番短い書き方は `models.ImageRecord` と `contracts.ImageRecord` です。ドットの左側が定義元です。

| 一枚取り込んだ直後 | `models.ImageRecord`（通常のGUI） | `contracts.ImageRecord`（新しい契約。ここではFakeで観測） |
|---|---|---|
| どの関数が作るか | `ImageRepository.import_file(Path)` | `FakeRepository.import_image(str) → _add` |
| 画像の場所 | `stored_path` に管理コピーの絶対パス | `stored_relpath` に管理用の相対パスを組み立てる。Fakeの `get_image_path(id)` が返すのは入力ファイルの場所 |
| 分類の初期値 | `category="other"`。画面表示は「その他」 | `category_id=None`。まだ分類していないことを表す。「その他」に確定すると `"other"` |
| 更新の仕方 | 属性へ代入して `save(record)` でDBに保存 | `save_annotation` などが版を確認し、`replace` で新しい記録を作って辞書へ入れ直す |

新型の `@dataclass(frozen=True)` は、既存の実体で `record.caption = ...` のように属性を付け替える操作を防ぎます。ただし `tags` が持つリストの中身までは固定しません。リストを直接変更すると更新メソッドの版チェックを通らないため、編集経路の設計ではこの違いも効いてきます。[旧型](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/models.py)・[新型](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py)・[Fakeの登録と書き換え](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L48-L167)

## `RepositoryPort` は何を渡せると約束するか

`repo: RepositoryPort = FakeRepository()` の `: RepositoryPort` は、この変数を通じて使うメソッドの形を表す型ヒントです。実際に動くオブジェクトを作るのは右辺です。`Protocol` を使うと、利用側は「`register_capture(data)` を呼べば所定の `ImageRecord` が返る」と書けます。契約を定義しただけで保存先が作られたり、起動時の `MainWindow.repo` がこの実体に切り替わったりはしません。[契約を使う実際のテスト](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_contract_bootstrap.py#L46-L64)

例えば旧GUIは `list_images(None)` を呼べます。Fakeの同名メソッドは `SearchQuery` を受け取り、まず `query.limit` を読みます。GUIの `ImageRepository()` を単純に `FakeRepository()` へ書き換えると、起動時の一覧更新で `None.limit` を読もうとして止まります。メソッド名に加え、**呼び出し側の引数と、結果から読む属性**がそろって初めて置き換えられます。[旧版の一覧](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L92-L110)・[Fakeの一覧](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L113-L142)

## AIへの依頼、応答の検査、保存は別々の呼び出し

`GeminiVisionProvider.annotate(image_path, transcript)` が受け取るのは「画像のある場所」と「文字起こし済みの文章」です。`_clean_jpeg` は画像を開いて向きを補正し、RGBに変換してメモリ上にJPEGとして書き出します。ここで初めて戻り値の型が `bytes`、つまり**JPEGファイルの中身を表すデータ**になります。`annotate` はその値と文字起こしを含む指示文をSDKに渡し、応答本文を次の関数へ渡します。[外部サービスを呼ぶ箇所](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L48-L97)

次は同じ実装の `_parse_annotation(text, transcript, model)` だけを呼んだ例です。通信せずに確認できます。

```python
a = _parse_annotation('{"caption":"  RC板書 ","tags":[" 回路 "]}', "復習用", "教材モデル")
```

`json.loads` で辞書になり、`caption` と `tags` の型・長さを確認してから空白を取り除きます。戻る `a.caption` は `"RC板書"`、`a.tags` は `["回路"]`、`a.transcript` は呼び出し側が渡した `"復習用"` です。`tags` が数値のリストなら `ValidationError` が出て、`a` への代入まで届きません。正常時もこの関数ではDBに一行も書きません。結果をどの写真に付けるかは、写真IDを持つ呼び出し側が決めます。[検査と値の生成](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L22-L45)・[正常・異常応答の実行例](../labs/response.py)

[契約とFakeを詳しく読む](../lessons/04-contract.md)・[音声認識とAI部品](../lessons/06-ai.md)

[前へ　3　一枚の画像とSQLite](remember.md)　·　[次へ　5　非同期処理と更新順序](time.md)
