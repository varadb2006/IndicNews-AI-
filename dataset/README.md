# Dataset

## Files

- **`hindi_news_dataset.csv`** (git-ignored, ~185 MB, 185,512 rows) — the
  real Inshorts Hindi News dataset, provided directly by the team since
  Kaggle isn't reachable from the dev/training sandbox. Source:
  https://www.kaggle.com/datasets/shivamtaneja2304/inshorts-dataset-hindi

This is the only dataset the project uses — there is no synthetic/sample
fallback. `training/data_utils.py::load_dataset()` loads this file
directly and raises a clear error if it isn't present at
`dataset/hindi_news_dataset.csv`.

## ⚠️ Real schema differs from the original project brief

The brief assumes `News Categories` is a single label per row. **It is
not.** In the real file it's a *stringified Python list* of 1–5 tags,
e.g. `"['politics', 'national']"`, mixing:

- **Core sections** the brief actually wants us to classify:
  `sports`, `politics`, `business`, `technology`, `entertainment`
- **Generic sections**: `national`, `world`, `miscellaneous`
- **One-off event hashtags**: e.g. `लोकसभा_चुनाव_2024`, `आईपीएल_2024`,
  `विश्व_कप_2023`, `एक्सप्लेनर`, `hatke`, `startup`, `fashion`... (34
  distinct tags total)

`data_utils.py` derives a clean single `primary_category` column for
training: the first tag (in order) that matches a core section; anything
else falls into `other`. Full reasoning and the resulting distribution
are in `training/notebooks/01_EDA.ipynb` (§3).

`Date` also mixes two formats (`DD-MM-YYYY` and `YYYY-MM-DD`) —
`data_utils.parse_dates()` handles both.

## ⚠️ Heavy duplication from repeated scraping

The dataset was built by scraping the Inshorts homepage repeatedly; the
same article stays on the front page — and gets re-scraped — for several
consecutive days. Result: **185,512 rows but only ~34,826 unique
(Headline, Content) articles** (~5.3× duplication). See `01_EDA.ipynb`
§2.1 for the full breakdown.

**Always deduplicate on `(Headline, Content)` before**: train/test
splitting, fitting TF-IDF/embeddings, or building the similarity index —
otherwise near-identical rows leak across splits and inflate metrics.

## Setting this up on another machine

1. Download `hindi_news_dataset.csv` (Kaggle link above, or get the file
   directly from the team).
2. Place it at `dataset/hindi_news_dataset.csv` — that exact filename,
   since `data_utils.py` no longer searches for alternate names or falls
   back to sample data.
3. Run `01_EDA.ipynb` (or any other notebook) — `load_dataset()` will
   pick it up automatically.
