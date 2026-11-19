"""ビルド後の教材をローカルHTTPで開き、読者が使う操作を確認する。"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
handler = partial(SimpleHTTPRequestHandler, directory=str(root / "site"))
with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 950}, locale="ja-JP")
            base = f"http://127.0.0.1:{server.server_port}/"
            page.goto(base)
            assert "概論" in page.locator("article h1").inner_text()
            for img in page.locator("article img").all():
                assert img.evaluate("el => el.complete && el.naturalWidth > 0")
            for chapter in ['起動とイベント', '一枚の画像とSQLite', 'データ型と契約', '非同期処理と更新順序', '検索・共有と変更の影響']:
                page.locator("article a").filter(has_text="次へ").filter(has_text=chapter).click()
                assert chapter in page.locator("article h1").inner_text()
            page.locator("article a").filter(has_text="全Pythonファイルの地図").click()
            page.locator("article summary").filter(has_text="core/repository.py").click()
            assert page.locator("article details[open]").get_by_text("ImageRepository.import_file", exact=False).is_visible()
            page.locator('label[for="__palette_1"]').click()
            assert page.locator("body").get_attribute("data-md-color-scheme") == "slate"
            page.locator("input[data-md-component='search-query']").fill("楽観ロック")
            page.locator(".md-search-result__item:visible").first.wait_for()
            page.locator("input[data-md-component='search-query']").fill("音声")
            page.locator(".md-search-result__item:visible").first.wait_for()
            page.keyboard.press("Escape")
            for lesson in ["course/operate", "lessons/02-boot", "reference/schema", "lessons/07-jobs", "lessons/09-sharing"]:
                page.goto(base + lesson + ".html")
                assert page.locator("article img").evaluate("el => el.complete && el.naturalWidth > 0")
            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(base)
            assert "概論" in page.locator("article h1").inner_text()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator('label.md-header__button[for="__drawer"]').click()
            assert page.locator("#__drawer").is_checked()
            browser.close()
    finally:
        server.shutdown()
        thread.join()
print("概論と実画面・全6章の移動・検索・配色・技術図・モバイルナビを確認しました。")
