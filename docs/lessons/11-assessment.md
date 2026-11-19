# テストの読み方と小さな機能変更の実例

[本編に戻る　6　検索・共有と変更の影響](../course/share.md)

試験が一つ通ったとき、写真の保存、AIの応答、画面の表示のうち、どこまでを観測できたのでしょう。ここではテストで実物を使った部分と、代役を使った部分を読み分けます。

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

## 小さな変更を一つ、最後まで読む

アルバムに「未分類の写真が何枚あるか」を表示したいとします。関数の入力は保存担当、出力は件数です。最初に二枚取り込むと2件。片方の分類を「その他」に決めると1件。その残りをごみ箱に移すと0件、復元すると1件です。この順序なら、どの写真を含めた数なのかがはっきりします。

実装例は、公開されている一覧取得に `SearchQuery(unclassified_only=True)` を渡します。1ページの既定上限は100件です。最初のページで100件返ってきたら、次は100件分ずらして読み、短いページが返るまで足します。101枚を一度に数えたつもりで100と表示してしまう間違いを、付属コードは実際に101枚用意して検査します。数えている最中に一覧が変わる場合は別途、一貫した読み取りが必要です。[動く実装と出力の検査](../labs/count_solution.py)

## 仕様が変わったとき、どこまで変えるか

「撮影前の音声は5秒から3秒にしたい」という変更を受けたとします。10秒と12秒に押した場合、保存したい区間はそれぞれ7秒から10秒の直前、9秒から12秒の直前です。重複は1秒。16 kHzなら各48,000サンプルになります。こうして期待する結果を具体的にすると、保持時間の定数、時刻窓のテスト、受入条件とその説明が変更対象に入ります。一方、共有時に承認する人や写真番号の発行方法は、この変更の影響を受けません。

変更を記録するGitのコミットは、その時点のファイルの組を指します。ブランチはコミットを指す名前で、PRは変更を取り込む前に差分と試験結果を検討する場です。この例なら「窓を3秒にした」「連写で48,000サンプルずつ残った」「実マイクは未確認」を書き分けると、何を確かめた変更かが次の人にも伝わります。外から見える動作を保つ整理をリファクタリングと呼びます。録音時間の変更は外から観察できるため、整理と変更を分けて記録すると追いやすくなります。

---

[前へ　三つの経路の追跡表](10-trace.md)　·　[概論へ](../index.md)
