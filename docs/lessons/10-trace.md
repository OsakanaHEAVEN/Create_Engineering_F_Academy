# 10　統合講義　同じ板書写真を三つの入口から追う

**到達点**　「この画像が画面に出るまで」を、関数・オブジェクト・ディスク・未接続区間を区別してホワイトボードに描く。第2〜9講を使う。表の `P` は1枚の論理上の写真の記号で、別実行のUUIDが一致するという意味はない。

## 通常のmainで板書を取り込む

`IMAGEBOX_DATA_DIR` を空の専用フォルダにして起動するケース。誰もカメラのシャッターを押していない。

| 時点 | 実行主体と呼出し | 値・副作用 | 目で確認できる結果 |
|---|---|---|---|
| 0 | `main → QApplication → MainWindow → ImageRepository` | `images.sqlite3` と `images/`、画像行0 | 初回refresh後の一覧は空 |
| 1 | クリック→ `add_image → getOpenFileNames` | `["D:/class/board.png"]`。キャンセルなら空リスト | まだ写真行は増えない |
| 2 | `repo.import_file → copy2 → save` | `images/P.png` とDB行 `P, other, "", "[]"`。元写真はそのまま | 戻り値は旧ImageRecord |
| 3 | `refresh → list_images(None)` | DB行→新しい実体→表示文字列 | 元名・その他・空の説明 |
| 4 | 種別「メモ・板書・資料」を選ぶ | `currentData()=="notes"`。SQLがotherを除外 | 一覧から消えても画像は残る |
| 5 | 閉じて再起動 | 接続を閉じ、同じルートを開き直す | 「すべて」でPが再び表示される |

「なぜAI説明がまだ出ないか」への答えは、ここにはジョブを作る呼出しがないからである。APIキーを設定してもこの呼出し列は変わらない。[実際の取込実験](03-storage.md) [MainWindow.refresh](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/ui/main_window.py#L64-L70)

## 契約テストで撮影後を再現する

`test_example_standalone_flow_without_other_roles` は画像を生成し、自分自身が段取りを進める。テスト関数がワーカーの代わりにclaim・completeを順番に呼ぶため、「待てば進む」システムではない。[test_example_standalone_flow_without_other_roles](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_contract_bootstrap.py#L49-L88)

| 時点 | 誰が何を渡すか | 更新先と観測値 |
|---|---|---|
| 1 | テスト→ `CaptureInput(image_tmp_path, None, UTC, group, 1)` → `register_capture` | FakeのrecordsとpathsにP、jobsにJ1。音声なし。実DB行0 |
| 2 | テスト→ `claim_job` → `FakeVisionProvider.annotate(path, "授業中")` | J1処理中。戻る説明は固定の「制御工学のRC回路の板書」。実API呼出し0 |
| 3 | テスト→ `complete_annotation_job(J1,a,0)` | P.captionと付加版1、J1完了、J2待機 |
| 4 | カテゴリ「授業」を作り、分類をclaim・classify・complete | PにカテゴリIDが入り、分類完了 |
| 5 | `FakeSearch(repo).search(SearchQuery(text="制御工学 RC"))` | Pを含むリスト。Qtへの通知・描画は発生しない |
| 6 | `trash_images → restore_images` | 通常検索件数が1→0→1。同じP。ディスク上の入力はそのまま |

## 設計上の結合　境界で一度止める

実装がある部品を矢印で並べても、結線するコードがなければ一連の動作にはならない。次の表は設計上の呼出し順と、現在の検証の切れ目を重ねたもの。[docs/INTEGRATION.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/INTEGRATION.md) [docs/ACCEPTANCE_TESTS.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/ACCEPTANCE_TESTS.md)

| シナリオ | 予定の関数・値・時系列 | 現在観測できる部分 |
|---|---|---|
| 起動 | 新Repositoryの初期化・移行→2ワーカー開始→GUI | 現GUIは旧DBを開く。新ワーカーの生成なし |
| カメラを開く・撮る | セッション開始→マイクPCM追加→シャッターでsnapshot(t)→要求41 | Qt撮影は独立例、時刻窓は実クラス |
| 直前音声と登録 | 41の保存完了→対応PCMをWAV化してCaptureInput→登録。音声失敗はNone→管理画像と行とJ1→image_captured(P) | [PCM/WAV実験](05-capture.md)・Fakeへの登録を個別に実行可能 |
| 付加→分類 | J1取得→音声文字列＋画像→Annotation→同一トランザクションでJ2追加→カテゴリ一覧からID→分類完了 | Whisper関数とGemini Vision部品は実コード。自動結線・本番分類Providerは未実装 |
| アルバムの表示 | ワーカーが変更IDを通知→GUIスレッドがRepositoryを再読込→Pを描画 | 旧GUIのrefreshは呼出しで動く。v2完了イベント未接続 |
| 手動caption修正中にAIが戻る | 手動値を先に保存し付加版0→1。古い期待版0を拒否→手動値保持 | Fakeで競合を実行可能。旧GUIには編集画面がない |
| APIに失敗 | 写真を残し、種類に応じて待機・有限回の再試行・failed・手動retry | 検証関数は例外を返す。通常GUIはこの要求を発生させない |
| 処理中に強制終了 | 永続jobsのprocessingを起動時に点検→回収→同世代の重複を避けて再開 | Fake辞書は失われ、旧DBにjobs表はない |
| 削除・復元・完全削除 | 通常一覧から除外→復元は同じID→明示purgeで管理画像・音声を削除 | Fakeで状態遷移。旧GUIの一括削除は即時削除 |
| 共有依頼・複数承認 | A→R作成→B端末で候補Pと手動Q→2枚承認→F1,F2→Aが受信 | 候補計算と認証例まで。実ファイル転送は[第9講](09-sharing.md)の予定フロー |

<details markdown="1">
<summary>画面は『その他』を表示し、契約テストはNoneを返した。同じ写真について二つの観測が両立する理由を、型と入口で答える。</summary>

起動入口はMainWindow→旧ImageRepository→models.ImageRecordで初期other。契約テスト入口はFakeRepository→contracts.ImageRecordで初期None。データベースもインスタンスも共有していない。

</details>

<details markdown="1">
<summary>ジョブ完了後に画面が変わらない。どこまでを別々に観測するか。</summary>

完了処理の戻り値と永続行、通知の発行、GUIスレッドでの受信、再読込したRepositoryが同じ保存先か、フィルタでPが隠れていないかを順に確認する。調査SHAでFakeを動かしただけならGUIへの接続自体がない。

</details>

最後の演習では、既存コードに小さな拡張を加え、どの証拠で完了を判断するかを決める。

---

[前へ　9　承認付き共有](09-sharing.md)　·　[次へ　11　総合演習](11-assessment.md)
