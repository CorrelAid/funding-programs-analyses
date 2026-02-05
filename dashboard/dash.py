import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils


def create_category_bar_chart(series: pd.Series, categories: list, title: str):
    """Create and display a bar chart for category counts."""
    fig = px.bar(utils.count_categories(series, categories), title=title)
    fig.update_layout({'xaxis_title_text': '', 'yaxis_title_text': '', 'showlegend': False})
    st.plotly_chart(fig, config={'scrollZoom': False}, width="stretch")


df = pd.read_parquet(utils.DATA_DIR / "sample_dashboard_data.parquet")
eligible_applicants_available = utils.extract_categories(df["eligible_applicants"])
funding_area_available = utils.extract_categories(df["funding_area"])
df[["description_short", "description_full"]] = utils.split_description(df)
df_ = df.copy()


st.set_page_config(
    layout="wide"
)

with st.sidebar:
    # Create text search filter.
    st.title("Suche")

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

    # Create filter for funding locations.
    with st.expander("Fördergebiet"):

        # Create switch between individual or complete selection.
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

        # Mask DataFrame.
        if search_term and search_fields:
            search_columns = [k for k,v in config.table.get('column_labels').items() if v in config.default.get('search_fields')]
            mask_search = utils.create_search_mask(df_, search_columns, search_term, fuzzy=config.default.get("fuzzy_search"))
            df_ = df_.loc[mask_search]

        mask_location = utils.create_mask(df["funding_location"], location_selection)
        df_ = df_.loc[mask_location]

    # Create filter for funding area.
    with st.expander("Förderbereich"):
        # Create switch between individual or complete selection.
        all_areas = st.toggle(
            label="alle Bereiche",
            value=False
        )

        if not all_areas:
            funding_area_selection = st.pills(
            label="Funding Area",
            label_visibility="collapsed",
            options=funding_area_available,
            default=config.default.get("funding_area"),
            selection_mode="multi",
            )
        else:
            funding_area_selection = funding_area_available

        # Mask DataFrame.
        mask_location = utils.create_mask(df["funding_area"], funding_area_selection)
        df_ = df_.loc[mask_location]

    # Create filter for eligible applicants.
    with st.expander("Förderberechtigte"):
        eligible_applicants_selection = st.pills(
        label="Eligible Applicants",
        label_visibility="collapsed",
        options=eligible_applicants_available,
        default=eligible_applicants_available,
        selection_mode="multi"
        )

        # Mask DataFrame according to selection.
        mask_location = utils.create_mask(df["eligible_applicants"], eligible_applicants_selection)
        df_ = df_.loc[mask_location]

    st.write(f"{len(df_)} Förderungen gefunden.")

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"][aria-expanded="true"] {
                min-width: 400px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Create tabs to switch between statistics and table of results.
tab_stats, tab_findings = st.tabs(["Statistik", "Suchergebnisse"])

with tab_stats:
    # Plot statistics.
    create_category_bar_chart(df_["funding_location"], location_selection, "Anzahl der Förderungen nach Gebiet")
    create_category_bar_chart(df_["funding_area"], funding_area_selection, "Anzahl der Förderungen nach Bereich")
    create_category_bar_chart(df_["eligible_applicants"], eligible_applicants_selection, "Anzahl der Förderungen nach Berechtigte")

with tab_findings:
    # Prepare masked DataFrame as table.
    df_display = df_.copy()
    df_display["title"] = df_.apply(
        lambda row: f"{row['url']}##{row['title']}" if pd.notna(row["url"]) else row["title"],
        axis=1
    )
    st.dataframe(
        df_display[config.table.get("column_config").keys()],
        hide_index=True,
        column_config=config.table.get("column_config"),
        column_order=config.default.get('column_order'),
        width="stretch",
        )
