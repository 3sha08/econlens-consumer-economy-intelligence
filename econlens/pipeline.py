"""Run end-to-end data ingestion; no demo values are silently substituted."""
from pathlib import Path
from .extract import fetch_all
from .transform import clean_observations, quality_report
from .storage import save_to_sqlite

def run():
    raw = fetch_all()
    processed = clean_observations(raw)
    Path('data/raw').mkdir(parents=True, exist_ok=True)
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    raw.to_csv('data/raw/world_bank_observations.csv', index=False)
    processed.to_csv('data/processed/economic_observations.csv', index=False)
    quality_report(processed).to_csv('data/processed/quality_report.csv', index=False)
    db_path = save_to_sqlite(processed)
    print(f'Loaded {len(processed)} rows ({processed.value.notna().sum()} non-null) into {db_path}')
    print('Year coverage per series: data/processed/quality_report.csv')

if __name__ == '__main__':
    run()
