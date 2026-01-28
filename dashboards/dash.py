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
    st.title("Sucheinstellungen")

    st.divider()

    # st.text("Textsuche")
    search_term = st.text_input(
        label="search_term",
        label_visibility="collapsed",
        placeholder="Suchebegriffe",
        )
    
    # st.text("Suchfelder")
    search_fields = st.segmented_control(
        label="search_fields",
        label_visibility="collapsed",
        options=["Titel", "Kurztext", "Volltext"],
        default=config.default.get("search_fields"),
        selection_mode="multi",
        width="stretch"
    )
    if search_term and not search_fields:
        st.warning("Bitte mindestens ein Suchfeld auswählen.")

    st.divider()

    # st.text("Waehle Bundeslaender")
    all_states = st.toggle(
        label="wähle Bundesländer aus"
    )
    if not all_states:
        location_selection = st.pills(
            label="Location",
            label_visibility="collapsed",
            options=list(config.funding_locations.get("mapping").keys()) + [config.funding_locations.get("nationwide")],
            default=config.default.get("funding_location"),
            selection_mode="multi",
            )
    else:
        location_selection = list(config.funding_locations.get("mapping").keys()) + [config.funding_locations.get("nationwide")]

    # Mask DataFrame according to set filters in dashboard.
    if search_term and search_fields:
        search_columns = [k for k,v in config.table.get("column_config").items() if v in search_fields]
        mask_search = df_[search_columns].apply(
            lambda col: col.str.lower().str.contains(search_term.lower(), na=False)
        ).any(axis=1)
        df_ = df_.loc[mask_search]

    mask_location = create_mask(df["funding_location"], location_selection)
    df_ = df_.loc[mask_location]

    st.divider()

    st.write(f"{len(df_)} Suchergebnisse.")
    

tab_stats, tab_findings = st.tabs(["Statistik", "Suchergebnisse"])

with tab_stats:
    fig = px.bar(count_individually(df_["funding_location"], location_selection), title="Counts of fundings per location")
    fig.update_layout({
        'xaxis_title_text': 'State',
        'yaxis_title_text': 'Counts',
        'showlegend': False, 
    })
    st.plotly_chart(fig, config = {'scrollZoom': False})
with tab_findings:
    st.dataframe(
        df_[config.table.get("column_config").keys()],
        hide_index=True,
        column_config=config.table.get("column_config"),
        )