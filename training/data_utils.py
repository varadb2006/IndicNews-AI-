
import ast
import os
import pandas as pd


DATASET_PATH = "../../dataset/hindi_news_dataset.csv"

REQUIRED_COLUMNS = ["Headline", "Content", "News Categories", "Date"]


CORE_CATEGORIES = ["sports", "politics", "business", "technology", "entertainment", "national"]
OTHER_LABEL = "other"


def load_dataset(path: str = None, verbose: bool = True) -> pd.DataFrame:
    
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
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing required column(s): {missing}. "
            f"Expected columns: {REQUIRED_COLUMNS}. Found: {list(df.columns)}"
        )


def parse_category_list(series: pd.Series) -> pd.Series:
    
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
        return [raw.lower()]

    return series.apply(_parse)


def derive_core_categories(tags) -> list:
    
    matched = [tag for tag in tags if tag in CORE_CATEGORIES]
    return matched if matched else [OTHER_LABEL]


def parse_dates(series: pd.Series) -> pd.Series:
    
    parsed_dmy = pd.to_datetime(series, format="%d-%m-%Y", errors="coerce")
    parsed_ymd = pd.to_datetime(series, format="%Y-%m-%d", errors="coerce")
    return parsed_dmy.fillna(parsed_ymd)