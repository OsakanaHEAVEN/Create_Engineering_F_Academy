"""各教材実験を独立プロセスで実行する。環境準備は資料室に記載。"""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
for lab in sorted((root / "docs/labs").glob("*.py")):
    print(f"\n--- {lab.name} ---", flush=True)
    subprocess.run([sys.executable, str(lab)], check=True)
