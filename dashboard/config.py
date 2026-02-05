import streamlit as st

funding_locations = {
    "mapping": {
        "Bayern": "BY",
        "Baden-Württemberg": "BW",
        "Berlin": "BE",
        "Brandenburg": "BB",
        "Bremen": "HB",
        "Hamburg": "HH",
        "Hessen": "HE",
        "Mecklenburg-Vorpommern": "MV",
        "Niedersachsen": "NI",
        "Nordrhein-Westfalen": "NW",
        "Rheinland-Pfalz": "RP",
        "Saarland": "SL",
        "Sachsen": "SN",
        "Sachsen-Anhalt": "ST",
        "Schleswig-Holstein": "SH",
        "Thüringen": "TH"
    },
    "nationwide": "bundesweit"
}

default = {
    "search_fields": ["Titel", "Kurztext", "Volltext"],
    "fuzzy_search": True,
    "funding_location": ["bundesweit","Hamburg", "Niedersachsen", "Schleswig-Holstein"],
    "funding_type": ["Zuschuss"],
    "funding_area": ["Frauenförderung","Gesundheit & Soziales", "Infrastruktur", "Wohnungsbau & Modernisierung", "Mobilität", "Landwirtschaft & Ländliche Entwicklung"],
    "column_order": ["title", "funding_location", "funding_area", "eligible_applicants"], # sets default visible columns
}

table = {
    "column_config": {
        "title": st.column_config.LinkColumn(
            label="Titel",
            display_text=r".*##(.+)",
        ),
        "funding_location": st.column_config.Column(
            label="Gebiet",
        ),
        "eligible_applicants": st.column_config.Column(
            label="Berechtigte",
        ),
        "funding_area": st.column_config.Column(
            label="Förderbereich",
        ),
        "description_short": st.column_config.Column(
            label="Kurztext",
        ),
        "description_full": st.column_config.Column(
            label="Volltext",
        ),
    },
}

table["column_labels"] = {k:v.get('label') for k,v in table.get('column_config').items()}