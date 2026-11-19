"""同じ写真の記録をDBから二度読み、Pythonの実体と保存値の違いを観察する。"""
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from imagebox.core.repository import ImageRepository


with TemporaryDirectory() as tmp:
    source = Path(tmp) / "board.png"
    Image.new("RGB", (32, 24), "white").save(source)
    repo = ImageRepository(Path(tmp) / "managed")
    try:
        item = repo.import_file(source)
        item.caption = "RC回路の板書"
        item.tags = ["回路", "板書"]
        before = repo.get(item.id)
        assert before is not None
        print(f"{type(item).__module__}.{type(item).__name__}")
        print(f"before={before.caption!r}, same_object={before is item}")
        result = repo.save(item)
        raw = repo.conn.execute("SELECT tags_json FROM images WHERE id=?", (item.id,)).fetchone()
        after = repo.get(item.id)
        assert after is not None
        print(f"save={result!r}, DB={raw['tags_json']}, Python={after.tags!r}")
        print(f"before={before.caption!r}, after={after.caption!r}")
        assert before.id == after.id == item.id and before is not item
        assert before.caption == "" and after.caption == "RC回路の板書"
        assert isinstance(raw["tags_json"], str) and after.tags == ["回路", "板書"]
    finally:
        repo.close()
