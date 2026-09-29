"""Type enforcement, missing-value handling, and data quality checks."""
import pandas as pd
from .config import COUNTRIES, INDICATORS

KEYS = ['country_code', 'indicator_code', 'year']
COLUMNS = ['country_code', 'country', 'indicator_code', 'indicator', 'year', 'value', 'source_url']


def clean_observations(raw):
    """Preserve missing source values as NaN; never fabricate observations."""
    missing_columns = set(COLUMNS) - set(raw.columns)
    if missing_columns:
        raise ValueError(f'Missing required columns: {sorted(missing_columns)}')
    df = raw[COLUMNS].copy()
    df['year'] = pd.to_numeric(df['year'], errors='raise').astype('int64')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    if not df['country_code'].isin(COUNTRIES).all():
        raise ValueError('Unexpected country code')
    if not df['indicator_code'].isin(INDICATORS).all():
        raise ValueError('Unexpected indicator code')
    if df.duplicated(KEYS).any():
        raise ValueError('Duplicate country/indicator/year observations')
    return df.sort_values(KEYS, kind='stable').reset_index(drop=True)


def quality_report(df):
    """Counts, missingness, and most recent non-null year by series."""
    grouped = df.groupby(['country', 'indicator'], sort=True)
    report = grouped.agg(rows=('value', 'size'), present=('value', 'count'),
                         missing=('value', lambda s: int(s.isna().sum()))).reset_index()
    latest = (df.loc[df['value'].notna()].groupby(['country', 'indicator'])['year']
              .max().rename('latest_observation_year').reset_index())
    return report.merge(latest, on=['country', 'indicator'], how='left')
