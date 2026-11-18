"""教材用の縮小DB。例外を挟んでも、完了と次段登録は一組になるか。"""
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE jobs(stage TEXT PRIMARY KEY, status TEXT NOT NULL)")
with db:
    db.execute("INSERT INTO jobs VALUES ('annotation','processing')")


def complete(fail: bool) -> None:
    with db:
        changed = db.execute(
            "UPDATE jobs SET status='completed' WHERE stage='annotation' AND status='processing'"
        ).rowcount
        if changed != 1:
            raise ValueError("すでに確定したジョブ")
        if fail:
            raise RuntimeError("二つの書込みの間で失敗")
        db.execute("INSERT INTO jobs VALUES ('classification','pending')")


try:
    complete(True)
except RuntimeError:
    print(db.execute("SELECT * FROM jobs").fetchall())
complete(False)
rows = db.execute("SELECT * FROM jobs ORDER BY stage").fetchall()
print(rows)
assert rows == [("annotation", "completed"), ("classification", "pending")]
db.close()
