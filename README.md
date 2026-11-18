# Create Engineering F 技術講義

**[本人限定サイトで概論を読む](https://create-engineering-f-academy.velvetclay32.chatgpt.site)**　・　[GitHubで概論を読む](docs/index.md)

板書、バスの時刻表、集合写真。同じアルバムに並ぶ三枚でも、後で何をしたいかは違います。この講義では、写真を撮る人と受け取る人の体験から出発し、そのためにアプリが何を記録し、どんな順番で処理するかを読み解きます。初めて読む方は、インストールせずに概論から進めます。

## 本編の読み順

| 章 | この章で見えること |
|---|---|
| [1　概論](docs/index.md) | なぜ写真に言葉を添えるのか。完成時の体験と、現在の画面でできること |
| [2　写真を覚える](docs/course/remember.md) | 同じ名前の写真を二枚取り込んでも、閉じて開き直せる理由 |
| [3　ボタンから処理へ](docs/course/operate.md) | ウィンドウが入力を待ち、キャンセルと取り込みを処理し分ける仕組み |
| [4　写真に意味を付ける](docs/course/meaning.md) | 同じ板書でも撮った理由が違うとき、説明・用途・検索が果たす役割 |
| [5　時間と失敗を扱う](docs/course/time.md) | 連写の完了順が逆になる、AIより先に人が説明を書く、保存途中で止まる場合 |
| [6　人と人の間で渡す](docs/course/share.md) | 欲しいと頼んだ人、持ち主、サーバーのそれぞれに、いつ何が届くか |

本編は、具体的な入力・結果・理由をその場で読める構成です。コードを一行ずつ追うときは各章の「詳しく読む」から実装ノートへ進めます。手元で再現したい場合にだけ[実行環境](docs/reference/setup.md)を使ってください。実装の所在は[ソース読解索引](docs/reference/code.md)、ブランチと実装状況は[調査台帳](docs/reference/audit.md)にあります。

## サイトとして読む

GitHubと本人限定サイトの更新は独立しています。手元で最新版をサイトとして開く場合は、教材直下のPowerShellで次を実行し、表示されたURLを開きます。

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m mkdocs serve
~~~

ビルドは `python -m mkdocs build --strict`、リンク・ラボ本文の検査は `python scripts/check_docs.py` です。Actionsのビルドが成功すると、実行ページからサイト一式を **course-html** として取得できます。Pagesの設定・配布、本体の変更に追従する手順は[改訂・公開手順](docs/reference/update.md)にあります。教材サイトの構築は元アプリに依存しません。元の関数を呼ぶ実験だけは[本体を使った実験](docs/reference/setup.md)の準備が必要です。
