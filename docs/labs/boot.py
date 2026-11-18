"""ディスプレイなしで通常のmain()を通し、イベントループ内で画面を閉じる。"""
import os
from pathlib import Path
from tempfile import TemporaryDirectory

os.environ["QT_QPA_PLATFORM"] = "offscreen"
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from imagebox.__main__ import main
from imagebox.ui.main_window import MainWindow

seen = []


def inspect_and_close():
    app = QApplication.instance()
    window = next(w for w in app.topLevelWidgets() if isinstance(w, MainWindow))
    tabs = window.centralWidget()
    seen.extend(tabs.tabText(i) for i in range(tabs.count()))
    print(seen, window.image_list.count())
    window.close()


with TemporaryDirectory() as folder:
    os.environ["IMAGEBOX_DATA_DIR"] = folder
    # main() 自身が QApplication を生成するため、イベント登録は生成直後に行う。
    original = MainWindow.show

    def show_and_schedule(self):
        original(self)
        QTimer.singleShot(0, inspect_and_close)

    MainWindow.show = show_and_schedule
    try:
        code = main()
    finally:
        MainWindow.show = original
    assert code == 0 and seen == ["分類", "付加", "共有"]
    assert (Path(folder) / "images.sqlite3").is_file()
