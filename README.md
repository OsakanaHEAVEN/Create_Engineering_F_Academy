# Create Engineering F 技術講義

[技術概論から読む](https://create-engineering-f-academy.velvetclay32.chatgpt.site)　·　[GitHubで読む](docs/index.md)　·　[Pythonファイルの地図](docs/reference/files.md)

画像を一枚取り込むとき、画面から保存関数に渡るのは何でしょう。保存した後、画面に出る記録は誰が読み直すのでしょう。この講義では、元アプリを開いて同じ行をたどれるように、ファイル、関数、実際の引数と戻り値を結び付けて読みます。前提はPythonの関数とクラスの初歩です。第1章から読み始めるのに環境の準備は要りません。

| 章 | コードから説明できること |
|---|---|
| [1　技術概論](docs/index.md) | 通常起動の構成。どのオブジェクトが保存担当とDB接続を持つか |
| [2　起動とイベント](docs/course/operate.md) | mainからQtの通知、ファイル選択、終了処理までの呼び出し |
| [3　一枚の画像とSQLite](docs/course/remember.md) | Path、ImageRecord、SQLの行、表示文字列の間で値がどう変わるか |
| [4　データ型と契約](docs/course/meaning.md) | 二つのImageRecord、Protocol、AI応答を検査する関数の入出力 |
| [5　非同期処理と更新順序](docs/course/time.md) | 撮影要求ID、音声片の終端時刻、ジョブID、版番号の使い分け |
| [6　検索・共有と変更の影響](docs/course/share.md) | 候補検索と承認の境界、分類キーやタグ型の変更が波及する場所 |

ファイルの所在から探すなら[全Pythonファイルの地図](docs/reference/files.md)、呼び出し元と副作用を確認するなら[関数の読解索引](docs/reference/code.md)を開いてください。[調査台帳](docs/reference/audit.md)には、講義の基準コミットと、通常の起動経路、開発用の代替実装、設計段階の機能の判定根拠があります。

## サイトとして読む

GitHubと本人限定サイトの更新は独立しています。手元で最新版をサイトとして開く場合は、教材直下のPowerShellで次を実行し、表示されたURLを開きます。

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m mkdocs serve
~~~

ビルドは `python -m mkdocs build --strict`、リンク・ラボ本文の検査は `python scripts/check_docs.py` です。Actionsのビルドが成功すると、実行ページからサイト一式を **course-html** として取得できます。Pagesの設定・配布、本体の変更に追従する手順は[改訂・公開手順](docs/reference/update.md)にあります。教材サイトの構築は元アプリに依存しません。元の関数を呼ぶ実験だけは[本体を使った実験](docs/reference/setup.md)の準備が必要です。
