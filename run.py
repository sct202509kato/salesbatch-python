from pathlib import Path
import pandas as pd

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def read_one_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in [".xlsx", ".xls"]:
        # Excel
        return pd.read_excel(path)
    elif path.suffix.lower() == ".csv":
        # CSV（文字コード対策）
        for enc in ["utf-8-sig", "cp932", "utf-8"]:
            try:
                return pd.read_csv(path, encoding=enc)
            except UnicodeDecodeError:
                continue
        return pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file: {path.name}")


def main():
    files = sorted(
        list(INPUT_DIR.glob("*.xlsx"))
        + list(INPUT_DIR.glob("*.xls"))
        + list(INPUT_DIR.glob("*.csv"))
    )
    if not files:
        print(f"No files found in {INPUT_DIR.resolve()}")
        return

    dfs = []
    for f in files:
        try:
            df = read_one_file(f)
            df["__source_file"] = f.name
            dfs.append(df)
            print(f"Loaded: {f.name} rows={len(df)}")
        except Exception as e:
            print(f"Skipped: {f.name} error={e}")

    if not dfs:
        print("No readable files.")
        return

    data = pd.concat(dfs, ignore_index=True)

    required = ["date", "product", "amount"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        print("Missing columns:", missing)
        print("Current columns:", list(data.columns))
        print("→ 列名が違う場合は COLUMN_MAP を追加してください")
        return

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")

    by_product = (
        data.dropna(subset=["amount"])
        .groupby("product", dropna=False)["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    data["month"] = data["date"].dt.to_period("M").astype(str)
    by_month = (
        data.dropna(subset=["amount"])
        .groupby("month")["amount"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    out_path = OUTPUT_DIR / "sales_summary.xlsx"
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="merged_raw", index=False)
        by_product.to_excel(writer, sheet_name="by_product", index=False)
        by_month.to_excel(writer, sheet_name="by_month", index=False)

    print(f"Done: {out_path.resolve()}")


if __name__ == "__main__":
    main()
