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
    "funding_location": ["Hamburg"],
    "funding_type": ["Zuschuss"],
}

table = {
    "column_config": {
        "title": "Titel",
        "funding_location": "Land",
        "funding_type": "Finanzierung",
        "url": st.column_config.LinkColumn(
                "Link",
                display_text="Link"
        )
    }
}