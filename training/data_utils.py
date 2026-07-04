"""
data_utils.py
--------------
Shared dataset loading & validation helpers used across every training
notebook (01_EDA ... 09_SaveModels). Centralising this here means we only
fix path/schema handling in one place.

Real-world schema notes (learned from the actual Kaggle export the team
downloaded, `dataset/hindi_news_dataset.csv`, 185,512 rows):

    Headline           : str  - short Hindi headline
    Content            : str  - full Hindi article body
    News Categories    : str  - a *stringified Python list* of tags, e.g.
                                 "['politics', 'national']" — NOT a single
                                 label. Rows carry 1-5 tags mixing broad
                                 sections (national/world/business/politics/
                                 entertainment/technology/sports/
                                 miscellaneous) with narrow event hashtags
                                 (e.g. 'लोकसभा_चुनाव_2024', 'आईपीएल_2024').
    Date               : str  - mixed formats in the wild: some rows use
                                 'DD-MM-YYYY', others 'YYYY-MM-DD'.

Because the real data is inherently multi-label (a row can be tagged
both `sports` and `national`), this module keeps that multi-label shape
instead of collapsing it to one class. `derive_core_categories()` filters
each row's tags down to just the ones the classifier cares about (see
`CORE_CATEGORIES`), producing a `core_categories` **list** column —
`["other"]` if none of the row's tags match a core category. Module 6
(Classification) will train a multi-label model against this column
rather than a single-label one.

Usage (from a notebook):
    import sys
    sys.path.append("..")            # so training/ is importable
    from data_utils import load_dataset

    df = load_dataset()              # loads dataset/hindi_news_dataset.csv
                                      # already includes `core_categories`
"""

import ast
import os
import pandas as pd

# Path is relative to the `training/notebooks/` folder where the notebooks
# live, so this works unchanged both locally and in Colab (after
# mounting/uploading the `dataset/` folder).
DATASET_PATH = "../../dataset/hindi_news_dataset.csv"

REQUIRED_COLUMNS = ["Headline", "Content", "News Categories", "Date"]

# The categories the classifier predicts. Anything that doesn't carry one
# of these tags falls into "other" (e.g. world/miscellaneous/event-only rows).
CORE_CATEGORIES = ["sports", "politics", "business", "technology", "entertainment", "national"]
OTHER_LABEL = "other"


def load_dataset(path: str = None, verbose: bool = True) -> pd.DataFrame:
    """
    Load the real Hindi news dataset (`dataset/hindi_news_dataset.csv`).

    Raises a clear error if the file is missing or doesn't match the
    expected schema, instead of failing later inside some other module.
    """
    resolved_path = path or DATASET_PATH

    if not os.path.exists(resolved_path):
        raise FileNotFoundError(
            f"Could not find dataset at '{resolved_path}'. "
            "Place the real dataset CSV at dataset/hindi_news_dataset.csv "
            "(source: https://www.kaggle.com/datasets/shivamtaneja2304/"
            "inshorts-dataset-hindi)."
        )

    df = pd.read_csv(resolved_path, encoding="utf-8-sig")
    validate_schema(df)

    df["category_list"] = parse_category_list(df["News Categories"])
    df["core_categories"] = df["category_list"].apply(derive_core_categories)
    df["parsed_date"] = parse_dates(df["Date"])

    if verbose:
        n_bad_dates = df["parsed_date"].isna().sum()
        print(f"[data_utils] Loaded dataset: {resolved_path}")
        print(f"[data_utils] Shape: {df.shape}")
        print(f"[data_utils] Unparseable dates: {n_bad_dates} ({n_bad_dates / len(df):.2%})")
        print(f"[data_utils] core_categories tag counts (rows can have >1 tag):")
        print(df["core_categories"].explode().value_counts())
        print(f"[data_utils] labels per row:\n{df['core_categories'].apply(len).value_counts().sort_index()}")

    return df


def validate_schema(df: pd.DataFrame) -> None:
    """Raise a descriptive error if any required column is missing."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing required column(s): {missing}. "
            f"Expected columns: {REQUIRED_COLUMNS}. Found: {list(df.columns)}"
        )


def parse_category_list(series: pd.Series) -> pd.Series:
    """
    Parse the `News Categories` column, which is a *stringified* Python
    list (e.g. "['politics', 'national']"), into an actual list of
    lowercase tag strings per row.
    """

    def _parse(raw):
        if isinstance(raw, list):
            return [str(t).strip().lower() for t in raw]
        if not isinstance(raw, str):
            return [OTHER_LABEL]
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            try:
                parsed = ast.literal_eval(raw)
                return [str(t).strip().lower() for t in parsed]
            except (ValueError, SyntaxError):
                pass
        # unexpected plain-string value — treat it as a single tag
        return [raw.lower()]

    return series.apply(_parse)


def derive_core_categories(tags) -> list:
    """
    Filter a row's raw tag list down to just the categories the classifier
    is trained on: Sports / Politics / Business / Technology /
    Entertainment / National.

    Real rows mix these broad section tags with narrow event hashtags
    (e.g. 'लोकसभा_चुनाव_2024') and other generic sections (world,
    miscellaneous). We keep ALL matching core tags, in their original
    order, since a row is often legitimately both e.g. `sports` AND
    `national` — collapsing that to a single label would throw away real
    information. Rows with no core tag at all get `["other"]`.
    """
    matched = [tag for tag in tags if tag in CORE_CATEGORIES]
    return matched if matched else [OTHER_LABEL]


def parse_dates(series: pd.Series) -> pd.Series:
    """
    Parse the `Date` column, which mixes 'DD-MM-YYYY' and 'YYYY-MM-DD'
    formats in the real dataset. Tries both explicitly (fast, no per-row
    format guessing) and merges the results; anything still unparseable
    becomes NaT rather than silently wrong.
    """
    parsed_dmy = pd.to_datetime(series, format="%d-%m-%Y", errors="coerce")
    parsed_ymd = pd.to_datetime(series, format="%Y-%m-%d", errors="coerce")
    return parsed_dmy.fillna(parsed_ymd)