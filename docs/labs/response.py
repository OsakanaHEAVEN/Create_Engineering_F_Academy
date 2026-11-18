"""ネット送信を行わず、実際の応答検証関数だけを呼ぶ。"""
from imagebox.augmentation.service import _parse_annotation
from imagebox.core.contracts import ValidationError

for payload in ['{"caption":"  RC板書  ","tags":[" 回路 "]}', '[]', '{"caption":"x","tags":[3]}']:
    try:
        a = _parse_annotation(payload, "復習用", "教材モデル")
    except ValidationError as error:
        print(type(error).__name__, str(error))
    else:
        print(a.caption, a.tags, a.transcript, a.prompt_version)
        assert a.tags == ["回路"]
