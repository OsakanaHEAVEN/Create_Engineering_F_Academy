# 旧・新の写真データと保存担当の代役

[本編に戻る　3　ボタンから処理へ](../course/operate.md)

二つのファイルに同じ名前のImageRecordが登場します。どちらの型かで「その他」の意味まで変わるので、呼び出す側が相手に何を頼んでいるかを見てみましょう。

## 呼び出す側が必要とする形を決める

受付票に「写真を預けるとIDの載った控えを返す」と記されていれば、呼ぶ側は保管棚の構造を知る必要がない。Repositoryはデータ操作の窓口、Portは呼出側から見たメソッドと引数・戻り値の約束、Providerは文字起こし等の能力を提供する側である。受付票だけを用意しても、ファイルを運ぶ担当者までは生まれない。

`repo: RepositoryPort = FakeRepository()` の右辺が実体を作る。左辺は型検査に使う注釈で、Pythonが本物のDBへ自動接続する命令ではない。`Protocol` は必要な属性やメソッドが構造的に合うことを表現でき、明示的な継承を要求しない。注釈の整合、実行できること、意味上の契約を守ることはそれぞれ別に確認する。[RepositoryPort](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L150-L187) [test_public_imports_and_fake_substitutability](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_contract_bootstrap.py#L36-L46)

| 問うこと | 通常GUIの `core.models` | v2契約の `core.contracts` |
|---|---|---|
| 画像の場所 | `stored_path` が絶対パス | `stored_relpath`。管理ルートから解決する設計 |
| 初期分類 | `category="other"` | 未判定は `category_id=None`、決定後の `"other"` と区別 |
| 編集 | 可変。フィールドを変えて `save` | `frozen=True` のレコード。更新要求が新しいレコードを返す |
| 説明の型 | `Annotation` はcaption以外に既定値あり | 同名型はprovider・model・prompt_version等を要求 |
| 取り込み口 | `import_file(Path)` | `import_image(str)` または `register_capture(CaptureInput)` |

同名のクラスでも定義したモジュールが違えば別の型。`frozen=True` は属性への再代入を制限するが、中にある `list` の要素まで不変にはしない。Fakeの `_write` は `dataclasses.replace` で変更した実体を辞書に置くため、以前受け取ったレコード変数には古い値が残る。[ImageRecord](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/models.py#L17-L27) [ImageRecord](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py#L88-L116) [FakeRepository._write](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L144-L150)

### どこが本当に差し替わったのか

`FakeSearch(repo)` は既存の `repo` を属性に保存し、`search(query)` で同じ実体の `list_images(query)` へ委譲する。ここで毎回新しい `FakeRepository()` を渡せば空のアルバムになる。Fakeは簡易ながら状態を持つ代替実装、Stubは決めた応答を返す代役、Mockは呼ばれ方を検査する代役として使う。名にFakeと付く `FakeSpeechProvider` はこの用途では固定文字列を返すStubとして働く。Whisperの試験では代役が初期化引数を記録し、テスト側が回数も検査する。[FakeSearch](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L308-L313) [tests/test_whisper_cache.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_whisper_cache.py)

| Fakeへ実在する32×24のPNGを渡す | 観測できること | 実物との境界 |
|---|---|---|
| `register_capture` の `_add` | Pillowが寸法と形式を読む。UUIDを生成し、辞書に登録 | パス文字列 `library/images/...` を作るが実体はコピーせず、`paths[id]` は入力パス |
| `get_image_path(id)` | 元のPNGのパスを返す | 一時ファイルが消えれば読めない |
| `enqueue_job` | annotationの辞書エントリが1件増える | DB・スレッド・クラウドの実行は発生しない |

本体の実験は[付加と分類を順に呼ぶ実行例](07-jobs.md)。まず `row = repo.register_capture(shot)` までを実行し、`row.stored_relpath` と `repo.get_image_path(row.id)` を両方表示する。文字列が異なる理由を上表で説明しよう。

### MainWindow の生成式だけを FakeRepository() へ変えたら、同じ画面が動くか。

初回 refresh は currentData() の None を list_images に渡す。Fakeのlist_imagesはSearchQueryを期待してquery.limitに触れるので失敗する。その先もrecord.categoryとcategory_id、import_fileとimport_imageが異なる。変換層か呼出側の移行が要る。

### 授業のデモでFakeを使うとき、再起動後にも写真一覧が残ると言えるか。

検査できるのは同じインスタンス内の登録・検索など。新しいインスタンスは空の辞書で始まる。永続化には別プロセスまたは接続を開き直す試験が要る。

---

[前へ　Qtの起動と終了](02-boot.md)　·　[次へ　音声・画像とAI付加](06-ai.md)　·　[概論へ](../index.md)
