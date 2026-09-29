"""Fetch public World Bank WDI observations with explicit error handling."""
import time
import requests
import pandas as pd
from .config import API_ROOT, COUNTRIES, INDICATORS, START_YEAR, END_YEAR


def fetch_indicator(indicator, session=None, start=START_YEAR, end=END_YEAR):
    """Return a DataFrame of observations for one WDI indicator (including nulls)."""
    if indicator not in INDICATORS:
        raise ValueError(f'Unknown indicator: {indicator}')
    session = session or requests.Session()
    url = f"{API_ROOT}/country/{';'.join(COUNTRIES)}/indicator/{indicator}"
    params = {'format': 'json', 'per_page': 1000, 'date': f'{start}:{end}', 'page': 1}
    records = []
    while True:
        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[0], dict):
            raise ValueError(f'Unexpected World Bank response for {indicator}: {payload}')
        metadata, entries = payload
        if not isinstance(entries, list):
            raise ValueError(f'No observations returned for {indicator}: {payload}')
        for item in entries:
            iso3 = item.get('countryiso3code')
            if iso3 not in COUNTRIES:  # Never include regional aggregates.
                continue
            records.append({
                'country_code': iso3,
                'country': COUNTRIES[iso3],
                'indicator_code': indicator,
                'indicator': INDICATORS[indicator],
                'year': item.get('date'),
                'value': item.get('value'),
                'source_url': f'https://data.worldbank.org/indicator/{indicator}',
            })
        if params['page'] >= int(metadata.get('pages', 1)):
            break
        params['page'] += 1
        time.sleep(0.15)
    if not records:
        raise ValueError(f'No matching country records returned for {indicator}')
    return pd.DataFrame.from_records(records)


def fetch_all(session=None, start=START_YEAR, end=END_YEAR):
    """Fetch all configured indicators; never replace real source data with demo data."""
    return pd.concat(
        [fetch_indicator(code, session=session, start=start, end=end) for code in INDICATORS],
        ignore_index=True,
    )
