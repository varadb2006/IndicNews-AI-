import { Link } from 'react-router-dom'
import CategoryStamp from '../components/CategoryStamp'

const PIPELINE_STEPS = [
  { en: 'Clean the text', detail: 'Devanagari-aware normalization and tokenization' },
  { en: 'Classify', detail: 'Multi-label category prediction, TF-IDF + Logistic Regression' },
  { en: 'Extract entities', detail: 'People, places, organizations via Stanza + a gazetteer' },
  { en: 'Find the topic', detail: 'NMF topic modeling over the full corpus' },
  { en: 'Surface similar dispatches', detail: 'Cosine similarity over TF-IDF vectors' },
]

const CREDENTIALS = [
  { value: '34,826', label: 'unique articles trained on' },
  { value: '60,359', label: 'TF-IDF features' },
  { value: '0.850', label: 'classifier micro F1' },
  { value: '7', label: 'categories, multi-label' },
]

export default function Home() {
  return (
    <div>
      <section className="border-b border-wire-light bg-ink text-paper-bright">
        <div className="mx-auto grid max-w-6xl gap-10 px-6 py-20 md:grid-cols-2 md:items-center">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.25em] text-marigold">
              Hindi News Analysis Desk
            </p>
            <h1 className="font-display-en mt-4 text-4xl font-semibold leading-tight md:text-5xl">
              Every headline,
              <br />
              stamped and filed.
            </h1>
            <p className="mt-5 max-w-md font-body-en text-paper-bright/80">
              Paste a Hindi headline or full article. Get its category, named
              entities, keywords, dominant topic, and the five most similar
              dispatches on record &mdash; in under a second.
            </p>
            <Link
              to="/analyze"
              className="mt-8 inline-block rounded bg-stamp px-6 py-3 font-display-en font-semibold text-paper-bright hover:opacity-90"
            >
              Open the desk
            </Link>
          </div>

          
          <div className="rounded border border-paper-bright/20 bg-paper-bright/5 p-6">
            <p className="hi-text mb-6 text-lg leading-relaxed text-paper-bright">
              भारतीय क्रिकेट टीम ने आज मैच में शानदार जीत दर्ज की
            </p>
            <div className="flex flex-wrap gap-4">
              <CategoryStamp label="sports" confidence={99.5} index={0} />
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-16">
        <h2 className="font-display-en text-2xl font-semibold text-ink">
          What happens when you press analyze
        </h2>
        <ol className="mt-8 space-y-6">
          {PIPELINE_STEPS.map((step, i) => (
            <li key={step.en} className="flex items-baseline gap-4">
              <span className="font-mono text-sm text-wire">
                {String(i + 1).padStart(2, '0')}
              </span>
              <span className="danda-divider text-wire">।</span>
              <div>
                <span className="hi-display text-lg text-stamp">{step.en}</span>
                <p className="font-body-en text-sm text-wire">{step.detail}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="border-t border-wire-light bg-paper-bright">
        <div className="mx-auto max-w-6xl px-6 py-12">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">
            On the record
          </p>
          <div className="mt-6 grid grid-cols-2 gap-8 md:grid-cols-4">
            {CREDENTIALS.map((c) => (
              <div key={c.label}>
                <p className="font-mono text-3xl text-ink">{c.value}</p>
                <p className="font-body-en text-sm text-wire">{c.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
