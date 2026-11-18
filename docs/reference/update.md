# 教材を新しいmainへ追従させる

## 二つのSHAを残す

元アプリと教材は別のGit履歴を持つ。教材の各版に「元アプリのどのSHAを読んだか」を残すと、コードだけ進んだ場合にも旧講義を再現できる。調査日、タイムゾーン、枝名、完全な40桁SHAを台帳へ追記する。以前の学習記録は教材コミットから再現できる。

~~~powershell
git -C ../CEF-reading fetch origin
git -C ../CEF-reading branch -r -v --no-abbrev
git -C ../CEF-reading rev-parse origin/main
git -C ../CEF-reading diff --name-status e7dbd20b3e581878729673e2cd82ea60719336e4 origin/main
git -C ../CEF-reading diff e7dbd20b3e581878729673e2cd82ea60719336e4 origin/main -- src tests examples docs
~~~

1. 本体の`__main__`から生成式と接続先をたどり直す。ファイルが追加されただけなら「部品」、実際の起動や操作から結線されていれば「GUI稼働」と区別する。
2. README・CONTRACTS・DATA_SCHEMA・ACCEPTANCE_TESTSを同じSHAで読む。差分で名称が変わったら呼出元、例、試験も探す。新規ブランチだけの実装にはそのブランチのSHAを明記する。
3. 旧・新のどちらのImageRecordをimportしているか、標本Pを使って状態表と出力を更新する。本文とラボ、図のソースとSVG、索引と用語集を一緒に変更する。
4. 本体の読解用コピーを新SHAへ切り替え、[実験環境](setup.md)で元pytestと教材ラボを実行する。固定リンクを一括置換する前に、対象定義と行番号を新コードで確認する。
5. 教材側で `python scripts/check_docs.py`、`python -m mkdocs build --strict` を実行。概論の図と画面、検索、本編6章の前後移動、狭い画面を確認してコミットする。新しい機能は、どの利用場面を変えるかを概論に反映してから、入力・結果・理由を本編の例に加える。関数別の詳しい読解は実装ノートへ置く。

## 次の改訂の入口

| 本体側で確認する条件 | 追加する読解・試験 |
|---|---|
| 新SQLite Repositoryとマイグレーションがmainに入る | 実スキーマのDDL、旧DBからの移行前後、異常終了の孤児回収を実記録で解説 |
| カメラサービスとCoordinatorが結線される | Windows実機で連写の要求ID・時刻・ファイル順を観測し、終了時の停止順を追記 |
| 本番分類Providerと永続ワーカーが実装される | 同時claim、429、再起動、手動編集との競合を実DBと試験で再評価 |
| 製品用HTTPサーバー・クライアントがmainに入る | owner・requester・第三者の独立データ領域で、承認と2枚の受信を照合 |
| 全体GUI・配布物が実装される | 再読込のシグナルと実機受入、配布版の初回起動・設定・終了を収録 |

これらの単元は本版でも契約と未接続箇所を解説している。実装が入った時点で予定の表を実測に置き換える。

## サイトの配布

GitHubのMarkdownはリポジトリの閲覧権限で読める。Actionsはpush・PRでリンク検査とstrict buildを行い、ビルド済みHTMLを成果物 `course-html` として保存する。Pagesを使う場合はリポジトリの **Settings → Pages → Source → GitHub Actions** を選び、公開対象の設定を確認してActionsの教材ワークフローを **Run workflow** から `deploy_pages=true` で実行する。以後のmainへのpushでも公開したい場合はリポジトリ変数 `PUBLISH_PAGES=true` を設定する。Pagesの利用可否と閲覧範囲はリポジトリ設定・プランに依存する。公開後のURLはdeployジョブのenvironmentに表示される。

---

[前へ　調査台帳](audit.md)　·　[概論へ](../index.md)
