const FEATURES = [
  {
    en: 'Multi-label classification',
    detail:
      'Predicts category across seven labels (sports, politics, business, technology, entertainment, national, other) using TF-IDF features and a One-vs-Rest Logistic Regression classifier. Genuinely multi-label, not single-label with a shrug: 15.5% of the training corpus carries two or more categories at once, and the model reflects that. Micro F1 0.850 on held-out data.',
  },
  {
    en: 'Named entity recognition',
    detail:
      'People, locations, and organizations extracted via Stanza\u2019s Hindi pipeline, backed by a small gazetteer of well-known political parties for cases the statistical model misses on its own (a normal recall limitation, not a flaw specific to this data).',
  },
  {
    en: 'Keyword extraction',
    detail:
      'Top terms by TF-IDF weight within the submitted text, drawn from a 60,359-feature vocabulary spanning unigrams through trigrams \u2014 so a phrase like "\u0935\u093f\u0936\u094d\u0935 \u0915\u092a" surfaces as one keyword, not two disconnected words.',
  },
  {
    en: 'Topic modeling',
    detail:
      'Seven latent topics discovered via NMF over the full corpus, chosen over LDA after a direct side-by-side comparison showed cleaner, more coherent topic-word groupings.',
  },
  {
    en: 'Similar article search',
    detail:
      'Cosine similarity (via a normalized dot product) over TF-IDF vectors returns the five most similar articles already on record, computed live in tens of milliseconds \u2014 fast enough to run on every request without precomputing anything.',
  },
  {
    en: 'Extractive summarization',
    detail:
      'For articles of 40 words or more, the highest TF-IDF-scoring sentences are selected and returned in their original order. Shorter dataset rows are already summary-length by nature (Inshorts-style reporting averages ~59 words), so summarization only kicks in where it would actually help.',
  },
  {
    en: 'Text statistics',
    detail:
      'Word count, character count, sentence count, and an estimated reading time \u2014 computed on the raw text as submitted, not the cleaned/stemmed version, since that would count something other than what was actually typed.',
  },
]

export default function Features() {
  return (
    <div className="mx-auto max-w-4xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-[0.25em] text-marigold">
        Capabilities
      </p>
      <h1 className="font-display-en mt-2 text-3xl font-semibold text-ink">
        Everything one dispatch gets run through
      </h1>

      <div className="mt-10 divide-y divide-wire-light border-y border-wire-light">
        {FEATURES.map((f) => (
          <article key={f.en} className="grid gap-2 py-8 md:grid-cols-[1fr_2fr] md:gap-8">
            <div>
              <span className="hi-display block text-2xl text-stamp">{f.en}</span>
            </div>
            <p className="font-body-en text-sm leading-relaxed text-wire">{f.detail}</p>
          </article>
        ))}
      </div>
    </div>
  )
}
