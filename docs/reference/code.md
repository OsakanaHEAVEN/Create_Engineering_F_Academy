# コード読解索引　呼び出した人から副作用まで

各リンクは調査したmainの定義行を指す。表の「利用者」はこの版で確認できる代表的な入口。設計上の呼び出しは本文に「予定」と記した。Pythonの先頭 `_` はモジュール内やクラス内での利用を意図する慣例で、言語が呼出しを禁止する印ではない。

## 入口と画面

| ファイル・読む記号 | 主なimport／位置の意味 | 呼出し元→入力→戻り値・副作用 |
|---|---|---|
| [main](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/__main__.py#L9-L13) | sys、Qt、MainWindow。パッケージ実行の入口 | `-m imagebox`→argvでアプリを作成→終了コードint。初期化失敗は上位へ |
| [MainWindow.__init__](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L23-L33) | Qtウィジェット・旧modelsとImageRepository。表示と操作の組立場所 | main→repoと3タブ生成→refresh。付加／共有の`_placeholder`はメッセージを含むQWidget |
| [MainWindow._classification_tab](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L42-L62) | ボタン・コンボ・リストとレイアウト | 初期化→接続と部品を持つQWidget。`currentData()` は表示ラベルとは別の内部値 |
| [MainWindow.add_image](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L72-L84) | QFileDialog、Path | クリック→各パス→import_file。ValueError/OSErrorは集約し先頭10件を警告。sqlite3.Errorはこの捕捉対象外 |
| [MainWindow.delete_category](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L86-L106) | QMessageBox | フィルタ値→件数→確認。全件選択時は中断し、Yes時だけ保存層へ。refreshとcloseEventは[Qtの起動ノート](../lessons/02-boot.md) |

## 永続化とデータ型

| ファイル・読む記号 | 主なimport／責務 | 値の変換・例外 |
|---|---|---|
| [src/imagebox/core/config.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/config.py) | 定数の置き場 | AudioRingBufferの既定5秒。library配下の定数が定義されても旧ストアが使うとは限らない |
| [src/imagebox/core/models.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/models.py) | dataclass、field、Literal。旧GUIとローカル部品の共有型 | ImageRecordは固定Categoryと絶対パス。Annotationに簡単な手動入力の既定値。ShareRequestは旧型 |
| [ImageRepository.__init__](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L24-L39) | sqlite3、Path、Pillow、shutil等。実接続をここに集約 | root任意→images/、images.sqlite3→Rowを列名で取得可能に。closeで接続を閉じる |
| [ImageRepository.import_file](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L44-L70) | Image.open、uuid4、datetime、copy2 | GUI／テストのPath→形式を読みコピー→save→旧ImageRecord。非画像はValueError |
| [ImageRepository.save](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L72-L90) | asdict、json.dumps、SQL | record→書込SQL、戻り値None。対象IDが同じなら一部の列をまとめて更新 |
| [ImageRepository.list_images](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L92-L110) | sqlite3.Rowとjson.loads | categoryまたはNone→降順list。getはそのリストからIDで1件またはNone |
| [ImageRepository.delete_category](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L118-L132) | Path.resolve、管理ルート照合 | category→所属画像行と管理コピーを削除→件数。管理外ならSQL削除前にValueError |
| [src/imagebox/core/contracts.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py) | dataclass・Literal・Protocol。各担当が参照する境界 | CaptureInput／ImageRecord／Annotation／SearchQuery、Repository・Search・Speech・Vision・Classification・Coordinator・SharingClientの各契約。契約型だけではワーカーは生まれない |

## 代替実装・付加・分類・共有

| ファイル・読む記号 | 呼出し元と主要な依存 | 値・副作用・失敗 |
|---|---|---|
| [FakeRepository._add](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L48-L80) | register_capture/import_image→Pillow・UUID・contracts | 画像寸法を読み、新IDでrecords/paths/audiosと付加ジョブを作成。重複撮影連番は呼出側でConflictError |
| [FakeRepository.save_annotation](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L152-L167) | complete_annotation_job／手動保存→_write/replace | 版と編集元を照合し部分更新。拒否時はConflictError。set_categoryは分類版を別に検査 |
| [FakeRepository.complete_classification_job](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L284-L293) | テストがclaimしたID→set_category | 分類を保存しジョブ完了。stage・statusの不整合はConflictError |
| [FakeSearch.search](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L312-L313) | SearchPortを使うテスト→注入済みrepo | queryをlist_imagesに委譲。DBなし。FakeSpeech/Vision/Classificationはそれぞれ文字列・Annotation・IDを返す |
| [AudioRingBuffer.snapshot](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py#L55-L88) | テスト・独立例→array、deque、Lock | 単調時刻から重なるチャンクを拾い(PCMコピー, rate)。push・clearは内部キューを変更。非有限時刻を拒否 |
| [record_wav](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py#L7-L25) | 単独関数→sounddevice、wave。依存を必要時にimport | path・seconds・rate→録音を待ちWAVを作りPath。既定16kHz、1〜15秒外を拒否 |
| [_whisper_model](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py#L29-L35) | transcribe_wav→遅延import・lru_cache | model_size→CPU int8モデルを最大2種類再利用。transcribe_wavがsegmentsを連結しstr |
| [_clean_jpeg](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L13-L19) | GeminiVisionProvider→ImageOps、BytesIO | 入力パス→向きを補正したJPEG形式の画像データ。元ファイルへ書き戻さない |
| [_parse_annotation](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L22-L45) | annotate／テスト→json・contracts | テキスト・transcript・model→検証済みAnnotation。不正はValidationError |
| [GeminiVisionProvider](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L48-L97) | モジュールCLIまたは明示生成→環境変数・google.genai | consentとmodelを保持。annotateは画像と文字列を送信、応答をparse。DBの保存は呼出側 |
| [classify_by_rules](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/classification/service.py#L9-L21) | 回帰テスト→旧Category | caption＋transcript→最初に一致した固定キー、それ以外other。通信・保存なし |
| [match_candidates](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L23-L39) | 単体試験→旧ImageRecord、Candidate | query＋一覧→bigramで並べた候補。空検索は空リスト。HTTP・DBなし |
| [approved_image_path](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L42-L49) | 単体試験→承認ID集合と旧records | 未承認はPermissionError、承認済みだが記録なしはLookupError。成功はパス文字列で、送信は別段階 |

## 別のエントリーポイント

`examples/help` のファイルはGUIからimportされる製品機能とは別に起動する例である。特にQt例にはトップレベルでウィンドウを開くコードがある。

| 実例 | 入力と観測 |
|---|---|
| [examples/help/qt_camera.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/qt_camera.py) / [examples/help/audio_ring.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/audio_ring.py) | デバイス→要求IDと保存完了の対応／人工PCM→スナップショット |
| [examples/help/qthread.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/qthread.py) | ボタンクリック→別スレッドの処理→doneでラベル更新 |
| [examples/help/gemini_image.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/gemini_image.py) / [examples/help/strip_exif.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/strip_exif.py) | 画像と同意→説明／入力画像→メタデータを落とした出力 |
| [examples/help/fastapi_server.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/fastapi_server.py) / [examples/help/httpx_client.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/httpx_client.py) | アプリ登録・本人照会／クライアント側からのHTTP実例 |

`__init__.py` 群はパッケージ境界と説明を置く。`README` は着手手順、`pyproject.toml` はインストールとテスト探索、CIはWindowsでpytestとruffを実行する設定である。[README.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/README.md) [pyproject.toml](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/pyproject.toml) [.github/workflows/ci.yml](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/.github/workflows/ci.yml)

---

[前へ　Pythonファイルの地図](files.md)　·　[次へ　用語集](glossary.md)　·　[概論へ](../index.md)
