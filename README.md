# IndicNews AI
### Intelligent Hindi News Analysis, Retrieval & Recommendation System

An end-to-end NLP system that analyzes Hindi news headlines/articles for:
category classification, named entity recognition, keyword extraction,
topic modeling, similar-news recommendation, extractive summarization,
and text analytics.



---

## 📁 Project Structure

```
IndicNewsAI/
│
├── frontend/                      # React.js + Tailwind CSS client
│   ├── public/                    # static assets, index.html
│   └── src/
│       ├── components/            # reusable UI: Cards, Badges, Spinner, Navbar...
│       ├── pages/                 # Home, About, Analyze, Results, Features
│       ├── services/              # Axios API client (calls Flask backend)
│       ├── hooks/                 # custom React hooks (e.g. useAnalyzeNews)
│       └── assets/                # images, icons, fonts
│
├── backend/                        # Flask REST API
│   └── app/
│       ├── routes/                # API endpoints (e.g. /analyze)
│       ├── services/               # business logic: preprocessing, NER,
│       │                           # classification, topic modeling, IR, summarizer
│       ├── utils/                 # helpers: text cleaning, validators, config loader
│       └── models/                # ML model wrapper classes (load/predict)
│
├── models/
│   └── saved_models/               # trained artifacts (.pkl, .model, vectorizers)
│
├── training/
│   └── notebooks/                  # Google Colab notebooks, numbered 01–09
│       # 01_EDA.ipynb
│       # 02_Preprocessing.ipynb
│       # 03_FeatureEngineering.ipynb
│       # 04_WordEmbeddings.ipynb
│       # 05_Classification.ipynb
│       # 06_NER.ipynb
│       # 07_TopicModeling.ipynb
│       # 08_Similarity.ipynb
│       # 09_SaveModels.ipynb
│
├── dataset/                        # raw + processed Hindi news dataset (Inshorts Hindi)
│
├── requirements.txt                 # backend + ML Python dependencies
├── README.md                        # this file
└── .gitignore
```

## 🧱 Tech Stack

| Layer            | Tools |
|------------------|-------|
| Frontend         | React.js, Tailwind CSS, Axios |
| Backend          | Python, Flask REST API |
| ML / NLP         | scikit-learn, NLTK, Gensim, spaCy, Stanza, IndicNLP, NumPy, Pandas |
| Model Training   | Google Colab |
| Dev Environment  | VS Code |

## 📊 Dataset

[Inshorts Hindi News Dataset (Kaggle)](https://www.kaggle.com/datasets/shivamtaneja2304/inshorts-dataset-hindi)
— columns: `Headline`, `Content`, `News Categories`, `Date`.

## 🗺️ Build Roadmap (module-by-module)

1. ✅ Project folder structure
2. ✅ Dataset loading & EDA
3. ✅ Text preprocessing
4. ✅ Feature engineering
5. ✅ Word2Vec & FastText
6. ✅ Classification
7. ✅ NER
8. ✅ Topic modeling
9. ✅ Similarity search
10. ⬜ Backend APIs
11. ⬜ React frontend
12. ⬜ Integration
13. ⬜ Testing
14. ⬜ Documentation
