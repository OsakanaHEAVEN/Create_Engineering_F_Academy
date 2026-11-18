"""元アプリの旧Repositoryを一時ディレクトリで呼ぶ。"""
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from imagebox.core.repository import ImageRepository

with TemporaryDirectory() as tmp:
    root = Path(tmp)
    source = root / "board.png"
    Image.new("RGB", (32, 24), "white").save(source)
    repo = ImageRepository(root / "managed")
    try:
        row = repo.import_file(source)
        row.tags.append("回路")
        repo.save(row)
        raw = repo.conn.execute(
            "SELECT category,tags_json FROM images WHERE id=?", (row.id,)
        ).fetchone()
        print(raw["category"], raw["tags_json"], repo.get(row.id).tags)
        copy = Path(row.stored_path)
        assert source.exists() and copy.exists() and copy != source
    finally:
        repo.close()
    reopened = ImageRepository(root / "managed")
    try:
        assert reopened.get(row.id).tags == ["回路"]
        assert reopened.delete_category("other") == 1
        print(source.exists(), copy.exists(), reopened.get(row.id))
    finally:
        reopened.close()
