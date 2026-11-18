"""静止したアルバムを対象に、公開APIだけを使って未分類を数える。"""
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from imagebox.core.contracts import RepositoryPort, SearchQuery
from imagebox.dev.fakes import FakeRepository


def count_unclassified(repo: RepositoryPort) -> int:
    total = 0
    while True:
        query = SearchQuery(unclassified_only=True, offset=total, limit=100)
        page = repo.list_images(query)
        total += len(page)
        if len(page) < query.limit:
            return total


if __name__ == "__main__":
    repo = FakeRepository()
    assert count_unclassified(repo) == 0
    with TemporaryDirectory() as folder:
        path = Path(folder) / "board.png"
        Image.new("RGB", (2, 2)).save(path)
        rows = [repo.import_image(str(path)) for _ in range(2)]
        counts = [count_unclassified(repo)]
        repo.set_category(rows[0].id, "other", 0, "manual")
        counts.append(count_unclassified(repo))
        repo.trash_images([rows[1].id])
        counts.append(count_unclassified(repo))
        repo.restore_images([rows[1].id])
        counts.append(count_unclassified(repo))
        assert counts == [2, 1, 0, 1]
        for _ in range(100):
            repo.import_image(str(path))
        assert count_unclassified(repo) == 101
        print(counts, 101)
