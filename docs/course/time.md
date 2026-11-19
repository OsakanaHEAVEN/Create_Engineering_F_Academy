# 5　非同期処理と更新順序｜遅れて返った値を何と結び付けるか

普通の関数なら呼び出し元はその場で `return` を受け取れます。撮影要求、録音の切り出し、AIジョブでは、受付と完了を別のタイミングで扱います。この三つの実装を読むと、**何のIDか、どの時計の時刻か、いつ読んだ版か**を引数で区別する理由が見えてきます。

## 撮影要求に返る整数と、あとで届くファイル名

独立した例 `examples/help/qt_camera.py` の `shoot()` は、保存先の絶対パスを文字列にして `capture.captureToFile(...)` に渡します。すぐに返る整数が `request_id` です。0以上なら `pending[request_id] = target` として覚えておきます。書き込み完了時はQtが別の関数 `saved(request_id, filename)` を呼びます。そこで `pending.pop(request_id, None)` すれば、対応する要求時のパスを取り出せます。たとえば41番、42番の順に要求して42番が先に完了しても、取り出すのは42番のパスです。この例の成功時の処理は表示までです。エラー通知では理由を表示しますが、`pending` の項目を取り除くコードはありません。[shootとsavedの接続](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/qt_camera.py#L28-L44)

## 音声の切り出しはメモリの中で完結する

本体の `camera/audio_ring.py` では `push(samples, timestamp)` の時刻がその音声片の**終端**を表します。毎秒4個の値を測る設定で時刻1.0に `[1, 2, 3, 4]` を渡すと、先頭の時刻は `1.0 − 4/4 = 0.0` 秒です。`snapshot(0.75)` なら0.75秒より前の3個だけが入り、戻り値は `(array("h", [1, 2, 3]), 4)` です。後者の4は再生時に必要なサンプルレートです。元の配列を消費しないため次の写真にも重なった区間を使えます。`Lock` は読み出しと書き込みが内部のキューを同時に変えないようにします。

この関数はWAVファイルを作りません。一方、新契約の `register_capture` が受け取る `CaptureInput.audio_tmp_path` はWAVの場所または `None` です。その間には、切り出した配列をファイル化して、対応する撮影要求と一組にする処理が要ります。通常起動の画面にはこの結線がありません。[音声部品の実装](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py#L27-L88)・[契約の入力型](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py)・[PCMからWAVを作る実行例](../labs/sound.py)

## テスト自身が次の関数を呼ぶところまで読む

`tests/test_contract_bootstrap.py` の `test_example_standalone_flow_without_other_roles` を開きます。以下で `P` は同じ写真のID、`J` はその付加ジョブのIDの略記です。順番を進めているのは、このテストのPythonコードです。

| テストからの呼び出し | 渡す値 → 戻る値 | Fake内部で変わるもの |
|---|---|---|
| `register_capture` | `CaptureInput` → 写真の記録 | `records[P]` を作り、`jobs[J]` に付加待ちを登録。説明の版も行の版も0 |
| `claim_job` | `"annotation"` と時刻 → ジョブ辞書のコピー | `jobs[J]["status"]` が `processing` になる。Fakeはこの時刻で期限を判定しない |
| `FakeVisionProvider.annotate` | 画像パスと `"授業中"` → `Annotation` | 固定の説明と渡された文字起こしをまとめる。この呼び出しだけなら記録の説明はまだ空 |
| `complete_annotation_job` | `J`、`Annotation`、期待する説明の版0 → 更新後の記録 | `save_annotation` が説明を保存し、続く `_write` が進行状態を更新。説明の版は1、行の版は2。付加を完了扱いにして分類待ちを追加 |
| `complete_classification_job` | 別途引き受けた分類ジョブのID、選んだカテゴリID、期待する分類の版0 → 更新後の記録 | `set_category` が分類を書き、次の `_write` が完了状態を書く。分類の版は1、行の版は4 |

では、AIの返答前に人が説明を編集していたらどうでしょう。`save_annotation` は現在の `annotation_revision` と引数の `expected_revision` を比べます。手動保存で現在値が1になれば、古い0を渡した呼び出しでは `ConflictError` が発生します。さらに現在の編集元が `manual` のときは、AIが最新版の1を渡しても上書きを拒みます。前者は「読んだ後で変わったか」、後者は「その値を誰が決めたか」という別々の条件です。Fakeの `complete_annotation_job` 自体はこの例外時にジョブを待ち直しへ戻さないので、引き受け済みの状態が残ります。[テストの呼び出し順](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_contract_bootstrap.py#L46-L105)・[版の判定](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L144-L167)・[ジョブ完了処理](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L262-L306)

このFakeの `jobs` はPythonの辞書で、プロセスを閉じれば消えます。永続ジョブの再起動後の回復と、複数の書き込みを一つのトランザクションにする設計は、[ジョブの読解と小さなSQLite実験](../lessons/07-jobs.md)で比較できます。[連写と録音の時系列](../lessons/05-capture.md)

[前へ　4　データ型と契約](meaning.md)　·　[次へ　6　検索・共有と変更の影響](share.md)
