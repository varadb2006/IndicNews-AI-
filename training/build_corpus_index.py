
from data_utils import load_dataset
from preprocessing import preprocess_pipeline

if __name__ == "__main__":
    df = load_dataset(verbose=False)
    uniq = df.drop_duplicates(subset=["Headline", "Content"]).reset_index(drop=True)
    clean_df = preprocess_pipeline(uniq, columns=["Headline", "Content"])

    corpus_index = clean_df[["Headline", "core_categories"]].copy()
    corpus_index.to_pickle("../models/saved_models/corpus_index.pkl")

    print(f"Saved corpus_index.pkl with {len(corpus_index)} rows.")
    print("Make sure this matches tfidf_matrix.npz's row count exactly.")
