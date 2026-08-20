export default function TopicCard({ topic }) {
  if (!topic) return null

  return (
    <div className="rounded border border-wire-light bg-paper-bright p-5">
      <p className="font-mono text-xs uppercase tracking-[0.15em] text-wire">
        Dominant topic
      </p>
      <p className="font-display-en mt-1 text-lg font-semibold text-ink">
        {topic.label}
      </p>
      <p className="hi-text mt-3 text-sm leading-relaxed text-wire">
        {topic.top_words.map((word, i) => (
          <span key={word}>
            {i > 0 && <span className="danda-divider mx-1.5">।</span>}
            {word}
          </span>
        ))}
      </p>
    </div>
  )
}
