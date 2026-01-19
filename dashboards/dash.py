import pandas as pd
import streamlit as st
import yaml

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
    "Location",
    list(locations_mapping.keys()),
    config["default"]["bundesland"]
    )

funding_type_selection = st.multiselect(
    "Funding Type",
    options=funding_types_available,
    # default=df["funding_type"].value_counts().index[0],
    default=config["default"]["funding_type"]
    )

df_ = df.copy()

df_ = df_.loc[df_["title"].str.lower().str.contains(title_search_term.lower())]

def create_mask(series: pd.Series, criteria: list | set):
    mask = series.fillna('').str.split(',').apply(
        lambda x: bool(set(s.strip() for s in x) & set(criteria)) 
    ) 
    return mask

mask_location = create_mask(df["funding_location"], location_selection + [config["nationwide"]])
df_ = df_.loc[mask_location]

mask_funding_type = create_mask(df["funding_type"], funding_type_selection)
df_ = df_.loc[mask_funding_type]

st.dataframe(df_, column_order=(["id_hash", "title", "funding_location", "funding_type"]))