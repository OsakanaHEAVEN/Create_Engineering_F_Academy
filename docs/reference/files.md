# Pythonファイルの地図　コードの置き場所から読む

ソースを開くときは、まず何を実行しているかを決めると迷いません。通常起動の入口は `src/imagebox/__main__.py`、部品を一つ試す例は `examples/help/`、決められた入力で結果を照合するコードは `tests/` にあります。以下は調査したmainにあるPythonファイルの配置です。名前を選ぶと、その版のソースが開きます。

たとえば「一枚取り込むときの型」を調べるなら、下の表から `ui/main_window.py` を開き、`add_image` の中で `self.repo.import_file(Path(name))` を見つけます。同じファイルで `self.repo =` を探せば担当クラスが分かり、先頭の `from` を見れば次に開くファイルが分かります。そこにある `def import_file(self, path: Path) -> ImageRecord` が、呼び出した側からは見えなかった受け渡しの約束です。[値を一行ずつ追う](../course/remember.md)・[呼び出し元と副作用の索引](code.md)

## src/imagebox

| Pythonファイル | ここで読める処理 |
|---|---|
| [__main__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/__main__.py) | 起動｜main が QApplication と MainWindow を生成し、イベントループの終了コードを返す。 |
| [ui/main_window.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py) | 画面｜MainWindow がボタンと関数を結ぶ。Qt → add_image → 保存担当、refresh → list_images → 表示。 |
| [core/models.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/models.py) | 旧型｜ImageRecord を repository が生成し、画面と共有部品が属性を読む。固定の分類キーと表示辞書もここ。 |
| [core/repository.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py) | 旧保存層｜ImageRepository が Path を受けて画像をコピーし、記録をSQLiteへ書く。画面から呼ばれる。 |
| [core/config.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/config.py) | 設定値｜PRE_CAPTURE_SECONDS を音声バッファが既定値に使う。ライブラリ用ディレクトリ名などの定数も定義。 |
| [core/contracts.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py) | 新しい共有型・例外・Protocol｜CaptureInput や Annotation と、受け取るメソッドの型を定義。FakeとAI部品がここをimportする。 |
| [dev/fakes.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py) | 開発用実装｜FakeRepository が記録とジョブを辞書に保持。FakeSearch は注入されたrepoに検索を渡す。契約テストが主な呼び出し元。 |
| [camera/audio_ring.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py) | 音声｜AudioRingBuffer.push が数値列と終端時刻を受け、snapshot がシャッター時刻に対応する音とサンプルレートを返す。 |
| [augmentation/audio.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py) | 録音・音声認識｜record_wav が録音してWAVの場所を返す。transcribe_wav は音声ファイルから文章を返す。 |
| [augmentation/service.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py) | 画像説明｜GeminiVisionProvider.annotate がパスと文字起こしを受ける。応答を _parse_annotation に渡し、新型の Annotation を返す。 |
| [classification/service.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/classification/service.py) | 分類｜classify_by_rules が説明と文字起こしの語句を照合し、旧型の分類キーを返す。 |
| [sharing/service.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py) | ローカル共有候補｜match_candidates が旧型の記録から候補リストを作り、approved_image_path が承認済み画像のローカルパスを返す。 |

## examples/help

| Pythonファイル | ここで読める処理 |
|---|---|
| [qt_camera.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/qt_camera.py) | 撮影ボタン → shoot → 要求ID。別の通知 → saved → 要求時のパスを取り出す。 |
| [audio_ring.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/audio_ring.py) | 人工入力またはマイクの値を本体の AudioRingBuffer に渡し、時刻を指定して取り出す。 |
| [qthread.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/qthread.py) | Window.start が処理を別のスレッドへ渡し、Worker の完了通知を画面側で受ける。 |
| [gemini_image.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/gemini_image.py) | 画像の場所と説明用の文字列を本体の annotate に渡し、戻った値の各属性を表示する。 |
| [strip_exif.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/strip_exif.py) | JPEGを開いて向きを補正し、付属情報を引き継がずに別のJPEGへ書き出す独立例。 |
| [fastapi_server.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/fastapi_server.py) | HTTPリクエストが health・register・me の各関数へ届く。登録データをメモリに持つデモ。 |
| [httpx_client.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/httpx_client.py) | 上記サーバーへ登録を送り、応答からトークンを取り出して本人情報の取得に使う。 |

## tests

| Pythonファイル | ここで読める処理 |
|---|---|
| [test_repository.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_repository.py) | 一時フォルダのPNG → 旧Repository。削除後に元ファイルが残ることや不正な分類を確認。 |
| [test_contract_bootstrap.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_contract_bootstrap.py) | テストが新しい入力型、Fakeの保存・付加・分類・検索を順に呼ぶ。呼び出す側を読むのに適している。 |
| [test_gemini_provider.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_gemini_provider.py) | サンプル応答 → parser、画像 → JPEG変換。同意の確認や入力の拒否を検査。 |
| [test_whisper_cache.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_whisper_cache.py) | モデルを差し替え、繰り返し文字起こししても初期化が再使用されることを確認。 |
| [test_audio_ring.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_audio_ring.py) | 時刻と数値列を与え、重なる窓、無音の穴、期限切れ、時刻の逆行を検査。 |
| [test_classification.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_classification.py) | 短い文を旧分類関数に渡し、戻った固定キーを確認。 |
| [test_augmentation.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_augmentation.py) | 手動入力に使う旧 Annotation の値を確認。 |
| [test_sharing.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_sharing.py) | 旧型のサンプル記録から候補を検索し、承認されていないパスの取得を拒むことを確認。 |
| [test_help_examples.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_help_examples.py) | 手引きの例と実ファイルの一致、依存や担当名の取り決めを確認。 |

## パッケージの入口

次の `__init__.py` はディレクトリをパッケージとして扱うために置かれています。この版ではここで保存層やワーカーを初期化していません。アプリの起動処理は上の `__main__.py` にあります。

[examples/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/__init__.py)、[examples/help/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/__init__.py)、[src/imagebox/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/__init__.py)、[src/imagebox/augmentation/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/__init__.py)、[src/imagebox/camera/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/__init__.py)、[src/imagebox/classification/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/classification/__init__.py)、[src/imagebox/core/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/__init__.py)、[src/imagebox/dev/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/__init__.py)、[src/imagebox/sharing/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/__init__.py)、[src/imagebox/ui/__init__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/__init__.py)。

## メソッドの引数を定義から引く

本体にある関数とメソッドの見出しを、定義元ごとに開けます。`self` は呼び出し先の実体、`->` の右は戻り値の型ヒントです。矢印のない定義では、実装の `return` や呼び出し例を確認します。`contracts.py` にあるProtocolのメソッドは型の約束です。実際に値を変える場所は、通常起動なら `repository.py`、契約テストなら `fakes.py` を開いて比べてください。

<details markdown="1"><summary>__main__.py</summary>

- `main() -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/__main__.py#L9)

</details>

<details markdown="1"><summary>ui/main_window.py</summary>

- `MainWindow.__init__(self)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L23)
- `MainWindow._placeholder(self, message: str) -> QWidget`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L35)
- `MainWindow._classification_tab(self) -> QWidget`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L42)
- `MainWindow.refresh(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L64)
- `MainWindow.add_image(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L72)
- `MainWindow.delete_category(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L86)
- `MainWindow.closeEvent(self, event)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L108)

</details>

<details markdown="1"><summary>core/repository.py</summary>

- `default_data_dir() -> Path`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L18)
- `ImageRepository.__init__(self, root: Path | None=None)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L24)
- `ImageRepository.close(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L41)
- `ImageRepository.import_file(self, path: Path) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L44)
- `ImageRepository.save(self, record: ImageRecord) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L72)
- `ImageRepository.list_images(self, category: str | None=None) -> list[ImageRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L92)
- `ImageRepository.get(self, image_id: str) -> ImageRecord | None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L112)
- `ImageRepository.delete_category(self, category: str) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L118)

</details>

<details markdown="1"><summary>core/contracts.py</summary>

- `RateLimited.__init__(self, retry_after_seconds: float | None=None)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L51)
- `RepositoryPort.register_capture(self, data: CaptureInput) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L153)
- `RepositoryPort.import_image(self, source_path: str) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L154)
- `RepositoryPort.get_image(self, image_id: str, include_trash: bool=False) -> ImageRecord | None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L155)
- `RepositoryPort.get_image_path(self, image_id: str) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L156)
- `RepositoryPort.get_audio_path(self, image_id: str) -> str | None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L157)
- `RepositoryPort.list_images(self, query: SearchQuery) -> list[ImageRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L158)
- `RepositoryPort.save_annotation(self, image_id: str, annotation: Annotation, expected_revision: int, source: AnnotationSource='ai') -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L159)
- `RepositoryPort.set_category(self, image_id: str, category_id: str | None, expected_revision: int, source: CategorySource) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L163)
- `RepositoryPort.create_category(self, name: str, description: str) -> CategoryRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L167)
- `RepositoryPort.update_category(self, category_id: str, name: str, description: str) -> CategoryRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L168)
- `RepositoryPort.delete_category(self, category_id: str) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L171)
- `RepositoryPort.list_categories(self) -> list[CategoryRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L172)
- `RepositoryPort.trash_images(self, image_ids: list[str]) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L173)
- `RepositoryPort.restore_images(self, image_ids: list[str]) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L174)
- `RepositoryPort.purge_images(self, image_ids: list[str]) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L175)
- `RepositoryPort.enqueue_job(self, image_id: str, stage: str, generation: int) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L176)
- `RepositoryPort.claim_job(self, stage: str, now_utc: str) -> dict | None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L177)
- `RepositoryPort.complete_annotation_job(self, job_id: str, annotation: Annotation, expected_revision: int) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L178)
- `RepositoryPort.complete_classification_job(self, job_id: str, category_id: str, expected_revision: int) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L181)
- `RepositoryPort.finish_job(self, job_id: str, status: JobState, error_code: str | None=None, retry_at_utc: str | None=None) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L184)
- `SearchPort.search(self, query: SearchQuery) -> list[ImageRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L192)
- `SpeechProvider.transcribe(self, wav_path: str) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L196)
- `VisionProvider.annotate(self, image_path: str, transcript: str) -> Annotation`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L200)
- `ClassificationProvider.classify(self, annotation: Annotation, categories: list[CategoryRecord]) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L204)
- `AnnotationCoordinator.retry(self, image_id: str) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L210)
- `AnnotationCoordinator.start_worker(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L211)
- `AnnotationCoordinator.stop_worker(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L212)
- `ClassificationCoordinator.retry(self, image_id: str) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L216)
- `ClassificationCoordinator.start_worker(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L217)
- `ClassificationCoordinator.stop_worker(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L218)
- `SharingClientPort.create_request(self, owner_user_id: str, query: str) -> ShareRequestRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L223)
- `SharingClientPort.list_inbox(self) -> list[ShareRequestRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L224)
- `SharingClientPort.list_outbox(self) -> list[ShareRequestRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L225)
- `SharingClientPort.reject(self, request_id: str) -> ShareRequestRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L226)
- `SharingClientPort.approve(self, request_id: str, file_paths: list[str]) -> list[SharedFileRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L227)
- `SharingClientPort.list_approved_files(self, request_id: str) -> list[SharedFileRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L228)
- `SharingClientPort.download(self, request_id: str, file_id: str, destination: str) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L229)

</details>

<details markdown="1"><summary>dev/fakes.py</summary>

- `_now() -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L28)
- `_normalize(text: str) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L32)
- `FakeRepository.__init__(self)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L39)
- `FakeRepository._add(self, path: str, audio_path: str | None, source: str, shutter_at: str | None, group: str | None, index: int | None) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L48)
- `FakeRepository.register_capture(self, data: CaptureInput) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L82)
- `FakeRepository.import_image(self, source_path: str) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L96)
- `FakeRepository.get_image(self, image_id: str, include_trash: bool=False) -> ImageRecord | None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L99)
- `FakeRepository.get_image_path(self, image_id: str) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L105)
- `FakeRepository.get_audio_path(self, image_id: str) -> str | None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L110)
- `FakeRepository.list_images(self, query: SearchQuery) -> list[ImageRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L115)
- `FakeRepository._write(self, image_id: str, **changes) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L144)
- `FakeRepository.save_annotation(self, image_id: str, annotation: Annotation, expected_revision: int, source: str='ai') -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L152)
- `FakeRepository.set_category(self, image_id: str, category_id: str | None, expected_revision: int, source: str) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L169)
- `FakeRepository.create_category(self, name: str, description: str) -> CategoryRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L187)
- `FakeRepository.update_category(self, category_id: str, name: str, description: str) -> CategoryRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L194)
- `FakeRepository.delete_category(self, category_id: str) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L203)
- `FakeRepository.list_categories(self) -> list[CategoryRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L216)
- `FakeRepository.trash_images(self, image_ids: list[str]) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L219)
- `FakeRepository.restore_images(self, image_ids: list[str]) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L227)
- `FakeRepository.purge_images(self, image_ids: list[str]) -> int`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L236)
- `FakeRepository.enqueue_job(self, image_id: str, stage: str, generation: int) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L253)
- `FakeRepository.claim_job(self, stage: str, now_utc: str) -> dict | None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L265)
- `FakeRepository.complete_annotation_job(self, job_id: str, annotation: Annotation, expected_revision: int) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L272)
- `FakeRepository.complete_classification_job(self, job_id: str, category_id: str, expected_revision: int) -> ImageRecord`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L284)
- `FakeRepository.finish_job(self, job_id: str, status: str, error_code: str | None=None, retry_at_utc: str | None=None) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L295)
- `FakeSearch.__init__(self, repository: FakeRepository)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L309)
- `FakeSearch.search(self, query: SearchQuery) -> list[ImageRecord]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L312)
- `FakeSpeechProvider.transcribe(self, wav_path: str) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L317)
- `FakeVisionProvider.annotate(self, image_path: str, transcript: str) -> Annotation`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L322)
- `FakeClassificationProvider.classify(self, annotation: Annotation, categories: list[CategoryRecord]) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L330)

</details>

<details markdown="1"><summary>camera/audio_ring.py</summary>

- `AudioRingBuffer.__init__(self, sample_rate: int=16000, seconds: float=PRE_CAPTURE_SECONDS)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py#L19)
- `AudioRingBuffer.push(self, samples: Iterable[int], timestamp: float) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py#L27)
- `AudioRingBuffer.snapshot(self, shutter_time: float) -> tuple[array, int]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py#L55)
- `AudioRingBuffer.clear(self) -> None`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py#L90)

</details>

<details markdown="1"><summary>augmentation/audio.py</summary>

- `record_wav(path: Path, seconds: float=5.0, sample_rate: int=16000) -> Path`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py#L7)
- `_whisper_model(model_size: str)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py#L29)
- `transcribe_wav(path: Path, model_size: str='tiny') -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py#L38)

</details>

<details markdown="1"><summary>augmentation/service.py</summary>

- `_clean_jpeg(image_path: str) -> bytes`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L13)
- `_parse_annotation(text: str, transcript: str, model: str) -> Annotation`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L22)
- `GeminiVisionProvider.__init__(self, *, consent: bool, model: str | None=None)`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L51)
- `GeminiVisionProvider.annotate(self, image_path: str, transcript: str) -> Annotation`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py#L55)

</details>

<details markdown="1"><summary>classification/service.py</summary>

- `classify_by_rules(caption: str, transcript: str='') -> Category`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/classification/service.py#L9)

</details>

<details markdown="1"><summary>sharing/service.py</summary>

- `_bigrams(value: str) -> set[str]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L14)
- `match_candidates(query: str, records: list[ImageRecord], limit: int=5, min_score: float=0.15) -> list[Candidate]`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L23)
- `approved_image_path(image_id: str, approved_ids: set[str], records: list[ImageRecord]) -> str`　[定義行](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L42)

</details>

[技術概論へ](../index.md)・[引数の意味・利用者・副作用を読む](code.md)
