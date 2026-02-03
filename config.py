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
    "funding_location": ["bundesweit","Hamburg", "Niedersachsen", "Schleswig-Holstein"],
    "funding_type": ["Zuschuss"],
    "search_fields": ["Titel", "Kurztext", "Volltext"]
}

table = {
    "column_config": {
        "title": "Titel",
        "funding_location": "Gebiet",
        "eligible_applicants": "Berechtigte",
        "funding_area": "Förderbereich",
        # "funding_type": "Art",
        # "description": "Beschreibung",
        "description_short": "Kurztext",
        "description_full": "Volltext",
        "url": st.column_config.LinkColumn(
                "Link",
                display_text="Link"
        )
    }
}