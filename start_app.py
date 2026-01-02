import sys
import webbrowser
from pathlib import Path

from streamlit.web import cli as stcli

# exe化（frozen）なら exe のあるフォルダを基準にする
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

UI = BASE_DIR / "ui_streamlit.py"


def main():
    # ブラウザを先に開く（起動後でもOKだけど、体感が良い）
    webbrowser.open("http://127.0.0.1:8501")

    # Streamlit CLI を同一プロセスで起動
    sys.argv = [
        "streamlit",
        "run",
        str(UI),
        "--server.address=127.0.0.1",
        "--server.port=8501",
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
    ]
    raise SystemExit(stcli.main())


if __name__ == "__main__":
    main()
