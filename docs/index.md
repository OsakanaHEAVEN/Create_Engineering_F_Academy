# Create Engineering F をコードから読む

板書を1枚取り込んだとき、どの関数が画像を複製し、何がSQLiteに入り、誰が画面を書き換えるのか。まずこの問いを実際のGUIで解き、次に同じ写真を撮影音声・AI・共有の設計へ運ぶ。読み終えたら図を閉じ、一枚の写真の一生を自分の言葉で説明しよう。

**初めて読む方は [第1講　Pythonはどのファイルから動くか](lessons/01-python.md) へ。** 実験用のWindowsコマンドは[実験環境](reference/setup.md)、現状を先に照合したいときは[調査台帳](reference/audit.md)へ進む。

## 学習の順序

| 単元 | 進む順序 | 読了後にできること |
|---|---|---|
| I　動いているGUIを読む | [1 実行入口](lessons/01-python.md) → [2 起動とイベント](lessons/02-boot.md) → [3 画像とDB](lessons/03-storage.md) → [保存設計演習](reference/schema.md) | メモリ・ファイル・DBを分け、起動から一枚の取込まで再現できる |
| II　部品間の約束を読む | [4 契約とFake](lessons/04-contract.md) → [5 音声と連写](lessons/05-capture.md) → [6 AI付加](lessons/06-ai.md) | 呼出側と実体を区別し、音声・画像・文字列の境界を説明できる |
| III　複数の処理をつなぐ | [7 ジョブと競合](lessons/07-jobs.md) → [8 分類・検索](lessons/08-album.md) → [9 承認付き共有](lessons/09-sharing.md) | 手動編集・停止・未承認のとき、残るべき値を予測できる |
| IV　自分で説明し、変える | [10 統合追跡](lessons/10-trace.md) → [11 総合演習](lessons/11-assessment.md) | 3経路を描き分け、既存の公開APIから小機能を実装できる |

## 1講ごとの使い方

本文中の値を一つ選び、実行前に「誰が作るか」「どこへ渡るか」「失敗後にどこへ残るか」を紙に書く。次にサンプルかリンク先の関数で確かめ、折りたたみ問題の解答を開く。進捗の単位は、読んだ時間より、**予測と実測を照合した経路の数**にするとよい。付加のジョブと画像行を別々に描けたら第7講の一つの到達点である。

## 調べ直す

[ソース読解索引](reference/code.md)は関数・引数・戻り値・副作用から引ける。[用語集](reference/glossary.md)は用語を扱う講義へ戻るために使う。教材の基準は2026年11月18日に確認したmainの `e7dbd20`。更新時は[調査台帳](reference/audit.md)と[改訂手順](reference/update.md)を一緒に更新する。

---

[次へ　1　Pythonの実行入口](lessons/01-python.md)
