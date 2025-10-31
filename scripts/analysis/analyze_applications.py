import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

import pandas as pd


@dataclass
class PeriodResult:
    period_index: int
    start_date: datetime
    end_date: datetime
    num_days: int
    num_applications: int
    applications_per_day: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze LinkedIn applications from Excel export")
    parser.add_argument("input_path", type=str, help="Path to Applications_Monolith.xlsx (or similar)")
    parser.add_argument("--gap-days", type=int, default=7, help="Gap (days) separating distinct application periods")
    parser.add_argument("--output-root", type=str, default="artifacts/operations", help="Root artifacts directory")
    parser.add_argument(
        "--focus-years",
        type=int,
        nargs="*",
        default=None,
        help="Years to focus on for comparative visuals (e.g., --focus-years 2022 2025)")
    return parser.parse_args()


def ensure_operation_dirs(output_root: Path) -> Path:
    operation_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f")
    op_dir = output_root / operation_id
    (op_dir / "input").mkdir(parents=True, exist_ok=True)
    (op_dir / "processing").mkdir(parents=True, exist_ok=True)
    (op_dir / "output").mkdir(parents=True, exist_ok=True)
    return op_dir


def detect_date_column(df: pd.DataFrame) -> Optional[str]:
    candidates = [
        "Applied On",
        "AppliedOn",
        "Application Date",
        "Applied Date",
        "Date",
        "Created At",
        "created_at",
        "timestamp",
    ]
    lower_map = {c.lower(): c for c in df.columns}
    for name in candidates:
        if name in df.columns:
            return name
        if name.lower() in lower_map:
            return lower_map[name.lower()]
    # Try first datetime-like column
    for col in df.columns:
        try:
            pd.to_datetime(df[col])
            return col
        except Exception:
            continue
    return None


def detect_company_column(df: pd.DataFrame) -> Optional[str]:
    candidates = [
        "Company",
        "Company Name",
        "company",
        "Organization",
        "Employer",
    ]
    lower_map = {c.lower(): c for c in df.columns}
    for name in candidates:
        if name in df.columns:
            return name
        if name.lower() in lower_map:
            return lower_map[name.lower()]
    return None


def segment_periods(dates: List[datetime], gap_days: int) -> List[List[datetime]]:
    if not dates:
        return []
    dates_sorted = sorted(dates)
    periods: List[List[datetime]] = [[dates_sorted[0]]]
    for d in dates_sorted[1:]:
        if (d - periods[-1][-1]).days > gap_days:
            periods.append([d])
        else:
            periods[-1].append(d)
    return periods


def summarize_periods(periods: List[List[datetime]]) -> List[PeriodResult]:
    results: List[PeriodResult] = []
    for i, pdts in enumerate(periods, start=1):
        start = pdts[0]
        end = pdts[-1]
        num_days = max(1, (end - start).days + 1)
        num_apps = len(pdts)
        rate = num_apps / num_days
        results.append(PeriodResult(i, start, end, num_days, num_apps, rate))
    return results


def analyze(input_path: Path, op_dir: Path, gap_days: int) -> Dict[str, Any]:
    df = pd.read_excel(input_path)

    date_col = detect_date_column(df)
    company_col = detect_company_column(df)

    if not date_col:
        raise ValueError("Could not detect a date column. Please ensure your export includes an application date column.")

    df["__date__"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["__date__"]).copy()
    df.sort_values("__date__", inplace=True)

    # Overall metrics
    total_apps = len(df)
    if total_apps == 0:
        periods: List[List[datetime]] = []
    else:
        periods = segment_periods(df["__date__"].tolist(), gap_days)

    period_summaries = summarize_periods(periods)

    # Applications per month/week
    monthly = (
        df.set_index("__date__").assign(count=1)["count"].resample("MS").sum().rename("applications")
    )
    weekly = (
        df.set_index("__date__").assign(count=1)["count"].resample("W-MON").sum().rename("applications")
    )

    # Company segmentation
    top_companies = None
    if company_col and company_col in df.columns:
        vc = df[company_col].fillna("(unknown)").value_counts()
        top_companies = vc.reset_index()
        # Force stable column names regardless of pandas behavior
        top_companies.columns = ["company", "applications"]

    # Recruiter vs Employer heuristic split
    recruiters_df = None
    employers_df = None
    if top_companies is not None and not top_companies.empty:
        recruiter_keywords = [
            "recruit", "talent", "agency", "partners", "consult", "headhunt",
            "search", "staff", "placement", "hiring", "people", "solutions"
        ]
        def is_recruiter(name: str) -> bool:
            n = (name or "").lower()
            return any(kw in n for kw in recruiter_keywords)
        tmp = top_companies.copy()
        tmp["type"] = tmp["company"].apply(lambda x: "recruiter" if is_recruiter(x) else "employer")
        recruiters_df = tmp[tmp["type"] == "recruiter"].nlargest(20, "applications")
        employers_df = tmp[tmp["type"] == "employer"].nlargest(20, "applications")

    # Yearly-focused features
    df["year"] = df["__date__"].dt.year
    df["month"] = df["__date__"].dt.month
    df["month_name"] = df["__date__"].dt.strftime("%b")
    df["weekday"] = df["__date__"].dt.day_name()

    yearly = df.groupby("year").size().rename("applications").astype(int)
    year_month = (
        df.groupby(["year", "month"]).size().unstack(fill_value=0).sort_index()
    )
    weekday_counts = df["weekday"].value_counts()

    # Save tabular outputs
    output_dir = op_dir / "output"
    monthly.to_csv(output_dir / "applications_by_month.csv", header=True)
    weekly.to_csv(output_dir / "applications_by_week.csv", header=True)
    if top_companies is not None:
        top_companies.to_csv(output_dir / "applications_by_company.csv", index=False)
        if recruiters_df is not None:
            recruiters_df.to_csv(output_dir / "top_recruiters.csv", index=False)
        if employers_df is not None:
            employers_df.to_csv(output_dir / "top_employers.csv", index=False)

    yearly.to_csv(output_dir / "applications_by_year.csv", header=True)
    year_month.to_csv(output_dir / "applications_by_year_month.csv")
    weekday_counts.to_csv(output_dir / "applications_by_weekday.csv", header=True)

    # Periods CSV
    if period_summaries:
        periods_df = pd.DataFrame([
            {
                "period_index": p.period_index,
                "start_date": p.start_date.date().isoformat(),
                "end_date": p.end_date.date().isoformat(),
                "num_days": p.num_days,
                "num_applications": p.num_applications,
                "applications_per_day": round(p.applications_per_day, 4),
            }
            for p in period_summaries
        ])
        periods_df.to_csv(output_dir / "application_periods.csv", index=False)

    # Charts
    charts_dir = output_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.set_theme(style="whitegrid")

        # By year (bar)
        plt.figure(figsize=(10, 5))
        yearly.plot(kind="bar", color="#4C78A8")
        plt.title("Applications by Year")
        plt.ylabel("Applications")
        plt.xlabel("Year")
        plt.tight_layout()
        by_year_path = charts_dir / "applications_by_year_bar.png"
        plt.savefig(by_year_path, dpi=150)
        plt.close()

        # Monthly timeline (line)
        plt.figure(figsize=(12, 4))
        monthly.plot(color="#F58518")
        plt.title("Applications by Month (Timeline)")
        plt.ylabel("Applications")
        plt.xlabel("")
        plt.tight_layout()
        by_month_line_path = charts_dir / "applications_by_month_line.png"
        plt.savefig(by_month_line_path, dpi=150)
        plt.close()

        # Year-Month heatmap
        # Ensure 1..12 columns
        full_cols = list(range(1, 13))
        ym_plot = year_month.reindex(columns=full_cols, fill_value=0)
        plt.figure(figsize=(12, max(3, 0.6 * len(ym_plot.index))))
        sns.heatmap(ym_plot, annot=True, fmt="d", cmap="Blues")
        plt.title("Applications Heatmap (Year vs Month)")
        plt.ylabel("Year")
        plt.xlabel("Month")
        plt.tight_layout()
        heatmap_path = charts_dir / "year_month_heatmap.png"
        plt.savefig(heatmap_path, dpi=150)
        plt.close()

        # Weekly timeline (line)
        plt.figure(figsize=(12, 4))
        weekly.plot(color="#54A24B")
        plt.title("Applications by Week (Mon-start)")
        plt.ylabel("Applications")
        plt.xlabel("")
        plt.tight_layout()
        by_week_line_path = charts_dir / "applications_by_week_line.png"
        plt.savefig(by_week_line_path, dpi=150)
        plt.close()

        # Top companies (barh)
        top_companies_path = None
        if top_companies is not None and not top_companies.empty:
            top_n = top_companies.head(20).copy()
            plt.figure(figsize=(10, max(4, 0.35 * len(top_n))))
            sns.barplot(data=top_n, x="applications", y="company", color="#E45756")
            plt.title("Top Companies by Applications (Top 20)")
            plt.xlabel("Applications")
            plt.ylabel("Company")
            plt.tight_layout()
            top_companies_path = charts_dir / "top_companies_bar.png"
            plt.savefig(top_companies_path, dpi=150)
            plt.close()

        # Weekday distribution (bar)
        plt.figure(figsize=(8, 4))
        order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_plot = weekday_counts.reindex(order).fillna(0)
        sns.barplot(x=weekday_plot.index, y=weekday_plot.values, color="#72B7B2")
        plt.title("Applications by Weekday")
        plt.ylabel("Applications")
        plt.xlabel("")
        plt.xticks(rotation=30)
        plt.tight_layout()
        weekday_path = charts_dir / "applications_by_weekday.png"
        plt.savefig(weekday_path, dpi=150)
        plt.close()

        chart_paths = {
            "by_year_bar": str(by_year_path),
            "by_month_line": str(by_month_line_path),
            "year_month_heatmap": str(heatmap_path),
            "by_week_line": str(by_week_line_path),
            "top_companies_bar": str(top_companies_path) if top_companies is not None else None,
            "weekday_bar": str(weekday_path),
        }
    except Exception as e:
        chart_paths = {"error": f"chart_generation_failed: {e}"}

    # Focus-year comparative visuals and report section
    focus_years = None
    try:
        # read from CLI via environment captured in main; fallback to None
        # We'll parse again in main and write into a small file for access here if needed
        pass
    except Exception:
        pass

    compare_paths: Dict[str, Optional[str]] = {}

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns

        # If the user passed focus years via a sentinel file created by main()
        fy_file = op_dir / "processing" / "focus_years.txt"
        focus_years = None
        if fy_file.exists():
            try:
                content = fy_file.read_text(encoding="utf-8").strip()
                if content:
                    focus_years = [int(x) for x in content.split()] if content else None
            except Exception:
                focus_years = None

        if focus_years and len(focus_years) >= 2:
            fy = [y for y in focus_years if y in yearly.index]
            if len(fy) >= 2:
                y1, y2 = fy[:2]

                # Monthly series per year (bar side-by-side)
                m1 = df[df["year"] == y1].set_index("__date__").assign(count=1)["count"].resample("MS").sum()
                m2 = df[df["year"] == y2].set_index("__date__").assign(count=1)["count"].resample("MS").sum()
                # align months Jan..Dec for both
                idx = pd.date_range(f"{min(y1,y2)}-01-01", f"{max(y1,y2)}-12-01", freq="MS")
                m1a = m1.reindex(pd.date_range(f"{y1}-01-01", f"{y1}-12-01", freq="MS"), fill_value=0)
                m2a = m2.reindex(pd.date_range(f"{y2}-01-01", f"{y2}-12-01", freq="MS"), fill_value=0)

                # Overlay line chart
                plt.figure(figsize=(12, 4))
                m1a.index = m1a.index.strftime("%b")
                m2a.index = m2a.index.strftime("%b")
                plt.plot(m1a.index, m1a.values, marker="o", label=str(y1))
                plt.plot(m2a.index, m2a.values, marker="o", label=str(y2))
                plt.title(f"Monthly Applications: {y1} vs {y2}")
                plt.ylabel("Applications")
                plt.legend()
                plt.tight_layout()
                cmp_month_line = charts_dir / f"compare_{y1}_vs_{y2}_monthly.png"
                plt.savefig(cmp_month_line, dpi=150)
                plt.close()

                # Cumulative curves per year
                c1 = m1a.cumsum()
                c2 = m2a.cumsum()
                plt.figure(figsize=(12, 4))
                plt.plot(c1.index, c1.values, marker="o", label=f"{y1} cumulative")
                plt.plot(c2.index, c2.values, marker="o", label=f"{y2} cumulative")
                plt.title(f"Cumulative Applications: {y1} vs {y2}")
                plt.ylabel("Cumulative Applications")
                plt.legend()
                plt.tight_layout()
                cmp_cum_line = charts_dir / f"compare_{y1}_vs_{y2}_cumulative.png"
                plt.savefig(cmp_cum_line, dpi=150)
                plt.close()

                # Weekday per year (normalized)
                order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                wd1 = df[df["year"] == y1]["weekday"].value_counts().reindex(order).fillna(0)
                wd2 = df[df["year"] == y2]["weekday"].value_counts().reindex(order).fillna(0)
                wd = pd.DataFrame({str(y1): wd1, str(y2): wd2})
                plt.figure(figsize=(10, 4))
                wd.plot(kind="bar", rot=30)
                plt.title(f"Applications by Weekday: {y1} vs {y2}")
                plt.ylabel("Applications")
                plt.xlabel("")
                plt.tight_layout()
                cmp_weekday_bar = charts_dir / f"compare_{y1}_vs_{y2}_weekday.png"
                plt.savefig(cmp_weekday_bar, dpi=150)
                plt.close()

                # Top companies per year (two separate plots)
                top_companies_path_y1 = None
                top_companies_path_y2 = None
                if company_col and company_col in df.columns:
                    t1 = (
                        df[df["year"] == y1][company_col]
                        .fillna("(unknown)")
                        .value_counts()
                        .head(20)
                        .reset_index()
                    )
                    t1.columns = ["company", "applications"]
                    plt.figure(figsize=(10, max(4, 0.35 * len(t1))))
                    sns.barplot(data=t1, x="applications", y="company", color="#E45756")
                    plt.title(f"Top Companies {y1}")
                    plt.xlabel("Applications")
                    plt.ylabel("Company")
                    plt.tight_layout()
                    top_companies_path_y1 = charts_dir / f"top_companies_{y1}.png"
                    plt.savefig(top_companies_path_y1, dpi=150)
                    plt.close()

                    t2 = (
                        df[df["year"] == y2][company_col]
                        .fillna("(unknown)")
                        .value_counts()
                        .head(20)
                        .reset_index()
                    )
                    t2.columns = ["company", "applications"]
                    plt.figure(figsize=(10, max(4, 0.35 * len(t2))))
                    sns.barplot(data=t2, x="applications", y="company", color="#4C78A8")
                    plt.title(f"Top Companies {y2}")
                    plt.xlabel("Applications")
                    plt.ylabel("Company")
                    plt.tight_layout()
                    top_companies_path_y2 = charts_dir / f"top_companies_{y2}.png"
                    plt.savefig(top_companies_path_y2, dpi=150)
                    plt.close()

                compare_paths = {
                    "focus_years": [y1, y2],
                    "monthly_overlay": str(cmp_month_line),
                    "cumulative_overlay": str(cmp_cum_line),
                    "weekday_comparison": str(cmp_weekday_bar),
                    "top_companies_y1": str(top_companies_path_y1) if company_col else None,
                    "top_companies_y2": str(top_companies_path_y2) if company_col else None,
                }
    except Exception as e:
        # Optional feature; don't fail the run
        compare_paths = {"error": f"focus_year_comparison_failed: {e}"}

    # Narrative report (Markdown)
    report_md = output_dir / "report.md"

    yoy = yearly.pct_change().fillna(0)
    best_year = yearly.idxmax() if not yearly.empty else None
    best_year_val = int(yearly.max()) if not yearly.empty else 0

    key_periods = sorted(
        period_summaries,
        key=lambda p: p.applications_per_day,
        reverse=True,
    )[:5]

    with open(report_md, "w", encoding="utf-8") as f:
        f.write("## Applications Analysis (Yearly Focus)\n\n")
        f.write(f"- Total applications: {int(total_apps)}\n")
        if not yearly.empty:
            f.write(f"- Peak year: {best_year} with {best_year_val} applications\n")
        f.write(f"- Distinct application periods: {len(period_summaries)} (gap={gap_days} days)\n\n")

        f.write("### Year-over-Year\n")
        if not yearly.empty:
            for y in yearly.index:
                change = yoy.get(y, 0.0)
                f.write(f"- {y}: {int(yearly.loc[y])} apps (YoY: {change:+.1%})\n")
        f.write("\n")

        f.write("### Strongest Periods (by applications/day)\n")
        for p in key_periods:
            f.write(
                f"- {p.start_date.date()} → {p.end_date.date()}: {p.num_applications} apps over {p.num_days} days "
                f"({p.applications_per_day:.2f}/day)\n"
            )
        f.write("\n")

        f.write("### Company Segmentation\n")
        if top_companies is not None and not top_companies.empty:
            top_row = top_companies.head(10)
            for _, row in top_row.iterrows():
                f.write(f"- {row['company']}: {int(row['applications'])}\n")
        else:
            f.write("- Not available\n")
        f.write("\n")

        f.write("### Visuals\n")
        for name, path in chart_paths.items():
            if path:
                f.write(f"- {name}: {path}\n")
        f.write("\n")

        # Focus-year comparison section
        if compare_paths and "focus_years" in compare_paths:
            y1, y2 = compare_paths["focus_years"]
            f.write(f"### Focus-Year Comparison: {y1} vs {y2}\n")
            f.write("- monthly_overlay: " + str(compare_paths.get("monthly_overlay")) + "\n")
            f.write("- cumulative_overlay: " + str(compare_paths.get("cumulative_overlay")) + "\n")
            f.write("- weekday_comparison: " + str(compare_paths.get("weekday_comparison")) + "\n")
            if compare_paths.get("top_companies_y1"):
                f.write("- top_companies_y1: " + str(compare_paths.get("top_companies_y1")) + "\n")
            if compare_paths.get("top_companies_y2"):
                f.write("- top_companies_y2: " + str(compare_paths.get("top_companies_y2")) + "\n")
            f.write("\n")

    # Summary JSON
    summary = {
        "status": "success",
        "message": "Applications analysis completed",
        "input_file": str(input_path),
        "gap_days": gap_days,
        "total_applications": int(total_apps),
        "date_column": date_col,
        "company_column": company_col,
        "periods": [
            {
                "period_index": p.period_index,
                "start_date": p.start_date.date().isoformat(),
                "end_date": p.end_date.date().isoformat(),
                "num_days": p.num_days,
                "num_applications": p.num_applications,
                "applications_per_day": round(p.applications_per_day, 4),
            }
            for p in period_summaries
        ],
        "artifacts": {
            "applications_by_month_csv": str(output_dir / "applications_by_month.csv"),
            "applications_by_week_csv": str(output_dir / "applications_by_week.csv"),
            "applications_by_company_csv": str(output_dir / "applications_by_company.csv") if top_companies is not None else None,
            "application_periods_csv": str(output_dir / "application_periods.csv") if period_summaries else None,
            "applications_by_year_csv": str(output_dir / "applications_by_year.csv"),
            "applications_by_year_month_csv": str(output_dir / "applications_by_year_month.csv"),
            "applications_by_weekday_csv": str(output_dir / "applications_by_weekday.csv"),
            "top_recruiters_csv": str(output_dir / "top_recruiters.csv") if recruiters_df is not None else None,
            "top_employers_csv": str(output_dir / "top_employers.csv") if employers_df is not None else None,
            "charts": chart_paths,
            "report_md": str(report_md),
            "focus_years": compare_paths,
        },
    }

    with open(op_dir / "output" / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Audit trail minimal
    audit = {
        "operation_id": op_dir.name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "excel-processing",
        "input_file": str(input_path),
        "output_dir": str(op_dir / "output"),
        "changes": [],
        "validation": {
            "status": "success",
            "notes": "Read-only analysis; no file mutations",
        },
        "approval_status": "not_required",
    }
    with open(op_dir / "audit.json", "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)

    return summary


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path)
    output_root = Path(args.output_root)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    op_dir = ensure_operation_dirs(output_root)

    # Write focus years sentinel if provided so analyze() can pick it up
    try:
        if args.focus_years:
            (op_dir / "processing").mkdir(parents=True, exist_ok=True)
            with open(op_dir / "processing" / "focus_years.txt", "w", encoding="utf-8") as f:
                f.write(" ".join(str(y) for y in args.focus_years))
    except Exception:
        pass

    # Copy input into artifacts/input for traceability
    try:
        # Avoid heavy copies for large files; just reference
        with open(op_dir / "input" / "README.txt", "w", encoding="utf-8") as f:
            f.write(f"Input referenced at: {input_path}\n")
    except Exception:
        pass

    summary = analyze(input_path, op_dir, args.gap_days)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()


