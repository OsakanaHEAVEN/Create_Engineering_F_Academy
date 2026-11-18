"""Markdown内の相対リンク、埋込みラボ、ナビゲーション、公開先の固定リンクを検査。"""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import yaml

root = Path(__file__).resolve().parents[1]
docs = root / "docs"
pages = sorted(docs.rglob("*.md"))
config = yaml.safe_load((root / "mkdocs.yml").read_text(encoding="utf-8"))
errors = []


def nav_paths(node):
    if isinstance(node, str):
        yield docs / node
    elif isinstance(node, list):
        for item in node:
            yield from nav_paths(item)
    elif isinstance(node, dict):
        for child in node.values():
            yield from nav_paths(child)


if set(nav_paths(config["nav"])) != set(pages):
    errors.append("目次とMarkdownページが一致しません")
for page in [*pages, root / "README.md"]:
    body = page.read_text(encoding="utf-8")
    # サンプル中のPythonのリストなどをMarkdownとして判定しない。
    prose = re.sub(r"^(```|~~~).*?^\1\s*$", "", body, flags=re.M | re.S)
    for target in re.findall(r"\]\(([^)\s]+)\)", prose):
        link = urlsplit(target)
        if not link.scheme and link.path and not (page.parent / unquote(link.path)).exists():
            errors.append(f"{page.name}: リンク先なし {target}")
        if "/OsakanaHEAVEN/Create_Engineering_F/blob/" in target:
            if not re.search(r"/blob/[0-9a-f]{40}/", target):
                errors.append(f"{page.name}: 固定されていない参照 {target}")
    for lab, code in re.findall(
        r"\[実験ファイル　\w+\.py\]\(([^)]+)\)\s+```python\n(.*?)\n```", body, re.S
    ):
        if code != (page.parent / lab).read_text(encoding="utf-8").strip():
            errors.append(f"{page.name}: 実験本文と{lab}が不一致")
    if body.count("<details ") != body.count("</details>"):
        errors.append(f"{page.name}: 解答欄が閉じていません")
if errors:
    raise SystemExit("\n".join(errors))
print(f"{len(pages)}ページの目次・リンク・実験本文を確認しました。")
