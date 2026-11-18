# シャッター前の音声を切り出す

[本編に戻る　5　時間と失敗を扱う](../course/time.md)

音は少しずつ届き、写真の保存が終わったという知らせは後で届きます。どの瞬間の音を残すかを、手で追える4 Hzの例に縮めて見ていきます。

## 三つの部品をつなぐ前に読む

現在の `camera/audio_ring.py` はハードウェアなしで実行できる。Qtの撮影は `examples/help/qt_camera.py` の独立例。`augmentation/audio.py` の `record_wav` は呼んだ時点から指定秒数を録音して待つ関数である。どの部品も、通常起動時に自動でカメラとマイクを開くわけではない。[AudioRingBuffer](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/camera/audio_ring.py#L18-L93) [examples/help/qt_camera.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/examples/help/qt_camera.py) [record_wav](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/src/imagebox/augmentation/audio.py#L7-L25)

PCMは音の振幅を等間隔に数値化した列。モノラル16ビットなら1時点が2バイト。16,000 Hzで5秒あれば `16,000 × 5 = 80,000` サンプル、音の本体は160,000バイト。WAVはこれにサンプルレート・チャネル数等を伴わせる容器である。リングは「直近の数秒しか残らない録音メモ」に似る。ただしこの実装は固定配列を上書きする方式ではなく、時刻付きチャンクを両端キューに積み、古い区間を捨てる。

### 4 Hzなら手で追える

`push([1,2,3,4], timestamp=1.0)` の `1.0` はチャンクの**終端**。開始は `1.0 − 4/4 = 0.0`。次の `[5,6,7,8]` が時刻2.0で終了すると、5は時刻1.00、6は1.25、7は1.50に対応する。`snapshot(1.5)` の右端は含まないので7は入らない。`snapshot` は共有キューをロック下で読み、出力用配列へコピーする。その後の連写・clearでも前の配列は変化しない。

[実験ファイル　sound.py](../labs/sound.py)

```python
"""疑似PCMを実装へ渡して、WAVのヘッダと中身を読み戻す。"""
from array import array
from io import BytesIO
import struct
import wave

from imagebox.camera.audio_ring import AudioRingBuffer

ring = AudioRingBuffer(sample_rate=4, seconds=2)
ring.push([1, 2, 3, 4], timestamp=1.0)
ring.push([5, 6, 7, 8], timestamp=2.0)
first, hz = ring.snapshot(1.5)
ring.push([9, 10, 11, 12], timestamp=3.0)
second, _ = ring.snapshot(3.0)
ring.clear()
print(list(first), list(second))
assert first == array("h", [1, 2, 3, 4, 5, 6])
assert list(second) == list(range(5, 13))

stream = BytesIO()
with wave.open(stream, "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(hz)
    f.writeframes(struct.pack(f"<{len(first)}h", *first))
stream.seek(0)
with wave.open(stream, "rb") as f:
    print(f.getframerate(), f.getnframes())
    assert f.readframes(6) == struct.pack("<6h", 1, 2, 3, 4, 5, 6)
```

この実験は追跡用に保持時間を2秒に短縮した。第2回スナップショットは `[1,3)` なので `[5,…,12]`。WAVにした最初の配列を読み直すと `4 Hz・6フレーム`。実際の5秒設定で10秒と12秒に撮ると `[5,10)` と `[7,12)` の3秒が重なる。開始直後は取得できた分だけ、既存チャンクの間に欠けた時刻はゼロで埋める。切り出しは単調時計、DBに記録する日時はUTC。両者の数値を引き算してはいけない。[tests/test_audio_ring.py](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/tests/test_audio_ring.py)

## 連写の設計を机上実行する

| 順序 | 実行場所 | 値と所有者 |
|---|---|---|
| 1 | Qt例の `shoot` | `captureToFile` が要求IDを返す。負なら例では登録しない。保存完了は後から通知 |
| 2 | 本番の予定 | シャッター時点で独立PCMを確保。要求41に音声A・連番1、要求42に音声B・連番2を対応付ける |
| 3 | `imageSaved(42, filenameB)` | 42をキーにBを取り出す。Bの画像・WAV・UTC・グループ・連番2をCaptureInputにそろえる |
| 4 | `imageSaved(41, filenameA)` | 41からAを取得。同じgroupで連番1。登録成功で初めて画像IDを通知 |

Qt例の `pending` が持つのは撮影先Pathだけ。`saved` は対応を表示して `pop` するところまで。エラーのラムダは表示のみで、保留エントリの掃除まで検証した例ではない。本番契約では録音拒否・音声保存失敗でも、画像が登録できれば `audio_tmp_path=None` で進める。[docs/CONTRACTS.md](https://github.com/OsakanaHEAVEN/Create_Engineering_F/blob/e7dbd20b3e581878729673e2cd82ea60719336e4/docs/CONTRACTS.md) [Qtの画像保存シグナル](https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QImageCapture.html)

### 保存完了が来た瞬間にsnapshotすれば簡単では？

完了通知が2秒遅れれば窓も2秒ずれ、シャッター後の音が入る。過去の時刻を引数にしても、新入力で既にキューから捨てたサンプルは戻らない。シャッター時に切り出し、要求IDで保持する。

### マイクが4 Hzで時刻1と3に各4フレーム届いた。3秒時点の5秒窓の長さと中央の値は？

最初の開始は0。3秒まで12フレームあり、間の[1,2)の4フレームはゼロ。開始以前の2秒は足さない。

---

[前へ　分類と検索](08-album.md)　·　[次へ　ジョブと競合](07-jobs.md)　·　[概論へ](../index.md)
