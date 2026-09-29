"""Persist historical snapshots locally in a SQLite relational database."""
from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path('data/processed/econlens.sqlite')

def save_to_sqlite(df, destination=DB_PATH):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(destination) as conn:
        df.to_sql('economic_observations', conn, if_exists='replace', index=False)
        conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS observation_key '
                     'ON economic_observations (country_code, indicator_code, year)')
    return destination


def read_from_sqlite(destination=DB_PATH):
    if not Path(destination).exists():
        raise FileNotFoundError('Database missing. First run: python -m econlens.pipeline')
    with sqlite3.connect(destination) as conn:
        return pd.read_sql_query('SELECT * FROM economic_observations', conn)
