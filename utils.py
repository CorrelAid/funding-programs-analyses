from pathlib import Path

import pandas as pd
import re

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"


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
    Count every single occurrence of given values in each cell in given Series.
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
