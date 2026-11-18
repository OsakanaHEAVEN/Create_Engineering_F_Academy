"""SQLite内の縮小模型。意図的に明示BEGINを使いDDLも同じ確定単位にする。"""
import sqlite3


def migrate(db: sqlite3.Connection, fail: bool = False) -> None:
    if db.execute("PRAGMA user_version").fetchone()[0] == 1:
        return
    with db:
        db.execute("BEGIN")
        db.execute("CREATE TABLE next_images(id TEXT PRIMARY KEY, caption TEXT, revision INTEGER)")
        db.execute("INSERT INTO next_images SELECT id, caption, 0 FROM images")
        if fail:
            raise RuntimeError("移行中断")
        db.execute("DROP TABLE images")
        db.execute("ALTER TABLE next_images RENAME TO images")
        db.execute("PRAGMA user_version=1")


db = sqlite3.connect(":memory:")
with db:
    db.execute("CREATE TABLE images(id TEXT PRIMARY KEY, caption TEXT)")
    db.execute("INSERT INTO images VALUES (?,?)", ("P", "RC回路"))
try:
    migrate(db, fail=True)
except RuntimeError:
    assert db.execute("PRAGMA user_version").fetchone() == (0,)
    assert db.execute("SELECT * FROM images").fetchall() == [("P", "RC回路")]
migrate(db)
migrate(db)
print(db.execute("PRAGMA user_version").fetchone(), db.execute("SELECT * FROM images").fetchall())
assert db.execute("SELECT * FROM images").fetchall() == [("P", "RC回路", 0)]
db.close()
