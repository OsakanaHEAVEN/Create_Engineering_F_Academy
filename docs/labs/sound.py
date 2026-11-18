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
