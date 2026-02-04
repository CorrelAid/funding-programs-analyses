# Todos
- [ ] collect ideas for v1.0 (make ready for exchange)
- [ ] collect ideas for v1.1 (include more sophisticated funding search, tests)

# Requirements
- [ ] v1.0

- [x] v0.4
  - [x] clean repo
    - [x] refractor
  - [x] UI
    - [x] adapt default selection for better initial overview

- [x] v0.3
  - [x] improve location filter
    - [x] change to pills
    - [x] add buttons to add all options
  - [x] improve text search filter
    - [x] add options to search within "Titel", "Kurztext" or "Langtext"
    - [ ] research on how to improve search technique (e.g. not exact but similar term, keyword-based search not whole text, preprocess topics based on description)
  - [x] add eligible applicants
    - [x] add filter
    - [x] introduce comparing visualisation
  - [x] add funding area
    - [x] add filter <- same pattern as for eligible applicants
    - [x] introduce comparing visualisation
  - [x] introduce tabs to switch between metrices/visualisations and tables

- [x] v0.2
  - [x] in displayed dataframe
    - [x] hide index
    - [x] hide id_hash
    - [x] add link
    - [x] add Kurzzusammenfassung
      - [x] split between kurztext and volltext
      - [x] add searching option for long texts
  - [x] add CorrelAid color palette
  - [x] add CorrelAid font

- [x] v0.1
  - [x] visualize descriptive statistics
    - [x] number of projects
    - [x] distribution of funding_location
  
- [x] UI v0.0
  - [x] display dataframe (id_hash, title, funding_area, funding_location)
  - [x] filter for location
  - [x] filter for title
  - [x] filter for funding type

# Ideas by Claude
## Dashboard
  Data & Performance
  - Cache expensive computations with @st.cache_data or @st.cache_resource
  - Load data once, filter in memory
  - Consider data aggregation for large datasets

  Layout & Structure
  - Use st.sidebar for filters and controls
  - Group related metrics with st.columns
  - Use st.tabs or st.expander to organize complex content
  - Keep the most important insights "above the fold"

  Interactivity
  - Provide sensible defaults for all filters
  - Use appropriate widgets (selectbox vs multiselect, slider for ranges)
  - Add st.session_state for cross-widget state when needed

  Visualization
  - Choose chart types that match your data (bar for comparison, line for
  trends, scatter for relationships)
  - Use consistent colors and scales across charts
  - Add clear titles, axis labels, and legends
  - Consider colorblind-friendly palettes

  User Experience
  - Add context with st.metric for KPIs (including delta indicators)
  - Provide explanatory text where needed
  - Show loading states with st.spinner
  - Handle edge cases (empty filters, missing data)

  Code Organization
  - Separate data loading, processing, and visualization into functions
  - Keep the main script as a clear flow of components