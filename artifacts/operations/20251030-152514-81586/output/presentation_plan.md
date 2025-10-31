## Presentation Plan: Applications Analysis (2022 vs 2025)

- Context: Distinguish pre- vs post-LLM application behavior using LinkedIn export.
- Data source: `Data Tests/Excel and Powerpoint Testing/Applications_Monolith.xlsx`
- Focus years: 2022 (pre-LLM) vs 2025 (post-LLM)
- Artifacts (latest analysis): `artifacts/operations/20251030-120018-339487/output/`

Design approach (per pptx skill)
- Fonts: Arial (web-safe), bold for headers, readable sizes.
- Palette: charcoal bg (#2C2C2C), off-white text (#F4F6F6), 2022 blue (#4C78A8), 2025 orange (#F58518), silver accents (#AAB7B8).
- Layouts: header bar + content; two-column for text+chart, full-bleed for key charts. Strong contrast and consistent margins.
- Visual details: minimal gridlines, oversized numbers when needed, consistent spacing, no stacked text over charts.

Slides
1) Title
   - Title: "Applications Analysis: 2022 vs 2025 (Pre vs Post LLM)"
   - Subtitle: "LinkedIn Applications – Volume, Tempo, and Patterns"

2) Objective & Data
   - Bullets: objectives, dataset, method (pandas resampling; 7-day period gap).

3) Yearly Volume Overview
   - Visual: applications_by_year_bar.png
   - Callout: Peak 2025 vs 2022 totals (507 vs 131 applications).

4) Timeline: Monthly Trend (All Years)
   - Visual: applications_by_month_line.png (context across years)

5) Heatmap: Year x Month
   - Visual: year_month_heatmap.png
   - Insight: 2022 concentrated Apr–May; 2025 sustained Mar–Jul.

6) Focus Overlay: 2022 vs 2025 Monthly
   - Visual: compare_2022_vs_2025_monthly.png
   - Message: 2025 starts earlier and remains consistently higher.

7) Focus Overlay: Cumulative Curve
   - Visual: compare_2022_vs_2025_cumulative.png
   - Message: 2025 cumulative pace outstrips 2022 month-over-month.

8) Weekday Distribution (Comparison)
   - Visual: compare_2022_vs_2025_weekday.png
   - Insight: Both skew to weekdays; 2025 dominates all days.

9) Top Companies 2022
   - Visual: top_companies_2022.png
   - Note any clusters (recruiters vs employers).

10) Top Companies 2025
    - Visual: top_companies_2025.png
    - Highlight spread vs 2022.

11) Application Periods (Bursts)
    - Visual: applications_by_week_line.png
    - Key stats (from application_periods.csv): 2025-03-19→2025-07-24 (3.72/day), 2022-04-22→2022-05-20 (3.36/day)

12) Rates & Capacity (Setup)
    - Bullets: 10-day sprint (~23), 4-week run (~90–105), 16–18 weeks (450+)

13) Next: Response/Interest Layer (Gmail)
    - Bullets: ingest replies; response/interview rates; time-to-first-response.

14) Data Quality & Cleaning
    - Bullets: date normalization; company normalization (to-do); recruiter labeling (to-do)

15) Summary & Takeaways
    - 2025 sustained higher intensity; clear pre/post LLM distinction; funnel pending email integration

Appendix: Tables
- applications_by_year.csv, applications_by_year_month.csv, applications_by_month.csv, applications_by_week.csv, applications_by_weekday.csv, applications_by_company.csv, application_periods.csv

PPTX skill workflow (POC)
- We’re using a direct builder (python-pptx) for now with a clean theme and strict margins (POC non-destructive writes under `artifacts/`).
- Optional: For pixel-perfect layouts, adopt the html2pptx flow (`pptx/scripts/html2pptx.js`) as a next step once Node deps are enabled.
