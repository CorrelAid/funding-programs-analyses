import config

import hashlib
import pandas as pd
import plotly.express as px
import re
import streamlit as st

### Define functions.

def create_mask(series: pd.Series, criteria: list | set):
    """
    Create a mask for a DataFrame based on given criteria.
    """
    mask = series.fillna('').str.split(',').apply(
        lambda x: bool(set(s.strip() for s in x) & set(criteria)) 
    ) 
    return mask

def count_individually(series: pd.Series, values: list):
    """
    Count every single occurences of given values in each cell in given Series.
    """
    counts = {
        v: series.str.contains(rf"\b{v}\b(?!-)", na=False, regex=True).sum() for v in values
    }
    return pd.Series(counts)

def split_description(series: pd.Series) -> pd.DataFrame:
    """
    Split the description column into their paragraps, i.e. 'short' and 'full' text.
    """
    extracted = series["description"].str.extract(
        r"### Kurztext\s*(.*?)\s*### Volltext\s*(.*)", 
        flags=re.DOTALL
    )
    return extracted

### Setup streamlit page.

st.set_page_config(
    layout="wide"
)

### Preprocess DataFrame with fundings.

df = pd.read_parquet("data/sample_dashboard_data.parquet")
df[["description_short", "description_full"]] = split_description(df)
df_ = df.copy()

### Create dashboards elements.

with st.sidebar:
    # Create filters.
    title_search_term = st.text_input("Title")
    location_selection = st.pills(
        label="Location",
        options=list(config.funding_locations.get("mapping").keys()) + [config.funding_locations.get("nationwide")],
        default=config.default.get("funding_location"),
        selection_mode="multi"
        )

    # Mask DataFrame according to set filters in dashboard.

    df_ = df_.loc[df_["title"].str.lower().str.contains(title_search_term.lower())]

    mask_location = create_mask(df["funding_location"], location_selection)
    df_ = df_.loc[mask_location]

    st.write(f"Number of fundings found: {len(df_)}")
    



fig = px.bar(count_individually(df_["funding_location"], location_selection), title="Counts of fundings per location")
fig.update_layout({
    'xaxis_title_text': 'State',
    'yaxis_title_text': 'Counts',
    'showlegend': False, 
})
st.plotly_chart(fig, config = {'scrollZoom': False})

st.dataframe(
    df_[config.table.get("column_config").keys()],
    hide_index=True,
    column_config=config.table.get("column_config"),
    )