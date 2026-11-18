"""同じ実物のFakeRepositoryを最後まで使い、状態を観測する。"""
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from imagebox.core.contracts import Annotation, CaptureInput, ConflictError, SearchQuery
from imagebox.dev.fakes import FakeClassificationProvider, FakeRepository, FakeVisionProvider

with TemporaryDirectory() as tmp:
    path = Path(tmp) / "board.png"
    Image.new("RGB", (32, 24)).save(path)
    repo = FakeRepository()
    t = "2026-11-18T01:00:00Z"
    shot = CaptureInput(str(path), None, t, "1" * 32, 1)
    row = repo.register_capture(shot)
    job = repo.claim_job("annotation", t)
    assert job and job["image_id"] == row.id
    auto = FakeVisionProvider().annotate(str(path), "復習用")
    annotated = repo.complete_annotation_job(job["id"], auto, 0)
    cat = repo.create_category("授業", "復習する資料")
    next_job = repo.claim_job("classification", t)
    selected = FakeClassificationProvider().classify(auto, repo.list_categories())
    result = repo.complete_classification_job(next_job["id"], selected, 0)
    print(row.category_id, annotated.annotation_revision, result.category_id == cat.id)
    assert [r.id for r in repo.list_images(SearchQuery(text="ＲＣ 板書"))] == [row.id]
    edit = Annotation("抵抗とコンデンサ", ["授業"], "", "manual", None, "manual")
    manual = repo.save_annotation(row.id, edit, annotated.annotation_revision, "manual")
    try:
        repo.save_annotation(row.id, auto, manual.annotation_revision, "ai")
    except ConflictError:
        print("手動値を保持", repo.get_image(row.id).caption)
    else:
        raise AssertionError("手動保護の消失")
    repo.trash_images([row.id])
    assert repo.list_images(SearchQuery()) == []
    repo.restore_images([row.id])
    assert repo.get_image(row.id).id == row.id
    repo.trash_images([row.id])
    repo.purge_images([row.id])
    assert path.exists() and not repo.jobs
