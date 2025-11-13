import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt
import json


def find_latest_op(artifacts_root: Path) -> Optional[Path]:
    ops = [p for p in artifacts_root.glob("*/") if p.is_dir()]
    if not ops:
        return None
    ops_sorted = sorted(ops, key=lambda p: p.stat().st_mtime, reverse=True)
    return ops_sorted[0]


def load_datasets(op_dir: Path, interviews_xlsx: Optional[Path], applications_xlsx: Optional[Path]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    enriched = op_dir / "output" / "enriched"
    i_path = interviews_xlsx or (enriched / "interviews_dataset.xlsx")
    a_path = applications_xlsx or (enriched / "applications_dataset.xlsx")
    interviews = pd.read_excel(i_path) if i_path.exists() else pd.DataFrame()
    applications = pd.read_excel(a_path) if a_path.exists() else pd.DataFrame()
    # Parse dates
    if not interviews.empty:
        interviews["event_datetime"] = pd.to_datetime(interviews.get("event_datetime"), errors="coerce")
        if "event_year" not in interviews:
            interviews["event_year"] = interviews["event_datetime"].dt.year
    if not applications.empty:
        applications["applied_date"] = pd.to_datetime(applications.get("applied_date"), errors="coerce")
        if "year" not in applications:
            applications["year"] = applications["applied_date"].dt.year
    return interviews, applications


def load_manual_periods(config_path: Optional[str]) -> dict:
    if not config_path:
        return {}
    p = Path(config_path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def ensure_out_dir(op_dir: Path) -> Path:
    charts = op_dir / "output" / "charts"
    charts.mkdir(parents=True, exist_ok=True)
    return charts


def monthly_counts(series: pd.Series) -> pd.Series:
    if series.empty:
        return pd.Series(dtype=int)
    s = series.dropna()
    if s.empty:
        return pd.Series(dtype=int)
    return (
        s.dt.to_period("M")
         .astype(str)
         .value_counts()
         .rename_axis("month")
         .sort_index()
    )


def daily_counts(series: pd.Series, year: int) -> pd.Series:
    if series.empty:
        return pd.Series(dtype=int)
    s = series.dropna()
    if s.empty:
        return pd.Series(dtype=int)
    # Filter to year and resample to day with 0 fill
    s = s[s.dt.year == year]
    if s.empty:
        return pd.Series(dtype=int)
    df = (
        s.dt.floor("D")
         .value_counts()
         .rename_axis("date")
         .sort_index()
         .rename("count")
         .to_frame()
    )
    full = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")
    df = df.reindex(full, fill_value=0)
    return df["count"]


def plot_apps_vs_interviews_monthly(charts: Path, interviews: pd.DataFrame, applications: pd.DataFrame, year: int) -> Optional[Path]:
    apps_monthly = monthly_counts(applications[applications["year"] == year]["applied_date"]) if not applications.empty else pd.Series(dtype=int)
    ints_monthly = monthly_counts(
        interviews[(interviews["event_year"] == year) & (interviews.get("event_type").fillna("") == "interview")]["event_datetime"]
    ) if not interviews.empty else pd.Series(dtype=int)

    # Align indices
    all_months = sorted(set(apps_monthly.index) | set(ints_monthly.index))
    if not all_months:
        return None
    apps = apps_monthly.reindex(all_months, fill_value=0)
    ints = ints_monthly.reindex(all_months, fill_value=0)

    plt.figure(figsize=(12, 5))
    plt.plot(all_months, apps.values, marker="o", label="Applications")
    plt.plot(all_months, ints.values, marker="o", label="Interviews")
    plt.title(f"Applications vs Interviews per Month - {year}")
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = charts / f"apps_vs_interviews_monthly_{year}.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_apps_interviews_outreach_monthly(charts: Path, interviews: pd.DataFrame, applications: pd.DataFrame, year: int) -> Optional[Path]:
    if interviews.empty and applications.empty:
        return None
    apps_monthly = monthly_counts(applications[applications["year"] == year]["applied_date"]) if not applications.empty else pd.Series(dtype=int)
    ints_monthly = monthly_counts(
        interviews[(interviews["event_year"] == year) & (interviews.get("event_type").fillna("") == "interview")]["event_datetime"]
    ) if not interviews.empty else pd.Series(dtype=int)
    out_monthly = monthly_counts(
        interviews[(interviews["event_year"] == year) & (interviews.get("event_type").fillna("") == "outreach")]["event_datetime"]
    ) if not interviews.empty else pd.Series(dtype=int)

    all_months = sorted(set(apps_monthly.index) | set(ints_monthly.index) | set(out_monthly.index))
    if not all_months:
        return None
    apps = apps_monthly.reindex(all_months, fill_value=0)
    ints = ints_monthly.reindex(all_months, fill_value=0)
    outs = out_monthly.reindex(all_months, fill_value=0)

    plt.figure(figsize=(12, 5))
    plt.plot(all_months, apps.values, marker="o", label="Applications")
    plt.plot(all_months, ints.values, marker="o", label="Interviews")
    plt.plot(all_months, outs.values, marker="o", label="Outreach")
    plt.title(f"Applications, Interviews, Outreach per Month - {year}")
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = charts / f"apps_interviews_outreach_monthly_{year}.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_yearly_grouped(charts: Path, interviews: pd.DataFrame, applications: pd.DataFrame) -> Optional[Path]:
    if interviews.empty and applications.empty:
        return None
    years = [y for y in [2022, 2025] if ((applications.get("year") == y).any() or (interviews.get("event_year") == y).any())]
    if not years:
        return None
    apps_counts = [int((applications["year"] == y).sum()) for y in years]
    ints_counts = [int(((interviews["event_year"] == y) & (interviews.get("event_type").fillna("") == "interview")).sum()) for y in years]

    import numpy as np
    x = np.arange(len(years))
    width = 0.35
    plt.figure(figsize=(7, 5))
    plt.bar(x - width/2, apps_counts, width, label="Applications")
    plt.bar(x + width/2, ints_counts, width, label="Interviews")
    plt.xticks(x, [str(y) for y in years])
    plt.ylabel("Count")
    plt.title("Applications vs Interviews by Year")
    for i, v in enumerate(apps_counts):
        plt.text(x[i] - width/2, v + 0.5, str(v), ha="center", va="bottom", fontsize=9)
    for i, v in enumerate(ints_counts):
        plt.text(x[i] + width/2, v + 0.5, str(v), ha="center", va="bottom", fontsize=9)
    plt.legend()
    plt.tight_layout()
    out = charts / "apps_vs_interviews_by_year.png"
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_events_by_type_year(charts: Path, interviews: pd.DataFrame) -> Optional[Path]:
    if interviews.empty or "event_type" not in interviews:
        return None
    df = interviews.copy()
    counts = (
        df.groupby(["event_year", "event_type"]).size().rename("count").reset_index()
    )
    if counts.empty:
        return None
    import numpy as np
    years = sorted(counts["event_year"].dropna().unique().tolist())
    types = sorted(counts["event_type"].dropna().unique().tolist())
    x = np.arange(len(years))
    width = 0.8 / max(1, len(types))
    plt.figure(figsize=(8, 5))
    for i, t in enumerate(types):
        vals = [int(counts[(counts["event_year"] == y) & (counts["event_type"] == t)]["count"].sum()) for y in years]
        plt.bar(x + (i - (len(types)-1)/2) * width, vals, width, label=t.title())
        for j, v in enumerate(vals):
            plt.text(x[j] + (i - (len(types)-1)/2) * width, v + 0.5, str(v), ha="center", va="bottom", fontsize=8)
    plt.xticks(x, [str(y) for y in years])
    plt.ylabel("Count")
    plt.title("Events by Type and Year")
    plt.legend()
    plt.tight_layout()
    out = charts / "events_by_type_by_year.png"
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_outreach_direction_by_year(charts: Path, interviews: pd.DataFrame) -> Optional[Path]:
    if interviews.empty or "direction" not in interviews or "event_type" not in interviews:
        return None
    df = interviews[interviews["event_type"] == "outreach"].copy()
    if df.empty:
        return None
    counts = df.groupby(["event_year", "direction"]).size().rename("count").reset_index()
    import numpy as np
    years = sorted(counts["event_year"].dropna().unique().tolist())
    dirs = sorted([d for d in counts["direction"].dropna().unique().tolist()])
    x = np.arange(len(years))
    width = 0.8 / max(1, len(dirs))
    plt.figure(figsize=(8, 5))
    for i, d in enumerate(dirs):
        vals = [int(counts[(counts["event_year"] == y) & (counts["direction"] == d)]["count"].sum()) for y in years]
        plt.bar(x + (i - (len(dirs)-1)/2) * width, vals, width, label=d.title())
        for j, v in enumerate(vals):
            plt.text(x[j] + (i - (len(dirs)-1)/2) * width, v + 0.5, str(v), ha="center", va="bottom", fontsize=8)
    plt.xticks(x, [str(y) for y in years])
    plt.ylabel("Count")
    plt.title("Outreach Direction by Year")
    plt.legend()
    plt.tight_layout()
    out = charts / "outreach_direction_by_year.png"
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_interviews_by_medium_year(charts: Path, interviews: pd.DataFrame) -> Optional[Path]:
    if interviews.empty or "medium" not in interviews:
        return None
    df = interviews[interviews.get("event_type").fillna("") == "interview"].copy()
    if df.empty:
        return None
    counts = df.groupby(["event_year", "medium"]).size().rename("count").reset_index()
    if counts.empty:
        return None
    years = sorted(counts["event_year"].dropna().unique().tolist())
    # One subplot per year
    n = len(years)
    fig, axes = plt.subplots(nrows=1, ncols=n, figsize=(6*n, 5), squeeze=False)
    for idx, y in enumerate(years):
        ax = axes[0][idx]
        sub = counts[counts["event_year"] == y].sort_values("count", ascending=False)
        ax.barh(sub["medium"], sub["count"])
        ax.set_title(f"Interviews by Medium - {y}")
        ax.set_xlabel("Count")
        ax.invert_yaxis()
        for i, v in enumerate(sub["count"].tolist()):
            ax.text(v + 0.2, i, str(int(v)), va="center")
    plt.tight_layout()
    out = charts / "interviews_by_medium_year.png"
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_cumulative_comparison_applications(charts: Path, applications: pd.DataFrame) -> Optional[Path]:
    if applications.empty:
        return None
    plt.figure(figsize=(12, 5))
    any_data = False
    for year in (2022, 2025):
        daily = daily_counts(applications["applied_date"], year)
        if daily.empty:
            continue
        any_data = True
        cum = daily.cumsum()
        plt.plot(cum.index.strftime("%Y-%m-%d"), cum.values, label=f"Applications {year}")
    if not any_data:
        plt.close()
        return None
    plt.title("Cumulative Applications: 2022 vs 2025")
    plt.xlabel("Date")
    plt.ylabel("Cumulative count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = charts / "cumulative_applications_2022_vs_2025.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_manual_vs_ai_assisted(charts: Path, applications: pd.DataFrame) -> Optional[Path]:
    # Assume 2022 manual, 2025 AI-assisted per user
    if applications.empty:
        return None
    manual = int((applications.get("year") == 2022).sum())
    ai = int((applications.get("year") == 2025).sum())
    import numpy as np
    x = np.arange(2)
    plt.figure(figsize=(6, 5))
    plt.bar(x[0], manual, color="tab:gray", label="Manual (2022)")
    plt.bar(x[1], ai, color="tab:purple", label="AI-assisted (2025)")
    plt.xticks(x, ["Manual", "AI-assisted"]) 
    for i, v in enumerate([manual, ai]):
        plt.text(i, v + max(1, v*0.01), str(v), ha="center", va="bottom")
    plt.ylabel("Applications")
    plt.title("Manual vs AI-assisted Applications")
    plt.legend()
    out = charts / "manual_vs_ai_assisted.png"
    plt.tight_layout(); plt.savefig(out, dpi=150); plt.close()
    return out


def plot_cumulative_comparison_events(charts: Path, interviews: pd.DataFrame) -> Optional[Path]:
    if interviews.empty:
        return None
    plt.figure(figsize=(12, 5))
    any_data = False
    for year in (2022, 2025):
        daily_all = daily_counts(interviews["event_datetime"], year)
        if daily_all.empty:
            continue
        any_data = True
        cum_all = daily_all.cumsum()
        plt.plot(cum_all.index.strftime("%Y-%m-%d"), cum_all.values, label=f"Total events {year}")
    if not any_data:
        plt.close()
        return None
    plt.title("Cumulative Events (Interviews + Outreach): 2022 vs 2025")
    plt.xlabel("Date")
    plt.ylabel("Cumulative count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = charts / "cumulative_events_2022_vs_2025.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_cumulative_apps_vs_interviews(charts: Path, interviews: pd.DataFrame, applications: pd.DataFrame, year: int) -> Optional[Path]:
    if applications.empty and interviews.empty:
        return None
    daily_apps = daily_counts(applications["applied_date"], year) if not applications.empty else pd.Series(dtype=int)
    daily_ints = daily_counts(
        interviews[interviews.get("event_type").fillna("") == "interview"]["event_datetime"], year
    ) if not interviews.empty else pd.Series(dtype=int)
    if daily_apps.empty and daily_ints.empty:
        return None
    # Align to same full-year index
    full = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")
    daily_apps = daily_apps.reindex(full, fill_value=0)
    daily_ints = daily_ints.reindex(full, fill_value=0)
    cum_apps = daily_apps.cumsum()
    cum_ints = daily_ints.cumsum()

    import matplotlib.dates as mdates
    plt.figure(figsize=(12, 5))
    plt.plot(cum_apps.index, cum_apps.values, label="Applications", color="tab:blue")
    plt.plot(cum_ints.index, cum_ints.values, label="Interviews", color="tab:green")
    plt.title(f"Cumulative Applications vs Interviews - {year}")
    plt.xlabel("Date")
    plt.ylabel("Cumulative count")
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = charts / f"cumulative_apps_vs_interviews_{year}.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_cumulative_apps_vs_inbound_role(charts: Path, interviews: pd.DataFrame, applications: pd.DataFrame, year: int) -> Optional[Path]:
    if applications.empty and interviews.empty:
        return None
    # Applications daily cumulative
    daily_apps = daily_counts(applications["applied_date"], year) if not applications.empty else pd.Series(dtype=int)
    # Inbound role contacts: outreach + inbound + role-related
    df = interviews.copy() if not interviews.empty else pd.DataFrame()
    if df.empty:
        return None
    df = df[(df.get("event_year") == year) & (df.get("event_type").fillna("") == "outreach")]
    if "direction" in df.columns:
        df = df[df["direction"].fillna("").str.lower() == "inbound"]
    if df.empty:
        return None
    # role-related: role column present or notes contain role-ish words
    def _role_related(row) -> bool:
        r = str(row.get("role") or "").strip()
        if r:
            return True
        n = str(row.get("notes") or "").lower()
        for kw in ("role","position","opening","opportunity","hiring","recruit","product","engineer","developer","data","ml","manager","designer"):
            if kw in n:
                return True
        return False
    df = df[df.apply(_role_related, axis=1)]
    daily_inbound_role = pd.Series(dtype=int)
    if not df.empty:
        s = df["event_datetime"].dropna().dt.floor("D")
        if not s.empty:
            daily_inbound_role = (
                s.value_counts().rename_axis("date").sort_index().rename("count").to_frame()["count"]
            )
    if daily_apps.empty and daily_inbound_role.empty:
        return None
    full = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")
    daily_apps = daily_apps.reindex(full, fill_value=0)
    daily_inbound_role = daily_inbound_role.reindex(full, fill_value=0)
    cum_apps = daily_apps.cumsum()
    cum_inbound_role = daily_inbound_role.cumsum()

    import matplotlib.dates as mdates
    plt.figure(figsize=(12, 5))
    plt.plot(cum_apps.index, cum_apps.values, label="Applications", color="tab:blue")
    plt.plot(cum_inbound_role.index, cum_inbound_role.values, label="Inbound role contacts", color="tab:red")
    plt.title(f"Cumulative Applications vs Inbound Role Contacts - {year}")
    plt.xlabel("Date")
    plt.ylabel("Cumulative count")
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = charts / f"cumulative_apps_vs_inbound_role_{year}.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def plot_cumulative_apps_with_inbound_outreach_spikes(charts: Path, interviews: pd.DataFrame, applications: pd.DataFrame, year: int) -> Optional[Path]:
    if applications.empty or interviews.empty:
        return None
    # Cumulative applications per day
    daily_apps = daily_counts(applications["applied_date"], year)
    if daily_apps.empty:
        return None
    cum_apps = daily_apps.cumsum()

    # Inbound outreach spikes (0/1 per day)
    inbound = interviews[(interviews.get("event_year") == year) & (interviews.get("event_type").fillna("") == "outreach")]
    if "direction" in inbound.columns:
        inbound = inbound[inbound["direction"].fillna("").str.lower() == "inbound"]
    daily_inbound = pd.Series(dtype=int)
    if not inbound.empty:
        s = inbound["event_datetime"].dropna().dt.floor("D")
        if not s.empty:
            daily_inbound = (
                s.value_counts().rename_axis("date").sort_index().rename("count").to_frame()["count"]
            )
            full = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")
            daily_inbound = daily_inbound.reindex(full, fill_value=0)
    # Convert to binary spikes
    spikes = (daily_inbound > 0).astype(int) if not daily_inbound.empty else pd.Series(0, index=cum_apps.index)
    # Ensure aligned index
    spikes = spikes.reindex(cum_apps.index, fill_value=0)

    import matplotlib.dates as mdates
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(cum_apps.index, cum_apps.values, color="tab:blue", label="Cumulative applications")
    ax1.set_ylabel("Cumulative applications", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xlabel("Date")
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    # Draw spikes as markers at y=1 on days with inbound outreach
    spike_days = spikes.index[spikes.values == 1]
    if len(spike_days) > 0:
        ax2.scatter(spike_days, [1] * len(spike_days), marker="|", s=200, color="tab:orange", label="Inbound outreach")
    ax2.set_ylim(0, 1.05)
    ax2.set_ylabel("Inbound outreach spikes (0/1)", color="tab:orange")
    ax2.tick_params(axis="y", labelcolor="tab:orange")

    # Build combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title(f"Cumulative Applications with Inbound Outreach Spikes - {year}")
    out = charts / f"cumulative_apps_with_inbound_outreach_spikes_{year}.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Plot comparative charts for applications and interviews (2022 vs 2025)")
    ap.add_argument("--artifacts-root", default="artifacts/operations", help="Artifacts root")
    ap.add_argument("--op-dir", default=None, help="Specific operation dir to read from")
    ap.add_argument("--interviews-xlsx", default=None, help="Path to interviews_dataset.xlsx")
    ap.add_argument("--applications-xlsx", default=None, help="Path to applications_dataset.xlsx")
    ap.add_argument("--periods-config", default="config/periods.json", help="Optional JSON config for manual periods")
    args = ap.parse_args()

    artifacts_root = Path(args.artifacts_root)
    op_dir = Path(args.op_dir) if args.op_dir else find_latest_op(artifacts_root)
    if not op_dir or not op_dir.exists():
        print("No operation directory found.")
        return

    interviews_xlsx = Path(args.interviews_xlsx) if args.interviews_xlsx else None
    applications_xlsx = Path(args.applications_xlsx) if args.applications_xlsx else None
    interviews, applications = load_datasets(op_dir, interviews_xlsx, applications_xlsx)
    manual_periods = load_manual_periods(args.periods_config)
    charts_dir = ensure_out_dir(op_dir)

    generated = {}
    for y in (2022, 2025):
        p = plot_apps_vs_interviews_monthly(charts_dir, interviews, applications, y)
        if p:
            generated[f"apps_vs_interviews_monthly_{y}"] = str(p)
        q = plot_apps_interviews_outreach_monthly(charts_dir, interviews, applications, y)
        if q:
            generated[f"apps_interviews_outreach_monthly_{y}"] = str(q)
        r = plot_cumulative_apps_with_inbound_outreach_spikes(charts_dir, interviews, applications, y)
        if r:
            generated[f"cumulative_apps_with_inbound_outreach_spikes_{y}"] = str(r)
        s = plot_cumulative_apps_vs_inbound_role(charts_dir, interviews, applications, y)
        if s:
            generated[f"cumulative_apps_vs_inbound_role_{y}"] = str(s)
        # Per-period charts when defined
        periods = manual_periods.get(str(y)) or []
        for idx, period in enumerate(periods, start=1):
            start = pd.to_datetime(period.get("start_date"), errors="coerce")
            end = pd.to_datetime(period.get("end_date"), errors="coerce")
            if pd.isna(start) or pd.isna(end):
                continue
            # Filter data to window and reuse cumulative apps vs inbound role function
            apps_win = applications[(applications["applied_date"] >= start) & (applications["applied_date"] <= end)].copy()
            iv_win = interviews[(interviews["event_datetime"] >= start) & (interviews["event_datetime"] <= end)].copy()
            # Build quick plot
            daily_apps = apps_win["applied_date"].dropna().dt.floor("D").value_counts().rename_axis("date").sort_index()
            inbound = iv_win[iv_win.get("event_type").fillna("") == "outreach"]
            if "direction" in inbound.columns:
                inbound = inbound[inbound["direction"].fillna("").str.lower() == "inbound"]
            def _role_related(row) -> bool:
                rtxt = str(row.get("role") or "").strip()
                if rtxt:
                    return True
                n = str(row.get("notes") or "").lower()
                for kw in ("role","position","opening","opportunity","hiring","recruit","product","engineer","developer","data","ml","manager","designer"):
                    if kw in n:
                        return True
                return False
            inbound_role = inbound[inbound.apply(_role_related, axis=1)] if not inbound.empty else inbound
            daily_ir = inbound_role["event_datetime"].dropna().dt.floor("D").value_counts().rename_axis("date").sort_index() if not inbound_role.empty else pd.Series(dtype=int)
            # build full index
            full = pd.date_range(start=start.floor("D"), end=end.floor("D"), freq="D")
            daily_apps = daily_apps.reindex(full, fill_value=0)
            daily_ir = daily_ir.reindex(full, fill_value=0)
            cum_apps = daily_apps.cumsum()
            cum_ir = daily_ir.cumsum()
            import matplotlib.dates as mdates
            plt.figure(figsize=(12, 5))
            plt.plot(cum_apps.index, cum_apps.values, label="Applications", color="tab:blue")
            plt.plot(cum_ir.index, cum_ir.values, label="Inbound role contacts", color="tab:red")
            title = period.get("name") or f"Period {idx}"
            plt.title(f"{title} ({start.date()} to {end.date()})")
            plt.xlabel("Date"); plt.ylabel("Cumulative count")
            ax = plt.gca(); ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
            plt.xticks(rotation=45, ha="right"); plt.grid(True, alpha=0.3); plt.legend()
            outp = charts_dir / f"period_{y}_{idx}_cumulative_apps_vs_inbound_role.png"
            plt.tight_layout(); plt.savefig(outp, dpi=150); plt.close()
            generated[f"period_{y}_{idx}_cumulative_apps_vs_inbound_role"] = str(outp)
    p = plot_yearly_grouped(charts_dir, interviews, applications)
    if p:
        generated["apps_vs_interviews_by_year"] = str(p)
    p = plot_events_by_type_year(charts_dir, interviews)
    if p:
        generated["events_by_type_by_year"] = str(p)
    p = plot_outreach_direction_by_year(charts_dir, interviews)
    if p:
        generated["outreach_direction_by_year"] = str(p)
    p = plot_interviews_by_medium_year(charts_dir, interviews)
    if p:
        generated["interviews_by_medium_year"] = str(p)
    p = plot_cumulative_comparison_applications(charts_dir, applications)
    if p:
        generated["cumulative_applications_2022_vs_2025"] = str(p)
    p = plot_cumulative_comparison_events(charts_dir, interviews)
    if p:
        generated["cumulative_events_2022_vs_2025"] = str(p)
    p = plot_manual_vs_ai_assisted(charts_dir, applications)
    if p:
        generated["manual_vs_ai_assisted"] = str(p)
    for y in (2022, 2025):
        p = plot_cumulative_apps_vs_interviews(charts_dir, interviews, applications, y)
        if p:
            generated[f"cumulative_apps_vs_interviews_{y}"] = str(p)

    # Small manifest
    manifest = {
        "operation_id": op_dir.name,
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "charts": generated,
    }
    (charts_dir / "charts_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()


