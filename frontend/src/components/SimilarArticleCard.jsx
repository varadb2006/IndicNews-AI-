export default function SimilarArticleCard({ article }) {
  return (
    <div className="border-b border-dashed border-wire-light py-4 last:border-0">
      <div className="flex items-start justify-between gap-4">
        <p className="hi-text text-base leading-snug text-ink">{article.headline}</p>
        <span className="shrink-0 font-mono text-xs text-marigold">
          {article.similarity_percent}%
        </span>
      </div>
      <p className="mt-1 font-mono text-[0.65rem] uppercase tracking-[0.1em] text-wire">
        {article.categories.join(' \u00b7 ')}
      </p>
    </div>
  )
}
