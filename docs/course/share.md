# 6　検索・共有と変更の影響｜型の利用先から設計を読む

同じ `service.py` でも、`classification/service.py` は説明文と文字起こしを受け取って分類キーを返し、`sharing/service.py` は文章と画像の記録を受け取って共有候補を返します。`augmentation/service.py` の担当は第4章で見た説明の生成です。ファイルを探すときには親フォルダまで読むと、同名のファイルを区別できます。[分類関数](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/classification/service.py)・[共有の関数](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py)

## 共有候補が一件返るまで

ここでは `models.ImageRecord` の例として、IDが `"P"`、`caption="RC回路"`、`tags=["板書"]`、`transcript=""` の一枚を使います。呼び出し元はローカルのテストに相当し、各関数を順に呼びます。

```python
candidates = match_candidates("板書", [record])
candidate = candidates[0]
path = approved_image_path(candidate.image_id, {"P"}, [record])
```

最初の行で `match_candidates` は各記録の説明、文字起こし、タグをつないで照合用の文字列にします。`_bigrams` は隣り合う2文字を集め、検索語の集合と説明側の集合の重なりを測ります。この例では検索語「板書」が元の照合用文字列にもそのまま含まれるので、実装中の完全な部分文字列一致の分岐でスコアが1.0になります。戻るのは `[Candidate(image_id="P", score=1.0, caption="RC回路")]`。候補には画像の保存場所が含まれていません。[候補型と照合処理](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L7-L39)

最後の行の三つの引数は、**選んだID、呼び出し側が用意した承認済みIDの集合、元の記録の一覧**です。関数は集合に `"P"` があることを確かめ、対応する記録の `stored_path` を文字列で返します。集合が空なら `PermissionError`、承認済みでも一覧に該当記録がなければ `LookupError` です。ここにHTTP通信やログインした人の確認はありません。独立した[HTTPの例](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/fastapi_server.py)と、製品で予定する[複数枚の承認・転送](../lessons/09-sharing.md)には別の呼び出しが必要です。[承認関数](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L42-L49)・[呼び出して検査するテスト](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_sharing.py)

## 「分類名を変える」ならどのファイルが影響を受けるか

ここまで読むと、変更内容を具体的なファイルまで絞れます。次は同じ画面上の名前に見える二つの変更例です。

| 仮の変更 | 値が通る経路 | 変更前のデータで確かめること |
|---|---|---|
| `notes` の表示を「授業メモ」にしたい | `core/models.py` の `CATEGORY_LABELS["notes"]` → `ui/main_window.py` の選択肢と一覧表示。コンボボックスの内部値は引き続き `"notes"` | 既存行 `category="notes"` が新しい表示名で一覧に出て、同じ絞り込みで選べる |
| 保存するキー自体を `notes` から `lecture` にしたい | `Category`、`CATEGORIES`、ラベル辞書、`classification/service.py` の戻り値、`ImageRepository.save/list_images` の入力検査、既存DBのカテゴリ値に影響する | 古いDBに `"notes"` が残ったままラベル辞書からそのキーを消すと、全件表示の `CATEGORY_LABELS[record.category]` で `KeyError`。旧キーをどう変換するか決めて読み書きの両方を確認する |

新契約の `category_id` と旧GUIの `category` は定義元も利用者も違います。片方の名前を変更する前に、`from imagebox.core.models import ...` と `from imagebox.core.contracts import ...` のどちらを読むコードなのかを調べます。旧DBの変更が、そのままFakeの辞書に適用されることはありません。[旧モデル](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/models.py)・[GUIでキーと表示名を結ぶ箇所](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L47-L70)・[旧DBの入力検査](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L72-L110)

## 型を変えた直後に例外が出るとは限らない

`tags` を一個の文字列にして `"回路"` を渡したとします。旧版の `save` はタグの各要素を検査しないため、`json.dumps` は文字列を正当なJSONとして保存できます。読み出し側の `json.loads` も成功します。ところが共有側の `*rec.tags` はリストなら `"回路"` 一個、文字列なら `"回"` と `"路"` の二個に展開します。`" ".join(...)` した直後の照合用テキストには `"回 路"` が入り、検索語 `"回路"` の連続一致が外れます。2文字組を作る側は空白を消すので、候補が必ず消えるわけではありません。壊れたのは型とスコア計算の条件です。新しいAI応答の検査では、同じ文字列が `tags` に届くとリスト型の検査で直ちに `ValidationError` になります。[旧共有の展開処理](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L14-L39)・[新しい応答の検査](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L22-L45)

初めて見る関数の場合も、定義の `def` に加えて、呼び出し側の一行、その戻り値の次の利用箇所まで開いてみてください。`approved_image_path` を例にすると「共有する関数」よりも、「承認済みIDと記録の一覧から、指定画像のローカルパスを返す関数」と説明できるようになります。[全Pythonファイルの地図](../reference/files.md)・[関数の読解索引](../reference/code.md)・[小さな変更を実装する例](../lessons/11-assessment.md)

[前へ　5　非同期処理と更新順序](time.md)　·　[概論へ](../index.md)
