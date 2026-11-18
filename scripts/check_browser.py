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
            page.goto(base + "lessons/07-jobs.html")
            page.locator("details summary").first.click()
            assert page.locator("details[open]").count() == 1
            page.locator('label[for="__palette_1"]').click()
            assert page.locator("body").get_attribute("data-md-color-scheme") == "slate"
            page.locator("input[data-md-component='search-query']").fill("楽観ロック")
            page.locator(".md-search-result__item").first.wait_for()
            page.keyboard.press("Escape")
            for lesson in ["lessons/02-boot", "reference/schema", "lessons/07-jobs", "lessons/09-sharing"]:
                page.goto(base + lesson + ".html")
                assert page.locator("article img").evaluate("el => el.complete && el.naturalWidth > 0")
            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(base + "lessons/03-storage.html")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator('label.md-header__button[for="__drawer"]').click()
            assert page.locator("#__drawer").is_checked()
            browser.close()
    finally:
        server.shutdown()
        thread.join()
print("検索・解答・配色・図4枚・モバイルナビを確認しました。")
