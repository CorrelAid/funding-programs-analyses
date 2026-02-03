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

def count_categories(series: pd.Series, values: list) -> pd.Series:
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

def extract_categories(series: pd.Series, separator=",") -> list:
    """
    Split each element into constiuent categories and return set of unique categories.
    """
    return sorted({i.strip() for x in list(series.dropna().unique()) for i in x.split(separator)})

### Setup streamlit dashboard.

st.set_page_config(
    layout="wide"
)

### Preprocess DataFrame with fundings.

df = pd.read_parquet("data/sample_dashboard_data.parquet")
eligible_applicants_available = extract_categories(df["eligible_applicants"])
funding_area_available = extract_categories(df["funding_area"])
df[["description_short", "description_full"]] = split_description(df)
df_ = df.copy()

### Create dashboards elements.

## Create sidebar with filters.
with st.sidebar:
    # Create text search filter.
    st.title("Sucheinstellungen")

    search_term = st.text_input(
        label="search_term",
        label_visibility="collapsed",
        placeholder="Suchebegriffe",
        )
    
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

    st.markdown("\n")

    ## Create filter for funding locations.
    with st.expander("Fördergebiet"):

        # Create toggle button to switch between individual selection of locations or complete selection.
        all_states = st.toggle(
            label="alle Bundesländer",
            value=True
        )

        # Create selection for locations.
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

        # Mask DataFrame according to selection.
        if search_term and search_fields:
            search_columns = [k for k,v in config.table.get("column_config").items() if v in search_fields]
            mask_search = df_[search_columns].apply(
                lambda col: col.str.lower().str.contains(search_term.lower(), na=False)
            ).any(axis=1)
            df_ = df_.loc[mask_search]

        mask_location = create_mask(df["funding_location"], location_selection)
        df_ = df_.loc[mask_location]

    ## Create filter filter for eligible applicants.
    with st.expander("Förderbereich"):
        # funding_area_selection = st.multiselect(
        funding_area_selection = st.pills(
        label="Funding Area",
        label_visibility="collapsed",
        options=funding_area_available,
        default=funding_area_available,
        selection_mode="multi"
        )
    
        # Mask DataFrame according to selection.
        mask_location = create_mask(df["funding_area"], funding_area_selection)
        df_ = df_.loc[mask_location]

    ## Create filter filter for eligible applicants.
    with st.expander("Förderberechtigte"):
        eligible_applicants_selection = st.pills(
        label="Eligible Applicants",
        label_visibility="collapsed",
        options=eligible_applicants_available,
        default=eligible_applicants_available,
        selection_mode="multi"
        )
    
        # Mask DataFrame according to selection.
        mask_location = create_mask(df["eligible_applicants"], eligible_applicants_selection)
        df_ = df_.loc[mask_location]

    st.write(f"{len(df_)} Förderungen gefunden.")
    
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                min-width: 400px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

## Create tabs to switch between statistics and table of results.
tab_stats, tab_findings = st.tabs(["Statistik", "Suchergebnisse"])

with tab_stats:
    # Plot counts of fundings per location.
    fig = px.bar(count_categories(df_["funding_location"], location_selection), title="Anzahl der Förderungen nach Gebiet")
    fig.update_layout({
        'xaxis_title_text': '',
        'yaxis_title_text': '',
        'showlegend': False, 
    })
    st.plotly_chart(fig, config = {'scrollZoom': False})

    # Plot counts of fundings per area.
    fig = px.bar(count_categories(df_["funding_area"], funding_area_selection), title="Anzahl der Förderungen nach Bereich")
    fig.update_layout({
        'xaxis_title_text': '',
        'yaxis_title_text': '',
        'showlegend': False, 
    })
    st.plotly_chart(fig, config = {'scrollZoom': False})

    # Plot counts of fundings per eligible applicant.
    fig = px.bar(count_categories(df_["eligible_applicants"], eligible_applicants_selection), title="Anzahl der Förderungen Berechtigte")
    fig.update_layout({
        'xaxis_title_text': '',
        'yaxis_title_text': '',
        'showlegend': False, 
    })
    st.plotly_chart(fig, config = {'scrollZoom': False})

with tab_findings:
    # Display masked DataFrame as table.
    st.dataframe(
        df_[config.table.get("column_config").keys()],
        hide_index=True,
        column_config=config.table.get("column_config"),
        )