import { useLocation, Link } from 'react-router-dom'
import CategoryStamp from '../components/CategoryStamp'
import EntityCard from '../components/EntityCard'
import KeywordChip from '../components/KeywordChip'
import TopicCard from '../components/TopicCard'
import StatisticsPanel from '../components/StatisticsPanel'
import SimilarArticleCard from '../components/SimilarArticleCard'

export default function Results() {
  const location = useLocation()
  const result = location.state?.result
  const sourceText = location.state?.sourceText

  if (!result) {
    return (
      <div className="mx-auto max-w-2xl px-6 py-20 text-center">
        <p className="hi-display text-3xl text-wire">।</p>
        <h1 className="font-display-en mt-4 text-2xl font-semibold text-ink">
          No dispatch on file
        </h1>
        <p className="mt-2 font-body-en text-wire">
          Results only exist right after an analysis runs. Submit a headline
          or article to see one here.
        </p>
        <Link
          to="/analyze"
          className="mt-6 inline-block rounded bg-stamp px-6 py-2.5 font-display-en font-semibold text-paper-bright hover:opacity-90"
        >
          Go to the desk
        </Link>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      {sourceText && (
        <p className="hi-text mb-8 rounded border-l-4 border-stamp bg-paper-bright p-4 text-lg leading-relaxed text-ink">
          {sourceText}
        </p>
      )}

      <section className="mb-10">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">Category</p>
        <div className="mt-4 flex flex-wrap gap-4">
          {result.categories.map((c, i) => (
            <CategoryStamp key={c.label} label={c.label} confidence={c.confidence} index={i} />
          ))}
        </div>
      </section>

      {result.summary && (
        <section className="mb-10">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">Summary</p>
          <p className="hi-text mt-3 leading-relaxed text-ink">{result.summary}</p>
        </section>
      )}

      <section className="mb-10 grid gap-10 md:grid-cols-2">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">
            Entities
          </p>
          <div className="mt-4">
            <EntityCard entities={result.entities} />
          </div>
        </div>

        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">
            Keywords
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            {result.keywords.map((kw) => (
              <KeywordChip key={kw} keyword={kw} />
            ))}
          </div>
        </div>
      </section>

      <section className="mb-10">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">Topic</p>
        <div className="mt-4">
          <TopicCard topic={result.topic} />
        </div>
      </section>

      <section className="mb-10">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">
          Statistics
        </p>
        <div className="mt-4">
          <StatisticsPanel statistics={result.statistics} />
        </div>
      </section>

      <section>
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-wire">
          Similar dispatches
        </p>
        <div className="mt-4 rounded border border-wire-light bg-paper-bright px-5">
          {result.similar_articles.map((article) => (
            <SimilarArticleCard key={article.headline} article={article} />
          ))}
        </div>
      </section>

      <Link
        to="/analyze"
        className="mt-12 inline-block font-mono text-sm text-wire underline decoration-dotted underline-offset-4 hover:text-stamp"
      >
        &larr; analyze another
      </Link>
    </div>
  )
}
