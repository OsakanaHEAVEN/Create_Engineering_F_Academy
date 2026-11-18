# 11　総合演習　自分で直し、証拠を示して説明する

**到達点**　動作予測、障害診断、機能の小拡張、口頭説明を一人で完了できる。前提は[統合講義](10-trace.md)。解答を閉じたまま、まず紙に入出力と副作用を書こう。

## テストの緑色は、何の証明か

pytestは `test_` から始まる関数を収集し、`assert` の条件を検査する。`tmp_path` はpytestがテストごとに用意する一時ディレクトリ。`pytest.raises(E)` は囲んだ呼出しがEを出すことを検査する。`monkeypatch` は試験中だけ依存先などを置き換える。テストは電気回路の測定点に似ている。測定点の電圧を確認しただけでは装置全体の動作条件は決まらない。

| 観測したい境界 | 元プロジェクトの試験 | 確認できる範囲 |
|---|---|---|
| 応答文字列→Annotation | [tests/test_gemini_provider.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_gemini_provider.py) | JSON・要素の型と長さ、同意拒否、メタデータの処理。実際のAPI可用性は別試験 |
| 時刻→PCM | [tests/test_audio_ring.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_audio_ring.py) | 連写の重なり、開始直後、欠けた区間、逆順入力。実マイクは使わない |
| ファイル＋SQLite | [tests/test_repository.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_repository.py) | 一時領域に本物のDBと画像を作る結合試験。旧保存層 |
| 付加・分類・検索 | [tests/test_contract_bootstrap.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_contract_bootstrap.py) | Fake間に流れる値と競合を検証。実ジョブの耐障害性は別 |
| ドキュメントの実例 | [tests/test_help_examples.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_help_examples.py) | Markdownと例の一致、compile等。全例でデバイス・通信を動かす試験ではない |
| 製品を受け入れる | [docs/ACCEPTANCE_TESTS.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/ACCEPTANCE_TESTS.md) | C01〜C20、A01〜A15、S01〜S13は合格条件。定義だけでは合格記録にならない |

### 課題1　元実装を呼ぶ関数を追加する

教材側に `practice_count.py` を新規作成する。引数は `repo: RepositoryPort`、戻り値は `int`。activeで未分類の画像数を返す `count_unclassified(repo)` を実装する。Fakeには写真を2枚登録し、片方をotherへ移す。その後もう片方をtrash→復元する。期待件数は `2 → 1 → 0 → 1`。Repository内部の辞書を触らず、101件でも正しく数えること。空のアルバム、全行がotherの場合も予測する。

<details markdown="1">
<summary>実装例と採点の観点</summary>

`SearchQuery(unclassified_only=True)` でフィルタし、既定limit=100を考慮してoffsetを進める。空ページまたは短い最終ページで終える。件数を数える間にデータが変わるとページ間の重複・欠落がありうるため、下の例は静止した一覧に限る。本番で厳密な件数が必要なら同じ条件のCOUNTや一貫した読取トランザクションを検討する。[実行できる解答と101件の検査](../labs/count_solution.py)

</details>

### 課題2　戻せる変更を設計する

新仕様「撮影前の音声窓を5秒から3秒に変える」を受けた。要件・定数・利用側・テストのどれが変わるか、変更不要の境界も含めて差分メモを書く。Gitのコミットはその時点のツリー、ブランチは先端コミットを指す名前、PRはあるブランチの変更を別ブランチへ取り込む前に検討する場所。学習用ブランチで差分を作り、根拠・実測・未検証条件をPR本文に分けよう。リファクタリング（外から見た振る舞いを保つ内部整理）と、この振る舞い変更は別コミットにすると比較しやすい。

<details markdown="1">
<summary>影響調査の解答</summary>

PROJECT_SPEC・CONTRACTS・受入A03、core/config.pyのPRE_CAPTURE_SECONDS、既定値でringを作るテスト、説明・例が対象。10秒・12秒撮影は[7,10)と[9,12)になり重複は1秒、16 kHzなら各48,000フレーム。CaptureInputのフィールド型・SQLiteの画像ID・HTTP認可規則は変わらない。record_wavの既定5秒は別の録音経路なので、同一要件が適用されるかを呼出元から判断する。別ブランチでも同じファイルを変更した場合は競合箇所の意図を照合し、解消後に改めて動作試験する。

</details>

### 課題3　障害を一つ切り分ける

「再起動後に分類されない」と報告された。旧GUI、Fake、予定の永続ワーカーの各場合について、最初に確認する1点と、見つけたい証拠を書く。

<details markdown="1">
<summary>解答例</summary>

旧GUIでは起動時のRepository型とjobs表の有無を確認する。旧層であれば再開対象を登録していない。Fakeではプロセス／インスタンスを作り直したかを確認する。辞書が失われた場合、待機では解決しない。永続版では該当画像のstage・status・generation・run_after_utcを調べ、再起動時のprocessing回収と二重登録防止を試験する。最後のケースは現在のmainの障害報告と断定できない。

</details>

### 課題4　資料を閉じて5分で教える

1分ずつ、①通常起動と表示、②取り込み時のファイルとDB、③音声と付加、④ジョブの競合と回復、⑤承認付き共有を説明する。各項目に「入口の関数か契約」「一つの具体値」「副作用」「失敗時」「実装区分」の五つを入れる。各項目5点、合計25点。自習の目安は20点以上かつ、実動作と予定を取り違えた項目がゼロ。翌日は資料を閉じ、同じ説明を逆向きに「この表示値を最後に書いたのはどこか」から行う。

<details markdown="1">
<summary>説明の一例　写真IDを起点にする</summary>

旧GUIはimport_fileが作ったUUIDをDB主キーと管理ファイル名に使う。Fakeの登録では別の実行のUUIDがメモリ内のrecordsとjobsを関連づける。共有設計ではこのローカルIDを相手のダウンロードIDに流用せず、承認済みファイルにサーバーが別のIDを発行する。IDの発行場所を特定すれば、誰に何を見せてよいかを説明できる。

</details>

解けなかった境界は[ソース読解索引](../reference/code.md)から実装に戻り、一つの値を変えて予測と観測を比較する。

---

[前へ　10　統合追跡](10-trace.md)　·　[次へ　実験環境](../reference/setup.md)
