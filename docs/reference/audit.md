# 調査台帳　どの時点の何を読んだか

調査基準は **2026年11月18日 10:55 JST（01:55 UTC）**。GitHubから全ブランチ先端と再帰ツリーを取得し、mainのソース・例・テスト・README・設計文書を固定SHAで取得した。ブランチ名は動くため、下記リンクはコミットを指す。

| 参照ブランチ | 調査したHEAD | 本文での扱い |
|---|---|---|
| main | [e7dbd20b3e581878729673e2cd82ea60719336e4](https://github.com/OsakanaHEAVEN/Create_Engineering_F/tree/e7dbd20b3e581878729673e2cd82ea60719336e4) | 講義の基準。旧GUI・新契約・独立例が共存 |
| docs/full-design-audit | [2075cadc605623e159bca6a204df4ef5df2b6964](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/2075cadc605623e159bca6a204df4ef5df2b6964/docs/PROJECT_DESIGN_AUDIT_AND_COMPLETION_PLAN.md#L617) | 監査・契約草案に「追加合意が必要」とある。こちらのAPI案をmainに転記していない |
| feat/augmentation-yoshimura | [d64db6cbe0271c768e64d7352e21899f565802ef](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/d64db6cbe0271c768e64d7352e21899f565802ef/src/imagebox/augmentation/service.py) | 旧Ollamaへの呼出関数がある。mainの同名ファイルはGeminiVisionProvider |

## 機能の判定

「GUI稼働」は通常入口から到達可能、「部品」は明示的に呼べる本体コード、「独立例」はexamplesを別起動、「Fake」は開発用の代替、「設計」は文書または型に示され、対応する完成部品がmainに見当たらないものを指す。外部サービス・実機の成功を静的読解だけで認定しない。

| 機能 | 実装区分と食い違い | 根拠 |
|---|---|---|
| 起動・取込・一覧 | GUI稼働。`MainWindow` が旧保存層を直接生成。新保存層の注入やワーカー開始なし | [src/imagebox/__main__.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/__main__.py) [src/imagebox/ui/main_window.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py) [docs/INTEGRATION.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/INTEGRATION.md) |
| 保存形式 | 旧DBはimages表・絶対パス・固定5分類。設計の複数表、相対パス、起動時回復・移行は未実装 | [src/imagebox/core/repository.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py) [docs/DATA_SCHEMA.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/DATA_SCHEMA.md) |
| 新Port | 型あり。Fakeは辞書に保存しパスは元ファイルを指す。初期カテゴリはotherの1件、SHAは固定文字列 | [src/imagebox/core/contracts.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/contracts.py) [src/imagebox/dev/fakes.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py) |
| カメラ・撮影前録音 | デバイス例と本体PCMリングあり。WAV録音関数は呼出し後の録音。要求ID照合から登録までの本体コントローラーなし | [examples/help/qt_camera.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/qt_camera.py) [src/imagebox/camera/audio_ring.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py) [src/imagebox/augmentation/audio.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py) |
| Speech・Vision | 音声認識関数とGemini付加は実部品。SpeechProviderの`transcribe`と実関数`transcribe_wav`の結線が必要。実API・実音声は今回未試験 | [src/imagebox/augmentation/service.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/service.py) [tests/test_whisper_cache.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_whisper_cache.py) |
| 用途分類 | 旧規則とFakeは実行可能。動的カテゴリをAPIへ送る本番分類器は設計 | [src/imagebox/classification/service.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/classification/service.py) [docs/classification/CATEGORY_POLICY.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/classification/CATEGORY_POLICY.md) |
| ジョブ・競合 | Fakeにclaim・complete・手動保護。永続jobs、原子的claim、再起動回復は設計 | [tests/test_contract_bootstrap.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_contract_bootstrap.py) [docs/CONTRACTS.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/CONTRACTS.md) |
| 編集・ごみ箱 | 新Port/Fakeで部分更新・trash。旧GUIの分類一括削除は物理削除。旧・新の同名delete_categoryは意味が違う | [ImageRepository.delete_category](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/core/repository.py#L118-L132) [FakeRepository.delete_category](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L203-L214) |
| 共有 | ローカル候補・明示承認チェックの部品、独立認証デモあり。所有者側検索、製品用HTTPルート・複数枚転送・サーバーDBは設計 | [src/imagebox/sharing/service.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py) [examples/help/fastapi_server.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/fastapi_server.py) [docs/sharing/API_DESIGN.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/sharing/API_DESIGN.md) |

## コードを正しいと仮定しないための照合

1. **補償の限界**　旧保存層はコピー後のDB例外を処理するが、強制終了や削除コミット後のunlink失敗にまたがる整合性回復はない。第3講で失敗位置ごとに確認する。
2. **Fakeの検索順位**　契約にrelevanceがあるがFakeは日時・ID順。カテゴリ削除とtrashが組み合わさる場合、Fakeは対象行を更新できないことがある。第8講で読み解く。
3. **次段の重複**　Fakeのenqueueは世代一意性を検査せず新しいUUIDを発行する。メソッドの存在は並行時の一意性の証拠にならない。第7講のSQL模型で分離する。
4. **障害の型**　RateLimitedが契約にあってもVision部品のgenerate_content例外をそこに翻訳する処理は見当たらない。実サービスの値と契約上の値の間に処理が必要。
5. **受入と単体テスト**　ソース同梱35ケースの成功は、C/A/S全48項目の完了数と一致しない。例のcompile、Fake、モデル差し替えを含むからである。

## 今回の検証範囲

固定SHAのmainを対象に、LinuxのPython 3.12、Pillow 12系・Qt for Python 6系で元のpytestが35件成功した。教材の実験ではダミー画像、一時DB、Qt offscreen、TestClientを使った。Windowsの実カメラ・マイク、実Gemini、独立の2台間通信、電源断実機試験は未検証。更新時は[再調査手順](update.md)に従う。

---

[前へ　用語集](glossary.md)　·　[次へ　改訂・公開手順](update.md)
