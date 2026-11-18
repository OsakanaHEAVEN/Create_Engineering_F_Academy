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
