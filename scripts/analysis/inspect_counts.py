import json
from pathlib import Path
import pandas as pd

def main() -> None:
    ops = Path('artifacts/operations')
    latest = max([p for p in ops.iterdir() if p.is_dir() and p.name[:8].isdigit()], key=lambda p: p.name)
    merged_p = latest / 'output' / 'enriched' / 'merged_interview_events.xlsx'
    df = pd.read_excel(merged_p)
    df['event_date_parsed'] = pd.to_datetime(df.get('event_date'), errors='coerce')
    if 'event_year' not in df.columns:
        df['event_year'] = df['event_date_parsed'].dt.year
    by_year_date = df.dropna(subset=['event_date_parsed']).assign(y=df['event_date_parsed'].dt.year).groupby('y').size().to_dict()
    by_event_year = df.dropna(subset=['event_year']).assign(y=pd.to_numeric(df['event_year'], errors='coerce').astype('Int64')).dropna(subset=['y']).groupby('y').size().to_dict()
    print(json.dumps({
        'latest_op': latest.name,
        'total_rows': int(len(df)),
        'by_year_event_date': {str(int(k)): int(v) for k,v in by_year_date.items()},
        'by_event_year_fallback': {str(int(k)): int(v) for k,v in by_event_year.items()}
    }, indent=2))

if __name__ == '__main__':
    main()
