from pathlib import Path

import pandas as pd
import re
from rapidfuzz import fuzz

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


def parse_search_terms(search_input: str) -> list[str]:
    """
    Parse search input into individual terms, preserving quoted phrases.
    Example: 'climate "renewable energy" solar' -> ['climate', 'renewable energy', 'solar']
    """
    phrases = re.findall(r'"([^"]+)"', search_input)
    remaining = re.sub(r'"[^"]+"', '', search_input)
    words = [w.strip() for w in remaining.split() if w.strip()]
    return phrases + words


def text_matches_terms(text: str, terms: list[str], fuzzy: bool = False, threshold: int = 80) -> bool:
    """
    Check if text contains all search terms (AND logic).
    With fuzzy=True, uses fuzzy matching for typo tolerance.
    """
    if pd.isna(text):
        return False
    text_lower = str(text).lower()

    for term in terms:
        term_lower = term.lower()
        if fuzzy:
            if fuzz.partial_ratio(term_lower, text_lower) < threshold:
                return False
        else:
            if term_lower not in text_lower:
                return False
    return True


def create_search_mask(df: pd.DataFrame, columns: list[str], search_input: str, fuzzy: bool = False) -> pd.Series:
    """
    Create a boolean mask for rows where any of the specified columns match all search terms.
    """
    terms = parse_search_terms(search_input)
    if not terms:
        return pd.Series(True, index=df.index)

    return df[columns].apply(
        lambda row: any(text_matches_terms(cell, terms, fuzzy) for cell in row),
        axis=1
    )
