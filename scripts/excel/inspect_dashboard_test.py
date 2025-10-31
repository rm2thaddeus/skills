import json
from pathlib import Path

import pandas as pd


def safe_snapshot(df: pd.DataFrame, rows: int = 8, cols: int = 12):
    subset = df.iloc[:rows, :cols].copy()
    out = []
    for _, row in subset.iterrows():
        formatted = []
        for val in row.tolist():
            if pd.isna(val):
                formatted.append(None)
            else:
                s = str(val)
                if len(s) > 80:
                    s = s[:80]
                formatted.append(s)
        out.append(formatted)
    return out


def main(path: str) -> None:
    p = Path(path)
    x = pd.ExcelFile(p)
    names = x.sheet_names

    med = pd.read_excel(p, sheet_name=names[1], header=None)
    vis = pd.read_excel(p, sheet_name=names[2], header=None)

    result = {
        "sheet_names": names,
        "medecins_head": safe_snapshot(med, rows=8, cols=12),
        "visites_head": safe_snapshot(vis, rows=8, cols=12),
    }
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("{}".format(json.dumps({"error": "missing_path"})))
        raise SystemExit(2)
    main(sys.argv[1])


