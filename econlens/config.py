"""Project configuration and World Bank indicator metadata."""
from datetime import date

START_YEAR = 2015
END_YEAR = date.today().year
COUNTRIES = {'IND': 'India', 'SGP': 'Singapore', 'THA': 'Thailand', 'ARE': 'United Arab Emirates'}
INDICATORS = {
    'FP.CPI.TOTL.ZG': 'Consumer price inflation (annual %)',
    'NE.CON.PRVT.KD.ZG': 'Household & NPISH consumption growth (annual %)',
    'NY.GDP.MKTP.KD.ZG': 'GDP growth (annual %)',
}
API_ROOT = 'https://api.worldbank.org/v2'
