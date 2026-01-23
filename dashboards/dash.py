import pandas as pd
import plotly.express as px
import streamlit as st
import yaml

def create_mask(series: pd.Series, criteria: list | set):
    mask = series.fillna('').str.split(',').apply(
        lambda x: bool(set(s.strip() for s in x) & set(criteria)) 
    ) 
    return mask

def count_individually(series: pd.Series, values: list):
    counts = {
        v: series.str.contains(rf"\b{v}\b(?!-)", na=False, regex=True).sum() for v in values
    }
    return pd.Series(counts)

config_file = "config.yaml"
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

locations_mapping = config["bundesland_abbr"]

st.set_page_config(
    layout="wide"
)

df = pd.read_parquet("data/sample_dashboard_data.parquet")

funding_types_available = {i.strip() for x in list(df["funding_type"].dropna().unique()) for i in x.split(',')}

title_search_term = st.text_input("Title")
location_selection = st.multiselect(
    label="Location",
    options=list(locations_mapping.keys()) + [config["nationwide"]],
    default=config["default"]["bundesland"]
    )

funding_type_selection = st.multiselect(
    label="Funding Type",
    options=funding_types_available,
    default=config["default"]["funding_type"]
    )

df_ = df.copy()

df_ = df_.loc[df_["title"].str.lower().str.contains(title_search_term.lower())]

mask_location = create_mask(df["funding_location"], location_selection)
df_ = df_.loc[mask_location]

mask_funding_type = create_mask(df["funding_type"], funding_type_selection)
df_ = df_.loc[mask_funding_type]

st.write(f"Number of fundings found: {len(df_)}")

fig = px.bar(count_individually(df_["funding_location"], location_selection), title="Counts of fundings per location")
fig.update_layout({
    'xaxis_title_text': 'State',
    'yaxis_title_text': 'Counts',
    'showlegend': False, 
})
st.plotly_chart(fig, config = {'scrollZoom': False})

fig = px.bar(count_individually(df_["funding_type"], funding_type_selection), title="Counts of fundings per type")
fig.update_layout({
    'xaxis_title_text': 'Type',
    'yaxis_title_text': 'Counts',
    'showlegend': False, 
})
st.plotly_chart(fig, config = {'scrollZoom': False})

st.dataframe(df_, column_order=(["id_hash", "title", "funding_location", "funding_type"]))