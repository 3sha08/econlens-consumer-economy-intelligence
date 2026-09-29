# EconLens — Consumer Economy Intelligence

A reproducible data visualisation portfolio project for studying annual inflation, household/NPISH consumption growth, and GDP growth across India, Singapore, Thailand, and the United Arab Emirates.


## Explore EconLens

- **Live Interactive Dashboard:** [Launch EconLens](https://econlens-consumer-economy-intelligence.streamlit.app/)
- **Published Economic Research Report:** [Read the Report](https://3sha08.github.io/econlens-consumer-economy-intelligence/)


### About the Project

EconLens is an independent economic intelligence platform combining Python, SQL, interactive data visualisation, and reproducible research reporting.

The project explores economic trends across India, Singapore, Thailand, and the UAE using publicly available World Bank indicators.

It demonstrates an end-to-end analytical workflow, from data extraction and validation to economic interpretation and automated reporting.


## Sources and integrity

- World Bank World Development Indicators, accessed through the public API v2 (no API key required).
- Series: `FP.CPI.TOTL.ZG`, `NE.CON.PRVT.KD.ZG`, `NY.GDP.MKTP.KD.ZG`.
- Years requested: 2015 through the calendar year when the pipeline runs. **Not all years will contain a published observation.**
- No Mastercard or consumer-level transaction data is used.
- Unit tests use deliberately synthetic fixtures; **the pipeline never substitutes mock data** for an unavailable live data source.


## Quick start (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m econlens.pipeline
python -m pytest -q
streamlit run app.py
```
On macOS/Linux, use `python3 -m venv .venv && source .venv/bin/activate` then the common commands above. The pipeline needs internet access. If the API is unavailable, it fails rather than inventing observations.


## Reproducible research report

Install the Quarto command-line application separately: https://quarto.org/docs/get-started/
Then run from the repo root:
```bash
quarto check jupyter
quarto render reports/economic_insights.qmd --to html
```
If Quarto doesn't import `econlens` from the repository root, set `PYTHONPATH=.` (PowerShell: `$env:PYTHONPATH='.'`) before rendering. Ensure the Jupyter kernel uses the project virtual environment.


## Project layout

- `econlens/extract.py`: API retrieval with pagination and source provenance.
- `econlens/transform.py`: typed cleaning, missing-data preservation, duplicate checks, coverage report.
- `econlens/storage.py`: SQLite database.
- `econlens/pipeline.py`: reproducible extract/transform/load.
- `app.py`: interactive Streamlit/Plotly dashboard with country, indicator, and year filters.
- `sql/analysis_queries.sql`: year-aligned SQL comparisons.
- `reports/economic_insights.qmd`: reproducible Quarto report.
- `tests/`: isolated unit tests without network calls.


## Future Enhancements

The current MVP includes a functional economic data pipeline, SQLite storage, interactive Streamlit dashboard, automated economic insights, and a published Quarto research report.

Planned improvements:

- Develop a complementary Power BI economic intelligence dashboard.
- Implement GitHub Actions for automated testing.
- Extract reusable analytical functions into an independent Python package (InsightForge).
- Introduce additional economic indicators and comparative analysis.
- Improve data freshness monitoring and automated reporting.


## License/data attribution

Project source code may be published with your chosen license. World Bank data pages identify the associated attribution/license; retain source links when publishing derived charts. Review any series-specific notes before redistribution.
