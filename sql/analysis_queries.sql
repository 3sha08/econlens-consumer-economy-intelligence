-- Inspect series coverage before interpreting comparisons.
SELECT country, indicator, COUNT(value) AS published_observations,
       MAX(CASE WHEN value IS NOT NULL THEN year END) AS latest_year
FROM economic_observations
GROUP BY country, indicator
ORDER BY country, indicator;

-- Year-aligned inflation vs household consumption growth, for exploratory analysis.
-- Missing values remain NULL and are excluded only for this paired comparison.
SELECT a.country, a.year, a.value AS inflation_pct, b.value AS consumption_growth_pct
FROM economic_observations AS a
JOIN economic_observations AS b
  ON a.country_code = b.country_code AND a.year = b.year
WHERE a.indicator_code = 'FP.CPI.TOTL.ZG'
  AND b.indicator_code = 'NE.CON.PRVT.KD.ZG'
  AND a.value IS NOT NULL AND b.value IS NOT NULL
ORDER BY a.country, a.year;
