import pandas as pd
import pytest
from econlens.transform import clean_observations, quality_report

# Synthetic fixtures used for unit tests ONLY; never passed off as source data.
def fixture_data():
    return pd.DataFrame([
        {'country_code':'IND','country':'India','indicator_code':'FP.CPI.TOTL.ZG',
         'indicator':'Consumer price inflation (annual %)','year':'2023','value':None,'source_url':'test'},
        {'country_code':'IND','country':'India','indicator_code':'FP.CPI.TOTL.ZG',
         'indicator':'Consumer price inflation (annual %)','year':'2022','value':5.0,'source_url':'test'},
    ])

def test_clean_preserves_missing_and_casts_year():
    cleaned = clean_observations(fixture_data())
    assert cleaned.year.dtype.kind in 'iu'
    assert cleaned.value.isna().sum() == 1
    assert cleaned.year.tolist() == [2022, 2023]

def test_duplicate_rejected():
    df = fixture_data()
    with pytest.raises(ValueError, match='Duplicate'):
        clean_observations(pd.concat([df, df.iloc[[0]]], ignore_index=True))

def test_quality_report_uses_latest_non_null_year():
    report = quality_report(clean_observations(fixture_data()))
    assert report.iloc[0]['latest_observation_year'] == 2022
    assert report.iloc[0]['missing'] == 1
