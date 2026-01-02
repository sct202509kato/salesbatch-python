import subprocess
import sys
from pathlib import Path

import streamlit as st

APP_TITLE = "売上集計ツール（ローカル）"

PROJECT_DIR = Path(__file__).resolve().parent
RUNPY = PROJECT_DIR / "run.py"
OUT_FILE = PROJECT_DIR / "output" / "sales_summary.xlsx"

st.set_page_config(page_title=APP_TITLE)
st.title(APP_TITLE)

st.write("1) input フォルダに Excel/CSV を入れる → 2) 実行ボタンを押す")

col1, col2 = st.columns(2)
with col1:
    st.code(str((PROJECT_DIR / "input").resolve()))
with col2:
    st.code(str((PROJECT_DIR / "output").resolve()))

if st.button("実行"):
    st.info("集計を実行しています…")
    proc = subprocess.run(
        [sys.executable, str(RUNPY)],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True,
    )

    if proc.stdout:
        st.text(proc.stdout)
    if proc.stderr:
        st.error(proc.stderr)

    if proc.returncode == 0 and OUT_FILE.exists():
        st.success("完了しました！")
        with open(OUT_FILE, "rb") as f:
            st.download_button(
                label="サマリーExcelをダウンロード",
                data=f,
                file_name="sales_summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.error("失敗しました。ログを確認してください。")
