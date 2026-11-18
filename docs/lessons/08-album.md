# 8　分類・検索・ごみ箱で、同じ写真の見え方が変わる

**到達点**　検索結果を手計算し、写真の非表示・カテゴリ削除・完全削除を区別する。第3講の旧レコード、第7講で作った新レコードを使う。

## ラベル、用途、検索語を区別する

図書館で「電気回路」という件名と、「明日の復習」という利用目的は別である。画像のタグと用途カテゴリも別々に持つ。さらに検索はラベルを再決定せず、今あるレコードから条件を満たすものを取り出す。図書館の棚と異なり、同じ画像が複数の検索結果に現れてもコピーは増えない。

| 経路 | 判定 | 板書写真の結果 |
|---|---|---|
| 旧分類 `classify_by_rules` | captionとtranscriptを連結しlower。辞書順で最初に当たった語の分類を返す | 「旅行の板書」はnotes。GUI取り込み直後はこの関数を呼ばないのでother |
| Fakeの `classify` | 最新一覧に「授業」という名前があればそのID、なければother | キャプションを替えてもこの規則は一定 |
| 新設計の分類Provider | Annotation＋カテゴリID・名前・説明をテキストAPIへ。返ったIDが入力一覧にあるか検証 | 名前変更時もIDは維持。失敗は未分類のまま。実クラウド分類器は未収録 |
| Fakeの `list_images(SearchQuery)` | 通常一覧はactiveだけ。NFKC→casefold→空白分割→各語がどこかに含まれるAND | `ＲＣ　板書` は `rc` と `板書` に変わり、両方必要 |

NFKCは互換表現を正規化し、casefoldは大小文字を照合用にそろえる。Fakeではcaption、transcript、tags、元名を連結する。空の語列に対する `all` は真なので空検索は他の条件に合う全件。日時範囲は開始を含み終了を含まない。撮影日がなければ取込日。文字列比較のため日時表現を同一形式にそろえる前提がある。最後に時刻・IDで並べ、offsetからlimit件を切り出す。`sort="relevance"` でもFakeは関連度計算を行わない。[FakeRepository.list_images](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L115-L142) [classify_by_rules](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/classification/service.py#L9-L21) [docs/classification/CATEGORY_POLICY.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/classification/CATEGORY_POLICY.md)

### 旧共有候補は別の計算

隣り合う2文字の集合をbigramと呼ぶ。`書回図` は {書回, 回図}、`板書回路` は {板書, 書回, 回路}。共通1種類、和集合4種類なので `1/4=0.25`。既定閾値0.15を超え候補になる。元文字列の大小をそろえた部分一致があれば得点を1以上へ引き上げ、同点はID順。候補になっただけでは承認済みにならない。[match_candidates](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/sharing/service.py#L23-L39)

[実験ファイル　search.py](../labs/search.py)

```python
"""旧共有候補、新検索の前処理、旧分類を同じ入力で比較する。"""
from imagebox.classification.service import classify_by_rules
from imagebox.core.models import ImageRecord
from imagebox.dev.fakes import _normalize
from imagebox.sharing.service import approved_image_path, match_candidates

row = ImageRecord("p1", "private/p1.png", "board.png", "2026-11-18", caption="板書回路")
print(classify_by_rules(row.caption), _normalize(" ＲＣ　板書  "))
candidate, = match_candidates("書回図", [row])
print(candidate.image_id, candidate.score)
assert candidate.score == 0.25
try:
    approved_image_path("p1", set(), [row])
except PermissionError:
    print("未承認")
assert approved_image_path("p1", {"p1"}, [row]) == "private/p1.png"
```

### 何を「削除」したのか

| 呼出し | 行・ファイルへの作用 | 復元 |
|---|---|---|
| 旧GUIの `delete_category("notes")` | その分類の写真行と管理画像を削除。分類キー自体は固定 | GUIから戻せない。元取込画像は残る |
| v2の `delete_category(id)` | カテゴリ行を消し、所属写真をotherへ移す契約 | 写真は残る。other自体は保護 |
| Fakeの `trash_images([P])` | storage_stateがtrash。通常取得と検索から外す | restoreで同じIDが再び見える |
| Fakeの `purge_images([P])` | trashだけが対象。レコード・パス辞書・関連ジョブを消す | Fakeは入力ファイルを消さない。予定の本物は管理画像・音声を消す |

例えばFakeでは復元時に直接 `replace` を使い、`row_version` や更新時刻を増やさない。また、ごみ箱に所属画像があるカテゴリを削除すると `_write` がactive限定の取得を使うため `NotFoundError` になりうる。複数件の変更中なら先行分だけ進む可能性がある。DB版の同一トランザクションを検証する材料になる。[FakeRepository.delete_category](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L203-L214) [FakeRepository.restore_images](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/dev/fakes.py#L227-L234)

<details markdown="1">
<summary>カテゴリ未設定とotherを両方「その他」と表示した。何が検査できなくなるか。</summary>

AI未処理・失敗の写真と、処理済みで「その他」を選んだ写真を区別できない。前者はcategory_id=None、後者はotherを検索条件に使う。

</details>

<details markdown="1">
<summary>「ＲＣ」「板書」が別々のフィールドにあってもFakeで見つかるか。</summary>

見つかる。対象フィールドを先に一つの文字列へ連結し、全語の存在を調べる。旧GUIのフィルタはcategory一致だけなのでこの検索を呼ばない。

</details>

次の章では、検索が所有者の端末内で終わり、承認が初めて通信を許す境界を読む。

---

[前へ　7　ジョブと競合](07-jobs.md)　·　[次へ　9　承認付き共有](09-sharing.md)
