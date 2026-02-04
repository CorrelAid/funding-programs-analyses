Funding Program Analyses
================

The `Funding Program Analyses` project processes information on German funding programs given on [Förderdatenbank website](https://www.foerderdatenbank.de/FDB/DE/Home/home.html). The information is presented in an interactive Dashboard.

Please note that this project is in early-stage.

# Project Structure

 ```bash
  ├── dashboard/                                                                    
  │   ├── config.py         # configuration for dashboard
  │   └── dash.py           # streamlit dashboard app
  ├── data/*.parquet        # data directory
  ├── notebooks/eda.ipynb   # exploratory analysis
  ├── requirements.txt      # python dependencies
  ├── run_dashboard.sh      # dashboard launch script
  └── utils.py              # shared utilities
  ```

# Data

This project relies on data which is provided by a [funding scraper](https://github.com/CorrelAid/cdl_funding_scraper). The scraper collects publicly available information on all fundings on the [Förderdatenbank website](https://www.foerderdatenbank.de/FDB/DE/Home/home.html). For details on the scraper please see the [funding scraper](https://github.com/CorrelAid/cdl_funding_scraper).

# Development

## Dependencies

Python dependencies are listed in 'requirements.txt'.



