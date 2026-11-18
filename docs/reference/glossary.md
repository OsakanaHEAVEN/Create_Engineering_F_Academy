# 用語集

| 用語 | このプロジェクトで指すもの | 戻り先 |
|---|---|---|
| import／パッケージ | 名前からモジュールを読み込み、定義した値を参照する。imageboxはsrc内のパッケージ | [実行入口](../lessons/01-python.md) |
| インスタンス／self | クラスから生成した実体／呼ばれたメソッドが受け取る実体 | [参照と実体](../lessons/01-python.md) |
| イベントループ／シグナル | 入力や通知を配送する仕組み／クリックや保存完了の通知 | [起動](../lessons/02-boot.md) |
| Repository／Port | 保存や取得の窓口／呼出側が要求する公開操作の集合 | [契約](../lessons/04-contract.md) |
| dataclass／Protocol | フィールドからメソッド等を生成する仕組み／構造で定義する型の契約 | [同名の型](../lessons/04-contract.md) |
| テストダブル | テスト用の代役。応答を固定するStub、簡易実装のFake、呼ばれ方を検査するMockなど | [差し替え](../lessons/04-contract.md) |
| UUID／主キー | 生成する識別子／行を一意に識別する列。写真名が同じでも別行を識別できる | [取り込み](../lessons/03-storage.md) |
| トランザクション／補償 | 複数のDB操作を一括確定する単位／DBの外で作ったコピー等を失敗後に片付ける処理 | [保存](../lessons/03-storage.md) |
| マイグレーション | 既存データを保持しつつスキーマを変更する手順 | [移行実験](schema.md) |
| PCM／WAV／単調時計 | 音のサンプル列／形式情報を含むファイル／経過時間を測る時計 | [撮影](../lessons/05-capture.md) |
| Provider／Annotation | 解析能力の提供者／説明・タグ・文字起こしと生成情報を運ぶ値 | [AI付加](../lessons/06-ai.md) |
| ジョブ／claim | 後で行う処理を表したデータ／処理の実行権を取得する操作 | [キュー](../lessons/07-jobs.md) |
| 楽観ロック／revision | 読み込み後の変更を保存時に検出する方式／照合する版番号 | [競合](../lessons/07-jobs.md) |
| generation／row_version | 処理の世代／行全体の変更を識別する版。特定の付加版・分類版とも区別 | [状態表](../lessons/07-jobs.md) |
| NFKC／casefold | 全角英字などを比較可能な形へ寄せる正規化／大小文字照合用の変換 | [検索](../lessons/08-album.md) |
| Bearer／認可 | 提示した人を識別する秘密のトークン／識別した人に操作を許すかの判定 | [共有](../lessons/09-sharing.md) |
| multipart | 一つのHTTP本文を複数の名前付き部分に分ける形式 | [2枚の承認](../lessons/09-sharing.md) |
| commit／branch／PR | 内容のスナップショット／先端を指す名前／変更を取り込む前の比較・議論の単位 | [機能変更の実例](../lessons/11-assessment.md) |

---

[前へ　ソース読解索引](code.md)　·　[次へ　調査台帳](audit.md)　·　[概論へ](../index.md)
