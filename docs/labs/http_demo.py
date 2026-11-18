"""元リポジトリ直下を探索パスに加え、例示用FastAPIをプロセス内で呼ぶ。"""
from fastapi.testclient import TestClient
from examples.help.fastapi_server import app

with TestClient(app) as client:
    reply = client.post("/api/users", json={"username": "reader"})
    reply.raise_for_status()
    token = reply.json()["token"]
    me = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    print(me.status_code, me.json()["id"])
    duplicate = client.post("/api/users", json={"username": "reader"})
    print(duplicate.status_code)
    assert me.json() == {"id": "reader"} and duplicate.status_code == 409
