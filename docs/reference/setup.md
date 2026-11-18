# 実験環境と実行コマンド

## まず教材を開く

GitHubでは[講義の入口](../index.md)からMarkdownを読める。サイト版を起動するには教材リポジトリ直下で次を実行する。`.venv` は教材用で、以下の `.labenv` はアプリ用である。

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m mkdocs serve
~~~

コマンドが表示するローカルURLを開く。終了はCtrl+C。ビルド検査は `.\.venv\Scripts\python.exe -m mkdocs build --strict`。ビルド済みフォルダを配布した場合はそのフォルダで `py -m http.server 8000 --bind 127.0.0.1` を実行し、ブラウザで `http://127.0.0.1:8000/` を開くと検索も利用できる。

## 本体を使った実験

教材を `Create_Engineering_F_Academy` にcloneした状態で、兄弟フォルダに元コードの**読解用コピー**を用意する。どちらの非公開リポジトリにも読み取り権限が必要。既存の開発ブランチでcheckoutする必要はない。

~~~powershell
git clone https://github.com/OsakanaHEAVEN/Create_Engineering_F.git ../CEF-reading
git -C ../CEF-reading switch --detach e7dbd20b3e581878729673e2cd82ea60719336e4
py -3.12 -m venv .labenv
.\.labenv\Scripts\python.exe -m pip install -e "../CEF-reading[dev,server]"
$env:PYTHONPATH = (Resolve-Path ../CEF-reading).Path
.\.labenv\Scripts\python.exe docs/labs/import_trace.py
.\.labenv\Scripts\python.exe docs/labs/fake_trace.py
~~~

editable installで `src/imagebox` を解決できる。`PYTHONPATH` に本体ルートも加える理由は、HTTP実験がパッケージ外の `examples/help` を読むためである。どの実験も生成したダミー画像を使い、キー・カメラ・マイクを要求しない。`http_demo.py` はプロセス内で通信を模擬する。`boot.py` はそのプロセスだけQtのoffscreenモードにする。

| ファイル | 経路 | 観測する出力 |
|---|---|---|
| [objects.py](../labs/objects.py) | 標準Python | 共有された実体と別々のリスト |
| [boot.py](../labs/boot.py) | Qtと本体 | 3タブの名前、0件 |
| [import_trace.py](../labs/import_trace.py) | 本体と実SQLite | `other`、JSONとリスト、`True False None` |
| [migration.py](../labs/migration.py) | 縮小DB | 版1、IDと説明が残る |
| [sound.py](../labs/sound.py) | リング実装とwave | 6個と8個の配列、4 Hz・6フレーム |
| [response.py](../labs/response.py) | 実parserのみ | 正常1件とValidationErrorが2件 |
| [fake_trace.py](../labs/fake_trace.py) | 実際の開発用Fake | `None 1 True`、手動値保持 |
| [atomic.py](../labs/atomic.py) | 縮小DB | 失敗直後はprocessing、成功後は2行 |
| [search.py](../labs/search.py) | 旧ローカル部品 | notes、正規化 `rc 板書`、0.25、未承認 |
| [http_demo.py](../labs/http_demo.py) | 独立FastAPI例 | `200 reader` と `409` |
| [count_solution.py](../labs/count_solution.py) | 小拡張の解答 | `[2, 1, 0, 1] 101` |

すべての実験を個別プロセスで実行するには `.\.labenv\Scripts\python.exe scripts/run_labs.py`。本体のテストは `Push-Location ../CEF-reading` して、教材側の `.labenv\Scripts\python.exe` をフルパスで指定して `-m pytest -q`、終わったら `Pop-Location`。GUIを自分で操作する場合は次の専用フォルダで起動する。

~~~powershell
$env:IMAGEBOX_DATA_DIR = Join-Path $PWD "study-data"
.\.labenv\Scripts\python.exe -m imagebox
~~~

「画像を取り込む」から自作PNGを選び、一覧を閉じて再起動する。次にフィルタで「その他」を選ぶ。ここから一括削除する操作は旧GUIでは管理コピーを即時削除する。使い捨ての画像と上記の専用フォルダで観測する。

---

[前へ　11　総合演習](../lessons/11-assessment.md)　·　[次へ　ソース読解索引](code.md)
