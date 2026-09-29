"""Interactive economic time-series dashboard. Launch: streamlit run app.py"""
import pandas as pd
import plotly.express as px
import streamlit as st
from econlens.config import COUNTRIES, INDICATORS
from econlens.storage import read_from_sqlite
from econlens.transform import quality_report

st.set_page_config(page_title='EconLens', page_icon='📈', layout='wide')
st.title('EconLens | Consumer Economy Intelligence')
st.caption('Source: World Bank World Development Indicators • Annual observations • Not Mastercard transaction data')
try:
    df = read_from_sqlite()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()

country_choices = list(COUNTRIES.values())
selected_countries = st.sidebar.multiselect('Countries', country_choices, default=country_choices)
selected_indicator = st.sidebar.selectbox('Indicator', list(INDICATORS.values()))
years = sorted(df['year'].unique())
start_year, end_year = st.sidebar.select_slider('Year range', options=years, value=(years[0], years[-1]))
view = df.loc[(df.country.isin(selected_countries)) & (df.indicator == selected_indicator)
              & df.year.between(start_year, end_year)].copy()
valid = view.dropna(subset=['value'])
if valid.empty:
    st.warning('No published observations for the current selection. Adjust filters.')
    st.stop()
left, middle, right = st.columns(3)
left.metric('Countries with observations', valid.country.nunique())
middle.metric('Latest observation year', int(valid.year.max()))
right.metric('Published data points', len(valid))
st.plotly_chart(px.line(valid, x='year', y='value', color='country', markers=True,
                        labels={'year': 'Year', 'value': 'Annual growth / inflation (%)'},
                        title=selected_indicator), use_container_width=True)
st.info('Interpret carefully: the latest available year may differ by country and indicator. A cross-country comparison requires aligned years.')
st.subheader('Latest available observations (not necessarily the same year)')
latest = valid.sort_values('year').groupby('country', as_index=False).tail(1)
st.dataframe(latest[['country', 'year', 'value']].rename(columns={'year':'observation_year'}), hide_index=True, use_container_width=True)

# Cross-country comparison using a common observation year

year_coverage = valid.groupby('year')['country'].nunique()

common_years = year_coverage[
    year_coverage == len(selected_countries)
].index

st.subheader('Cross-Country Economic Comparison')

if len(common_years) > 0:

    comparison_year = int(max(common_years))

    comparison_data = valid[
        valid['year'] == comparison_year
    ].sort_values('value', ascending=False)

    st.caption(
        f'Latest common observation year: {comparison_year}'
    )

    fig = px.bar(
        comparison_data,
        x='country',
        y='value',
        color='country',
        text_auto='.2f',
        title=f'{selected_indicator} ({comparison_year})',
        labels={
            'country': 'Country',
            'value': 'Annual percentage (%)'
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # Automatically generated economic insight

    highest = comparison_data.iloc[0]
    lowest = comparison_data.iloc[-1]

    difference = highest['value'] - lowest['value']

    st.subheader('Economic Insights')

    st.info(
        f"Among the selected countries in {comparison_year}, "
        f"{highest['country']} recorded "
        f"the highest {selected_indicator.lower()} "
        f"at {highest['value']:.2f}%, while "
        f"{lowest['country']} recorded the lowest "
        f"at {lowest['value']:.2f}%. "
        f"The difference between these economies was "
        f"{difference:.2f} percentage points."
    )
else:
    st.warning(
        'No common observation year is available '
        'for the selected countries.'
    )
st.subheader('Data quality and coverage')
st.dataframe(quality_report(df), hide_index=True, use_container_width=True)
st.download_button('Download filtered data (CSV)', data=view.to_csv(index=False), file_name='econlens_filtered.csv', mime='text/csv')
