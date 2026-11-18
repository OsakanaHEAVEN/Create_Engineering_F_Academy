# Create Engineering F 技術講義

**[教材サイトを開く（本人限定）](https://create-engineering-f-academy.velvetclay32.chatgpt.site)**　・　[GitHubで読む](docs/index.md)　・　[調査台帳](docs/reference/audit.md)　・　[実験環境](docs/reference/setup.md)　・　[ソース読解索引](docs/reference/code.md)

一枚の板書写真を題材に、Pythonの起動、Qt、SQLite、音声、AI、ジョブ、承認付き共有を読む日本語のオンライン教科書です。調査対象は2026年11月18日に確認した元アプリのmain（e7dbd20）。通常GUIから動く経路、独立部品、開発用Fake、将来の結合設計を、各講で根拠のコードと照合します。

## 学習方法

[第1講](docs/lessons/01-python.md)から順に、図と実行例の出力を先に予測し、実行してから折りたたみ解答と照合してください。第10講は処理全体を追う統合講義、第11講は小機能の実装と口頭試問です。図の編集元は [diagrams](diagrams)、小実験は [docs/labs](docs/labs) にあります。実験に実写真やAPIキーを使う必要はありません。

## サイトとして読む

上記の本人限定サイトは教材コミット [91d4556](https://github.com/OsakanaHEAVEN/Create_Engineering_F_Academy/commit/91d4556ffd01256842141e50c64b84d5b6f6291c) の配信版です。GitHubへのpushとこの閲覧サイトの更新は独立しています。GitHub上でも全講義を読めます。検索・階層ナビゲーション付きのサイトをWindowsで開くには、教材直下のPowerShellで次を実行し、表示されたURLを開きます。

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m mkdocs serve
~~~

ビルドは `python -m mkdocs build --strict`、リンク・ラボ本文の検査は `python scripts/check_docs.py` です。Actionsのビルドが成功すると、実行ページからサイト一式を **course-html** として取得できます。Pagesの設定・配布、本体の変更に追従する手順は[改訂・公開手順](docs/reference/update.md)にあります。教材サイトの構築は元アプリに依存しません。元の関数を呼ぶ実験だけは[本体を使った実験](docs/reference/setup.md)の準備が必要です。

## この版で確認したこと

本体の固定SHAでpytestが35件成功し、教材のPython実験11本を実行しました。教材側は18ページをstrict buildし、GitHub ActionsのChromiumで日本語検索、解答の開閉、ダークモード、図4枚、390px幅の目次操作を確認しました。実カメラ・マイク・外部AIの受入状況は[調査台帳](docs/reference/audit.md)に記録しています。[ブラウザ試験と配布用HTML](https://github.com/OsakanaHEAVEN/Create_Engineering_F_Academy/actions/runs/44223502863)
